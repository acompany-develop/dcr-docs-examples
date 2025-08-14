import csv
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


def print_log(msg):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        os.makedirs(OUTPUT_A_PATH, exist_ok=True)
        with open(os.path.join(OUTPUT_A_PATH, "app.log"), "a") as log_file:
            log_file.write(f"[{current_time}]:[handler.py]: {msg}\n")
    except Exception:
        pass  # 出力ディレクトリへの書き込みに失敗しても続行


def run():
    try:
        import easyocr

        print_log("handler.run: Started.")

        # OCRモデル（文字検出/文字認識）を呼び出し
        reader = easyocr.Reader(
            ["en", "ja"],
            gpu=False,
            model_storage_directory=os.path.join(INPUT_A_PATH, "model"),
        )

        # OCRを実行
        results = reader.readtext(os.path.join(INPUT_B_PATH, "input_b.jpg"))
        # OCRの結果をcsvとして保存
        with open(os.path.join(OUTPUT_A_PATH, "output.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(["BoundingBox", "DetectedText", "ConfidenceLevel"])
            for result in results:
                writer.writerow([result[0], result[1], round(float(result[2]), 2)])

        print_log("handler.run: DONE.")
    except BaseException as e:
        print_log(f"handler.run: ERROR: {str(e)}")
        try:
            os.makedirs(OUTPUT_A_PATH, exist_ok=True)
            with open(os.path.join(OUTPUT_A_PATH, "error.log"), "w") as error_file:
                traceback.print_exc(file=error_file)
        except Exception:
            pass  # エラーログの書き込みに失敗しても続行
        raise e
