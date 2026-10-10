# 別PCでのセットアップ手順

このフォルダを複数のPCで同期するための手順です。

---

## 手順1：フォルダを作成する

別PCのドキュメントフォルダに `CoworkBackup` フォルダを作成します。
例：`C:\Users\[ユーザー名]\Documents\CoworkBackup`

---

## 手順2：スクリプトファイルをコピーする

以下の3ファイルをこのPCの `CoworkBackup` フォルダからコピーしてください：

- `github_backup.py`（GitHubへのアップロード）
- `github_sync.py`（GitHubからのダウンロード）
- `.github_backup_config.json`（認証情報・設定）

> `.github_backup_config.json` は隠しファイルのため、エクスプローラーで「隠しファイルを表示する」設定が必要な場合があります。

---

## 手順3：設定ファイルを編集する

別PCにコピーした `.github_backup_config.json` を開いて、`backup_folder` のパスを別PCのパスに変更します：

```json
{
  "github_token": "（変更不要）",
  "repo_owner": "RejohnPlayerSpecials-Arch",
  "repo_name": "my-data",
  "backup_folder": "C:\\Users\\[別PCのユーザー名]\\Documents\\CoworkBackup"
}
```

---

## 手順4：Cowork でスケジュールを設定する

別PCの Cowork を開いて Claude に以下のように伝えてください：

> 「`C:\Users\[ユーザー名]\Documents\CoworkBackup` フォルダを毎日GitHubにバックアップして。また、朝9時にGitHubから同期するスケジュールも設定して」

---

## 同期の流れ

```
PC-A (このPC)          GitHub             PC-B (別PC)
  │                      │                   │
  │ 毎夜9時 アップロード →│                   │
  │                      │← ダウンロード 毎朝9時
  │                      │                   │
```

- **PC-A** で作ったファイルが夜9時にGitHubへ保存される
- **PC-B** で朝9時にGitHubから最新ファイルを取得できる
- 逆方向も同様に設定すれば完全な双方向同期になります

---

## トラブルシューティング

**スクリプトが動かない場合**
1. Python がインストールされているか確認：`python --version`
2. requests ライブラリをインストール：`pip install requests`

**ファイルが同期されない場合**
- `.github_backup_config.json` の `backup_folder` パスが正しいか確認
- GitHub トークンの有効期限を確認（有効期限なしに設定済みのため通常は不要）
