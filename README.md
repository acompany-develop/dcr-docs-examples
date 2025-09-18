# DCR Documentation Examples

このリポジトリは、AutoPrivacy DCR（Data Clean Room）のチュートリアルとDCR上で実行する関数の実装例を提供します。

## 概要

AutoPrivacy DCRは、複数のテナント間で安全にデータを共有し、プライバシーを保護しながらデータ分析を実行するためのプラットフォームです。このリポジトリには、チュートリアルとDCR上で実行する関数の実装例が含まれています。

## プロジェクト構成

```
dcr-docs-examples/
├── functions/              # DCR上で実行可能な関数群
│   └── function_name/      # 各関数ディレクトリ
│       ├── function/       # 関数本体とパッケージ
│       ├── inputs/         # 入力データディレクトリ
│       └── outputs/        # 出力データディレクトリ
└── notebooks/              # Jupyter Notebookとドキュメント
    ├── img/               # 画像ファイル
    ├── mmd/               # Mermaidファイル
    └── tutorial/          # チュートリアル
```

## 利用可能な関数

`functions/`ディレクトリには、DCR上で実行可能な関数の実装例が含まれています。各関数の詳細については、対応するディレクトリ内のドキュメントを参照してください。

## チュートリアル

`notebooks/tutorial/basic_apc_cli_tutorial.ipynb` には、APC-CLIを使用してDCR上で関数を実行するための基本的なフローがJupyter Notebookとして含まれています。

## セットアップ

1. リポジトリをクローン：
   ```bash
   git clone https://github.com/acompany-develop/dcr-docs-examples.git
   cd dcr-docs-examples
   ```

2. チュートリアルを開始：
   `notebooks/tutorial/basic_apc_cli_tutorial.ipynb` を開いて、手順に従って実行してください。

## ドキュメント

詳細なドキュメントは以下を参照してください：
- [AutoPrivacy Cloud DCR ユーザーガイド](https://acompany-develop.github.io/autoprivacy-cloud/apc-dcr/)
- [APC-CLI リファレンス](https://acompany-develop.github.io/autoprivacy-cloud/apc-cli/)