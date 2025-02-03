# セットアップガイド

## 必要要件
- Python 3.11以上
- Poetry（Pythonパッケージマネージャー）

## インストール手順
### 1. リポジトリのクローン
```shell
git clone https://github.com/ruis2615/ImageDownloader.git
cd ImageDownloader
```

### 2. Poetry環境のセットアップ
```shell
poetry install
```
これにより、以下の依存関係がインストールされます（pyproject.toml参照）
- beautifulsoup4
- python-dotenv
- requests

### 3. 環境変数の設定
`.env.sample`を同じディレクトリにコピーし、ファイル名を`.env`に変更後、以下の内容を設定してください。
```env
SAVE_DIR=/path/to/your/dir
SAVE_LOG_FILE_NAME=customizeFileName

TARGET_URL=https://example.com/abcd
PAGE_QUERY=page

START_PAGE_NUMBER=0
STOP_PAGE_NUMBER=1

EXCLUDE_FILES=example.png,example_1.jpg
```
- `SAVE_DIR`：保存先のディレクトリ(末尾の`/`は不要)
- `SAVE_LOG_FILE_NAME`：ログファイルのファイル名(保存先のディレクトリは`SAVE_DIR`で指定したディレクトリ)
- `TARGET_URL`：一括保存したいサイトのURL
- `PAGE_QUERY`：ページクエリ(`https://example.com/abcd?page=1`の`page`に該当する部分)
- `START_PAGE_NUMBER`：処理を開始したいページ番号
- `STOP_PAGE_NUMBER`：処理を終了したいページ番号
- `EXCLUDE_FILES`：保存させたくないファイル名(カンマ区切り)

### 4. 実行方法
Poetry環境内でスクリプトを実行：
```shell
poetry run python main.py
```
## 注意事項
- poetry + pyenvの環境で構築しているため、その他の環境の場合は適宜コマンドを修正してください。

## ライセンス
MITライセンスの下で提供されています。詳細はLICENSEファイルを参照してください。