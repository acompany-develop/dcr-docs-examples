import os
import sys
import traceback
from datetime import datetime

"""
Note: External packages are supposed to be installed in function/packages.
"""
sys.path.insert(0, "/work/function/packages")  # functionが依存するパッケージのパス

WORK_DIR = "/work"  # functionが参照可能なディレクトリパス
INPUT_A_PATH = (
    f"{WORK_DIR}/inputs/input_1"  # acompany専用入力データ<input_a>のmount先パス
)
INPUT_B_PATH = (
    f"{WORK_DIR}/inputs/input_2"  # bcompany専用入力データ<input_b>のmount先パス
)
OUTPUT_A_PATH = (
    f"{WORK_DIR}/outputs/output_1"  # acompany専用出力データ<output_a>のmount先パス
)


def print_log(msg):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        os.makedirs(OUTPUT_A_PATH, exist_ok=True)
        with open(os.path.join(OUTPUT_A_PATH, "app.log"), "a") as log_file:
            log_file.write(f"[{current_time}]:[handler.py]: {msg}\n")
    except Exception:
        pass  # 出力ディレクトリへの書き込みに失敗しても続行


# メモリ使用量と実行時間を計測するための関数
def print_memory_usage():
    try:
        import psutil

        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        print_log(
            f"Current memory usage: {memory_info.rss / 1024**2:.2f} MB"
        )  # RSS: Resident Set Size (in MB)
        return memory_info.rss
    except Exception as e:
        print_log(f"Failed to get memory usage. {str(e)}")
        return 0


def run():
    try:
        import pandas as pd

        df_a = pd.read_csv(os.path.join(INPUT_A_PATH, "input_a.csv"))
        df_b = pd.read_csv(os.path.join(INPUT_B_PATH, "input_b.csv"))

        # Join on leftmost columns of both dataframes
        key_a = df_a.columns[0]
        key_b = df_b.columns[0]
        result = pd.merge(df_a, df_b, left_on=key_a, right_on=key_b)
        # Drop the redundant key
        result = result.drop(columns=[key_a, key_b])

        print_log("join result shape:" + str(result.shape))
        print_memory_usage()

        os.makedirs(OUTPUT_A_PATH, exist_ok=True)

        # 結果の保存
        result.to_csv(os.path.join(OUTPUT_A_PATH, "output.csv"), index=False)

    except BaseException as e:
        try:
            os.makedirs(OUTPUT_A_PATH, exist_ok=True)
            with open(os.path.join(OUTPUT_A_PATH, "error.log"), "w") as error_file:
                traceback.print_exc(file=error_file)
        except Exception:
            pass  # エラーログの書き込みに失敗しても続行
        raise e
