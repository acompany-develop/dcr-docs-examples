DCR上でEasyOCRの推論のみを行うfunction

# 注意点
- Graniteサーバーの実行環境と同じ環境で本functionを実行する必要がある (torchのCPUバージョンがクロスプラットフォームビルドができないため)
- EPCメモリは32GB用意する (easyocrの依存ライブラリの影響でfunction.zipのサイズが大きいため)

# EasyOCR e2eテスト実行前準備
`inputs/input_1/`配下に、recognition modelとdetection modelをそれぞれダウンロードするために、`{REPO_DIR}/src/tests/e2e_tests/client/apc_cli/testcases/easyocr`ディレクトリで以下のコマンドを実行する
```bash
TARGET_DIR="./inputs/input_1/model" && \
mkdir -p "$TARGET_DIR" && \
curl -L -o "$TARGET_DIR/japanese_g2.zip" https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/japanese_g2.zip && \
unzip "$TARGET_DIR/japanese_g2.zip" -d "$TARGET_DIR" && \
rm "$TARGET_DIR/japanese_g2.zip"

curl -L -o "$TARGET_DIR/craft_mlt_25k.zip" https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip && \
unzip "$TARGET_DIR/craft_mlt_25k.zip" -d "$TARGET_DIR" && \
rm "$TARGET_DIR/craft_mlt_25k.zip"
```
