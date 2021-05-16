# open data parser
船橋市のオープンデータを取得し、加工する。

## Install
```bash
poetry install
```

## Requirement
- Python 3.8 or later
- poetry 1.0 or later
- GOOGLE_API_KEY
    - GCPのgeocoding APIの利用が許可されたAPIキー

## Usage
```bash
# GOOGLE_API_KEYを環境変数に設定する
export GOOGLE_API_KEY="Your GOOGLE API KEY"
# open_data_parser/main.pyファイル内のTARGET変数を設定し、下記のコマンドを実行する
poetry run python open_data_parser/main.py
```
