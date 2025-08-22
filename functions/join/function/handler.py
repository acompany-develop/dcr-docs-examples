import os
import sys
import traceback
from datetime import datetime

# 依存ライブラリがある場合は、packagesディレクトリをパスに追加
sys.path.append("/work/function/packages")

import pandas as pd

# 作業ディレクトリとI/Oディレクトリのパス設定
WORK_DIR = "/work"
INPUT_DIR = f"{WORK_DIR}/inputs"
OUTPUT_DIR = f"{WORK_DIR}/outputs"
INPUT_1_DIR = f"{INPUT_DIR}/input_1"
INPUT_2_DIR = f"{INPUT_DIR}/input_2"
OUTPUT_1_DIR = f"{OUTPUT_DIR}/output_1"
OUTPUT_2_DIR = f"{OUTPUT_DIR}/output_2"


def print_log(msg: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for path in [OUTPUT_1_DIR, OUTPUT_2_DIR]:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "app.log"), "a") as log_file:
            log_file.write(f"{current_time}:{msg}\n")


def join_data(input_1_path: str, input_2_path: str) -> pd.DataFrame:
    print_log("join_data: Started.")
    df_1 = pd.read_csv(input_1_path)
    df_2 = pd.read_csv(input_2_path)
    key_a = df_1.columns[0]
    key_b = df_2.columns[0]
    df_joined = pd.merge(df_1, df_2, left_on=key_a, right_on=key_b)
    # 重複キーを削除
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
