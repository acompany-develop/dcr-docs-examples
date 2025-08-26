# Cross Table Function

## 概要

Cross Table Functionは、2つのCSVファイルを結合し、クロス集計表を作成する関数です。両方のデータフレームの最左列をキーとして使用し、内部結合（INNER JOIN）を実行した後、属性列の組み合わせごとに集計を行います。Polarsライブラリを使用して高速なデータ処理を実現します。

## 機能

- **データ結合**: 2つのCSVファイルを最左列をキーとして結合
- **クロス集計**: 属性列の組み合わせごとに件数を集計
- **閾値フィルタリング**: 集計数が閾値未満の行を除外
- **ログ出力**: 処理経過とエラー情報をログファイルに記録
- **処理結果**: 結果をcsvファイルに格納して返す

## 入力データ

### input_1.csv (user1専用入力データ)
- **パス**: `/work/inputs/input_1/input_1.csv`
- **形式**: CSVファイル
- **要件**: 最左列が結合キーとして使用される

### input_2.csv (user2専用入力データ)
- **パス**: `/work/inputs/input_2/input_2.csv`
- **形式**: CSVファイル
- **要件**: 最左列が結合キーとして使用される

## 出力データ

### output_1.csv (user1専用出力データ)
- **パス**: `/work/outputs/output_1/output_1.csv`
- **形式**: CSVファイル
- **内容**: クロス集計結果（number_of_rows列が先頭、属性列がソート済み）

### output_2.csv (user2専用出力データ)
- **パス**: `/work/outputs/output_2/output_2.csv`
- **形式**: CSVファイル
- **内容**: クロス集計結果（number_of_rows列が先頭、属性列がソート済み）

### ログファイル
- **app.log**: 処理ログ（`/work/outputs/output_1/app.log`、`/work/outputs/output_2/app.log`）

## アルゴリズム

1. **データ読み込み**
   - `input_1.csv`をLazyFrameとして読み込み
   - `input_2.csv`をLazyFrameとして読み込み

2. **キー抽出**
   - 両データフレームの最左列を結合キーとして抽出

3. **データ結合**
   - `polars.join()`を使用して内部結合を実行
   - `left_on`: input_1の最左列
   - `right_on`: input_2の最左列

4. **クロス集計**
   - 属性列（キー列以外）でグループ化
   - 各組み合わせの件数を集計

5. **閾値フィルタリング**
   - 集計数が閾値（THRESHOLD=2）未満の行を除外

6. **列順序整理**
   - `number_of_rows`列を先頭に配置
   - 属性列をアルファベット順にソート

7. **結果保存**
   - クロス集計結果を両方の出力ディレクトリに保存

## 使用例

### 入力ファイル例

**input_1.csv**:
```csv
id,age,gender
1,25,F
2,30,M
3,35,M
4,28,F
5,25,F
6,30,M
```

**input_2.csv**:
```csv
id,city,department
1,Tokyo,Sales
2,Osaka,Marketing
3,Tokyo,Engineering
4,Kyoto,HR
5,Tokyo,Sales
6,Osaka,Marketing
```

### 出力ファイル例

**output_1.csv・output_2.csv** (user1用・user2用):
```csv
number_of_rows,age,gender,city,department
2,25,F,Tokyo,Sales
2,30,M,Osaka,Marketing
```

## 設定パラメータ

- **THRESHOLD**: 集計数がこの値未満の行は出力されない（デフォルト: 2）

