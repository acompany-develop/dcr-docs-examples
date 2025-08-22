import os
import sys
import traceback
from datetime import datetime

# 作業ディレクトリとI/Oディレクトリのパス設定
WORK_DIR = "/work"
INPUT_DIR = f"{WORK_DIR}/inputs"
OUTPUT_DIR = f"{WORK_DIR}/outputs"
INPUT_1_DIR = f"{INPUT_DIR}/input_1"
INPUT_2_DIR = f"{INPUT_DIR}/input_2"
OUTPUT_1_DIR = f"{OUTPUT_DIR}/output_1"
OUTPUT_2_DIR = f"{OUTPUT_DIR}/output_2"

# 依存ライブラリがある場合は、packagesディレクトリをパスに追加
sys.path.append(f"{WORK_DIR}/function/packages")

import polars as pl

THRESHOLD = 2  # 集計数がこの値未満の行は出力されない


def print_log(msg: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for path in [OUTPUT_1_DIR, OUTPUT_2_DIR]:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "app.log"), "a") as log_file:
            log_file.write(f"{current_time}:{msg}\n")


def cross_table_data(input_1_path: str, input_2_path: str):
    print_log("cross_table_data: Started.")

    # 入力データを読み込む（LazyFrameとして読み込み）
    lf_a = pl.scan_csv(input_1_path)
    lf_b = pl.scan_csv(input_2_path)

    # キー列を特定
    key_a = lf_a.columns[0]
    key_b = lf_b.columns[0]

    # 列名をリネーム
    cols_to_rename_a = [col for col in lf_a.columns if col != key_a]
    rename_map_a = {col: f"0:{col}" for col in cols_to_rename_a}
    lf_a_renamed = lf_a.rename(rename_map_a)

    cols_to_rename_b = [col for col in lf_b.columns if col != key_b]
    rename_map_b = {col: f"1:{col}" for col in cols_to_rename_b}
    lf_b_renamed = lf_b.rename(rename_map_b)

    # データを結合
    lf_joined = lf_a_renamed.join(
        lf_b_renamed, left_on=key_a, right_on=key_b, how="inner"
    )

    # 属性列を特定（キー列以外）
    attribute_cols = [col for col in lf_joined.columns if col != key_a and col != key_b]

    # グループ化して集計
    lf_summary = lf_joined.group_by(attribute_cols).agg(
        pl.count().alias("number_of_rows")
    )

    # 閾値でフィルタリング
    lf_filtered = lf_summary.filter(pl.col("number_of_rows") >= THRESHOLD)

    # 列の順序を整理（number_of_rowsを先頭に）
    sorted_cols = ["number_of_rows"] + sorted(attribute_cols)
    lf_final = lf_filtered.select(sorted_cols)

    # 計算を実行して結果を取得
    final_result = lf_final.collect(streaming=True)

    print_log("cross_table_data: Completed.")
    return final_result


def run():
    try:
        print_log("run: Started.")

        df_cross_table = cross_table_data(
            f"{INPUT_1_DIR}/input_a.csv", f"{INPUT_2_DIR}/input_b.csv"
        )
        print_log("run: Cross table data created.")

        # polarsのDataFrameを直接保存
        df_cross_table.write_csv(f"{OUTPUT_1_DIR}/output.csv")
        print_log("run: Saved output.csv to output_1.")

        df_cross_table.write_csv(f"{OUTPUT_2_DIR}/output.csv")
        print_log("run: Saved output.csv to output_2.")

        print_log("run: Completed.")
    except BaseException as e:
        print_log(f"error type: {type(e).__name__}")

        tb = traceback.extract_tb(e.__traceback__)
        if tb:
            for i, frame in enumerate(tb):
                print_log(f"error location {i + 1}: {frame.filename}:{frame.lineno}")
