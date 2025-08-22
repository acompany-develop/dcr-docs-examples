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

import pandas as pd


def print_log(msg: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for path in [OUTPUT_1_DIR, OUTPUT_2_DIR]:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "app.log"), "a") as log_file:
            log_file.write(f"{current_time}:{msg}\n")


def join_data(input_1_path: str, input_2_path: str) -> pd.DataFrame:
    print_log("join_data: Started.")
    
    # 入力CSVファイルを読み込み
    df_1 = pd.read_csv(input_1_path)
    df_2 = pd.read_csv(input_2_path)
    
    # 両データフレームの最左列を結合キーとして取得
    key_a = df_1.columns[0]  # 1つ目のファイルの最左列
    key_b = df_2.columns[0]  # 2つ目のファイルの最左列
    
    # 内部結合を実行（両方のファイルに存在するキーのみ）
    df_joined = pd.merge(df_1, df_2, left_on=key_a, right_on=key_b)
    
    # 重複したキー列を削除（結合後のデータフレームには同じ値の列が2つ存在するため）
    df_joined = df_joined.drop(columns=[key_a, key_b])
    
    print_log("join_data: Completed.")
    return df_joined


def run():
    try:
        print_log("run: Started.")

        df_joined = join_data(
            f"{INPUT_1_DIR}/input_a.csv", f"{INPUT_2_DIR}/input_b.csv"
        )
        print_log("run: Joined data.")

        df_joined.to_csv(f"{OUTPUT_1_DIR}/output_a.csv", index=False)
        print_log("run: Saved output_a.csv.")

        df_joined.to_csv(f"{OUTPUT_2_DIR}/output_b.csv", index=False)
        print_log("run: Saved output_b.csv.")

        print_log("run: Completed.")
    except BaseException as e:
        print_log(f"error type: {type(e).__name__}")

        tb = traceback.extract_tb(e.__traceback__)
        if tb:
            for i, frame in enumerate(tb):
                print_log(f"error location {i + 1}: {frame.filename}:{frame.lineno}")
