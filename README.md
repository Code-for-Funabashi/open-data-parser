# open data parser
船橋市のオープンデータを取得し、加工する。

## Install
```bash
poetry install
```

## Requirement
- Python 3.10 or later
- poetry 1.2 or later

[geocoding]: https://developers.google.com/maps/documentation/geocoding/overview

## Usage

1. 入力データを [input ディレクトリ](./input)に格納する

2. 入力データのメタ情報を[meta.yml](./input/meta.yml)に格納する

3. 以下のコマンドを実行する
```bash
poetry run python open_data_parser/main.py
```

## Testing
```bash
poetry run python -m unittest discover tests/open_data_parser/
```

## Data

### Input
入力するデータを `input/` 配下に格納する。  


### Output
open_data_parserで加工したデータは `/data` 配下に出力される。  
これは [kosodate-map](https://github.com/Code-for-Funabashi/kosodate-map) で利用するため、githubの管理対象としている。
