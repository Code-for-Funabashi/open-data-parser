# open data parser
船橋市のオープンデータを取得するコードを管理するレポジトリです。

## Install
```bash
poetry install
```

## Usage
```bash
# GOOGLE_API_KEYを環境変数に設定する
export GOOGLE_API_KEY="Your GOOGLE API KEY"
# open_data_parser/main.pyファイル内のTARGET変数を設定し、下記のコマンドを実行する
poetry run python open_data_parser/main.py
```

## Requirement
- Python 3.8 ~
- poetry 1.0 ~


1. geocodeディレクトリ:
    - 子育てマップ（https://github.com/Code-for-Funabashi/kosodate-map/）開発に利用する施設データのスクレープ、整形コード
    - https://www.city.funabashi.lg.jp/funakkonavi/map/11/index.html からデータを取得しております。

    - projects
        - PJTで利用するデータを格納するディレクトリ
        - /kosodate-map(このPJT用のデータだけgitに上げています)
    
    - utils.py
        - データ整形に利用出来そうな汎用的な関数をまとめておく
    - csv2json.py
        - 暫定的に用意したcsvファイル（projects/kosodate-map/配下にある）をtsで扱いやすい・拡張可能な形でjson形式に変換する
        - `python Scrape-OpenData/geodata/csv2json.py`で実行