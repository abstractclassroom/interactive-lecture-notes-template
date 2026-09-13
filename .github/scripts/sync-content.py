#!/usr/bin/env python3
"""Publish tracked lessons through course-bound GitHub OIDC and S3 staging."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

MAX_FILES = 1000
MAX_BYTES = 100_000_000
IMAGES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}\Z")
ORDERED = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,119}\Z")


def regular_file(root: Path, name: str) -> Path:
    path = root / name
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("A lesson file is missing or outside the repository.")
    if any(parent.is_symlink() for parent in [path, *path.parents] if parent != root):
        raise ValueError("Lesson uploads do not follow symbolic links.")
    return path


def collect_content(root: Path, destination: Path) -> bytes:
    tracked = set(filter(None, subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root,
    ).decode("utf-8").split("\0")))
    selected: set[str] = set()
    for filename in sorted(tracked):
        if not filename.endswith("/config.json"):
            continue
        lesson = filename.removesuffix("/config.json")
        parts = lesson.split("/")
        if any(part.startswith(".") for part in parts):
            continue
        if len(parts) > 12 or not all(SEGMENT.fullmatch(part) for part in parts):
            raise ValueError("A lesson directory has an unsupported path.")
        config_path = regular_file(root, filename)
        if config_path.stat().st_size > 64_000:
            raise ValueError("A lesson configuration exceeds 64 KB.")
        config = json.loads(config_path.read_text(encoding="utf-8"))
        order = config.get("order")
        if config.get("schemaVersion") != 1 or not isinstance(order, list) or not 1 <= len(order) <= 40:
            raise ValueError("A lesson configuration has invalid schema or order.")
        selected.add(filename)
        for name in order:
            if not isinstance(name, str) or not ORDERED.fullmatch(name) or not name.endswith((".md", ".question.json")):
                raise ValueError("A lesson order contains an unsupported file.")
            path = f"{lesson}/{name}"
            if path not in tracked:
                raise ValueError("An ordered lesson file is missing or untracked.")
            selected.add(path)
        for path in tracked:
            if path.startswith(lesson + "/") and Path(path).suffix.lower() in IMAGES:
                selected.add(path)
    if not selected or len(selected) > MAX_FILES:
        raise ValueError("A publication must have 1 through 1000 files.")
    manifest = []
    total = 0
    for name in sorted(selected):
        if len(name) > 500:
            raise ValueError("A lesson file path is too long.")
        source = regular_file(root, name)
        limit = 5_000_000 if source.suffix.lower() in IMAGES else 256_000 if name.endswith(".md") else 64_000
        size = source.stat().st_size
        total += size
        if size > limit or total > MAX_BYTES:
            raise ValueError("Lesson content exceeds its file or 100 MB publication limit.")
        data = source.read_bytes()
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        manifest.append({"path": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    encoded = json.dumps({"schemaVersion": 1, "files": manifest}, separators=(",", ":")).encode()
    if len(encoded) > 256_000:
        raise ValueError("The publication manifest exceeds 256 KB.")
    return encoded


def json_request(request: urllib.request.Request) -> dict:
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def call_api(body: dict) -> dict:
    # Fresh identity for each request, including polling after a long upload.
    url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"] + "&audience=" + os.environ["ABSTRACTCLASSROOM_AUDIENCE"]
    oidc = json_request(urllib.request.Request(url, headers={
        "Authorization": "bearer " + os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"],
    }))["value"]
    print("::add-mask::" + oidc, flush=True)
    return json_request(urllib.request.Request(
        os.environ["ABSTRACTCLASSROOM_ENDPOINT"], data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + oidc, "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    ))


def main() -> None:
    root = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip() != os.environ["GITHUB_SHA"]:
        raise ValueError("The checked-out commit differs from the workflow commit.")
    with tempfile.TemporaryDirectory(prefix="abstractclassroom-content-") as temporary:
        work = Path(temporary)
        content = work / "files"
        content.mkdir()
        manifest = collect_content(root, content)
        manifest_path = work / "manifest.json"
        manifest_path.write_bytes(manifest)
        response = call_api({"action": "sync", "manifestDigest": hashlib.sha256(manifest).hexdigest()})
        if not response.get("recognized"):
            raise ValueError("Link this repository to your course through the AbstractClassroom dashboard, then rerun this workflow.")
        uploads = response.get("uploads", [])
        if not uploads:
            raise ValueError("The server did not authorize a course upload.")
        for upload in uploads:
            if upload["status"] == "PUBLISHED":
                continue
            if upload["status"] != "UPLOADING":
                raise ValueError("This publication attempt is no longer current. Rerun the workflow.")
            credentials = upload["credentials"]
            for value in credentials.values():
                print("::add-mask::" + value, flush=True)
            environment = {**os.environ,
                "AWS_ACCESS_KEY_ID": credentials["accessKeyId"],
                "AWS_SECRET_ACCESS_KEY": credentials["secretAccessKey"],
                "AWS_SESSION_TOKEN": credentials["sessionToken"],
                "AWS_DEFAULT_REGION": upload["region"], "AWS_EC2_METADATA_DISABLED": "true",
            }
            destination = f"s3://{upload['bucket']}/{upload['prefix']}"
            subprocess.run(["aws", "s3", "sync", str(content) + "/", destination + "files/",
                "--no-follow-symlinks", "--only-show-errors", "--no-progress"], env=environment, check=True)
            # Upload last: this event triggers validation after all files arrived.
            subprocess.run(["aws", "s3", "cp", str(manifest_path), destination + "manifest.json",
                "--content-type", "application/json", "--only-show-errors", "--no-progress"], env=environment, check=True)
        deadline = time.monotonic() + 600
        pending = {upload["uploadId"] for upload in uploads if upload["status"] != "PUBLISHED"}
        while pending and time.monotonic() < deadline:
            time.sleep(10)
            for upload_id in list(pending):
                status = call_api({"action": "status", "uploadId": upload_id})
                if status["status"] == "PUBLISHED":
                    pending.remove(upload_id)
                elif status["status"] in {"FAILED", "SUPERSEDED"}:
                    raise ValueError("The publication was rejected or superseded: " + status.get("failureCode", "unknown"))
        if pending:
            raise ValueError("Publication verification timed out. Check the workflow and rerun it.")
        print("AbstractClassroom published the validated lesson content to S3.")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        raise SystemExit(f"AbstractClassroom sync request failed (HTTP {error.code}).") from None
    except (ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from None
