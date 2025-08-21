import os
import sys
import traceback
from datetime import datetime

sys.path.insert(0, "/work/function/packages")  # functionが依存するパッケージのパス

WORK_DIR = "/work"
INPUT_A_PATH = f"{WORK_DIR}/inputs/input_1"
INPUT_B_PATH = f"{WORK_DIR}/inputs/input_2"
OUTPUT_A_PATH = f"{WORK_DIR}/outputs/output_1"
OUTPUT_B_PATH = f"{WORK_DIR}/outputs/output_2"
DOWNLOAD_DIR = "downloads/"

THRESHOLD = 2  # 集計数がこの値未満の行は出力されない


def print_log(msg):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        with open(os.path.join(DOWNLOAD_DIR, "app.log"), "a") as log_file:
            log_file.write(f"[{current_time}]:[handler.py]: {msg}\n")
        os.makedirs(OUTPUT_A_PATH, exist_ok=True)
        with open(os.path.join(OUTPUT_A_PATH, "app.log"), "a") as log_file:
            log_file.write(f"[{current_time}]:[handler.py]: {msg}\n")
        os.makedirs(OUTPUT_B_PATH, exist_ok=True)
        with open(os.path.join(OUTPUT_B_PATH, "app.log"), "a") as log_file:
            log_file.write(f"[{current_time}]:[handler.py]: {msg}\n")
    except Exception:
        pass  # 出力ディレクトリへの書き込みに失敗しても続行


# メモリ使用量と実行時間を計測するための関数
def get_memory_usage():
    """現在のメモリ使用量を取得"""
    import psutil

    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # MB単位


def print_memory_usage(stage_name):
    """メモリ使用量を表示"""
    try:
        memory_mb = get_memory_usage()
        print_log(f"[{stage_name}] メモリ使用量: {memory_mb:.2f} MB")
    except Exception as e:
        print_log(f"Failed to get memory usage: {e.__class__.__name__}")
        return 0


def run():
    try:
        print_memory_usage("開始時")
        print_log("handler.run: Started.")

        import polars as pl

        print_log("handler.run: Imported successfully.")

        # 入力データを読み込む
        lf_a = pl.scan_csv(os.path.join(INPUT_A_PATH, "input_a.csv"))
        print_log("handler.run: Read input_a.csv successfully.")
        print_memory_usage("input_a.csv読み込み後")
        lf_b = pl.scan_csv(os.path.join(INPUT_B_PATH, "input_b.csv"))
        print_log("handler.run: Read input_b.csv successfully.")
        print_memory_usage("input_b.csv読み込み後")

        # キー列を特定
        key_a = lf_a.columns[0]
        key_b = lf_b.columns[0]

        # 2. Join前のリネーム処理
        # dataset_a の列名をリネーム (id以外)
        cols_to_rename_a = [col for col in lf_a.columns if col != key_a]
        rename_map_a = {col: f"0:{col}" for col in cols_to_rename_a}
        lf_a_renamed = lf_a.rename(rename_map_a)
        print_memory_usage("0_列名リネーム後")

        # dataset_b の列名をリネーム (id以外)
        cols_to_rename_b = [col for col in lf_b.columns if col != key_b]
        rename_map_b = {col: f"1:{col}" for col in cols_to_rename_b}
        lf_b_renamed = lf_b.rename(rename_map_b)
        print_memory_usage("1_列名リネーム後")
        print_log("handler.run: Renamed columns successfully.")

        # 3. リネーム済みのLazyFrameをJoin
        lf_joined = lf_a_renamed.join(
            lf_b_renamed, left_on=key_a, right_on=key_b, how="inner"
        )
        print_log("handler.run: Merged successfully with leftmost columns.")
        print_memory_usage("Join後")

        # 4. 全Attribute列でGroup By & Count
        # id以外の全ての列（a_...とb_...）をグループ化のキーに指定
        attribute_cols = [
            col for col in lf_joined.columns if col != key_a and col != key_b
        ]

        lf_summary = lf_joined.group_by(attribute_cols).agg(
            pl.count().alias("number_of_rows")
        )
        print_memory_usage("Group By & Count後")

        # 5. 列の整形
        # number_of_rows を先頭に持ってくる
        # 列名をソートしてから指定
        sorted_cols = ["number_of_rows"] + sorted(attribute_cols)
        lf_final = lf_summary.select(sorted_cols)

        filtered = lf_final.filter(pl.col("number_of_rows") >= THRESHOLD)
        print_log(f"handler.run: Filtered successfully with threshold {THRESHOLD}.")
        print_memory_usage("Filter後")

        # 計算を実行して結果を表示
        final_result = filtered.collect(streaming=True)
        print_memory_usage("Collect後")

        # CSV形式で出力
        try:
            os.makedirs(OUTPUT_A_PATH, exist_ok=True)
            os.makedirs(OUTPUT_B_PATH, exist_ok=True)

            final_result.write_csv(os.path.join(OUTPUT_A_PATH, "output.csv"))
            print_log("handler.run: Saved a's output.csv successfully.")
            print_memory_usage("a's output.csv保存後")
            final_result.write_csv(os.path.join(OUTPUT_B_PATH, "output.csv"))
            print_log("handler.run: Saved b's output.csv successfully.")
            print_memory_usage("b's output.csv保存後")
        except Exception as e:
            print_log(f"handler.run: Error saving results: {str(e)}")

        print_log("handler.run: DONE.")
        print_memory_usage("終了時")

    except BaseException as e:
        print_log(f"handler.run: ERROR: {str(e)}")
        try:
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            with open(os.path.join(DOWNLOAD_DIR, "error.log"), "w") as error_file:
                traceback.print_exc(file=error_file)
        except Exception:
            pass  # エラーログの書き込みに失敗しても続行
        raise e
