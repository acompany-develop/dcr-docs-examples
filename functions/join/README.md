# Join Function

## 概要

Join Functionは、2つのCSVファイルを結合する関数です。両方のデータフレームの最左列をキーとして使用し、内部結合（INNER JOIN）を実行します。

## 機能

- **データ結合**: 2つのCSVファイルを最左列をキーとして結合
- **重複キー削除**: 結合後の重複したキー列を自動削除
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
- **内容**: 結合されたデータ（重複キー列は削除済み）

### output_2.csv (user2専用出力データ)
- **パス**: `/work/outputs/output_2/output_2.csv`
- **形式**: CSVファイル
- **内容**: 結合されたデータ（重複キー列は削除済み）

### ログファイル
- **app.log**: 処理ログ（`/work/outputs/output_1/app.log`、`/work/outputs/output_2/app.log`）

## アルゴリズム

1. **データ読み込み**
   - `input_1.csv`を読み込み
   - `input_2.csv`を読み込み

2. **キー抽出**
   - 両データフレームの最左列を結合キーとして抽出

3. **データ結合**
   - `pandas.merge()`を使用して内部結合を実行
   - `left_on`: input_1の最左列
   - `right_on`: input_2の最左列

4. **重複キー削除**
   - 結合後の重複したキー列を削除

5. **結果保存**
   - 結合結果を両方の出力ディレクトリに保存

## 使用例

### 入力ファイル例

**input_1.csv**:
```csv
id,name,age
1,Alice,25
2,Bob,30
3,Charlie,35
```

**input_2.csv**:
```csv
id,city,salary
1,Tokyo,50000
2,Osaka,60000
4,Kyoto,45000
```

### 出力ファイル例

**output_1.csv・output_2.csv** (user1・user2用):
```csv
name,age,city,salary
Alice,25,Tokyo,50000
Bob,30,Osaka,60000
```
