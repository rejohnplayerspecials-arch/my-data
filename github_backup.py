#!/usr/bin/env python3
"""
Cowork Backup Script
CoworkBackup フォルダ内のファイルを GitHub の my-data リポジトリへ自動バックアップします。
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

  def get_file_sha(headers, owner, repo, path):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
                  return res.json().get("sha")
              return None

def upload_file(headers, owner, repo, filepath, backup_folder):
      rel_path = os.path.relpath(filepath, backup_folder).replace("\\", "/")
    if rel_path in [".github_backup_config.json", "github_backup.py"]:
              return None
          with open(filepath, "rb") as f:
                    content = base64.b64encode(f.read()).decode("utf-8")
                sha = get_file_sha(headers, owner, repo, rel_path)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {"message": f"Daily backup: {rel_path} ({date_str})", "content": content}
    if sha:
              payload["sha"] = sha
          url = f"https://api.github.com/repos/{owner}/{repo}/contents/{rel_path}"
    res = requests.put(url, headers=headers, json=payload)
    return res.status_code, rel_path

def main():
      config = load_config()
    token = config["github_token"]
    owner = config["repo_owner"]
    repo = config["repo_name"]
    backup_folder = config["backup_folder"]
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] バックアップ開始: {backup_folder}")
    uploaded = 0
    errors = 0
    for root, dirs, files in os.walk(backup_folder):
              dirs[:] = [d for d in dirs if not d.startswith(".")]
              for filename in files:
                            if filename.startswith("."):
                                              continue
                                          filepath = os.path.join(root, filename)
                            result = upload_file(headers, owner, repo, filepath, backup_folder)
                            if result is None:
                                              continue
                                          status, rel_path = result
                            if status in (200, 201):
                                              print(f"  OK {rel_path}")
                                              uploaded += 1
else:
                print(f"  NG {rel_path} (status: {status})")
                  errors += 1
    print(f"\n完了: {uploaded} ファイルをバックアップ、{errors} エラー")

if __name__ == "__main__":
      main()
