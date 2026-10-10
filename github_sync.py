#!/usr/bin/env python3
"""
GitHub Sync Script (ダウンロード)
GitHub の my-data リポジトリから C:/Users/Owner/Documents/CoworkBackup へ
最新ファイルを同期（ダウンロード）します。
別PCで最新データを受け取るときに使います。
"""

import os
import json
import base64
import requests
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), ".github_backup_config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def list_repo_files(headers, owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return []
    items = res.json()
    files = []
    for item in items:
        if item["type"] == "file":
            files.append(item)
        elif item["type"] == "dir":
            files.extend(list_repo_files(headers, owner, repo, item["path"]))
    return files

def download_file(headers, file_info, backup_folder):
    # README.md はスキップ
    if file_info["name"] == "README.md" and file_info["path"] == "README.md":
        return None

    res = requests.get(file_info["download_url"], headers=headers)
    if res.status_code != 200:
        return False, file_info["path"]

    local_path = os.path.join(backup_folder, file_info["path"].replace("/", os.sep))
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with open(local_path, "wb") as f:
        f.write(res.content)
    return True, file_info["path"]

def main():
    config = load_config()
    token = config["github_token"]
    owner = config["repo_owner"]
    repo = config["repo_name"]
    backup_folder = config["backup_folder"]

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GitHub から同期開始")
    print(f"  リポジトリ: {owner}/{repo}")
    print(f"  保存先: {backup_folder}")

    files = list_repo_files(headers, owner, repo)

    if not files:
        print("リポジトリにファイルが見つかりませんでした。")
        return

    downloaded = 0
    skipped = 0
    errors = 0

    for file_info in files:
        # 設定ファイルとスクリプトはダウンロードしない
        if file_info["name"] in [".github_backup_config.json", "github_backup.py", "github_sync.py"]:
            skipped += 1
            continue

        result = download_file(headers, file_info, backup_folder)
        if result is None:
            skipped += 1
            continue
        success, path = result
        if success:
            print(f"  ✓ {path}")
            downloaded += 1
        else:
            print(f"  ✗ {path}")
            errors += 1

    print(f"\n完了: {downloaded} ファイルをダウンロード、{skipped} スキップ、{errors} エラー")

if __name__ == "__main__":
    main()
