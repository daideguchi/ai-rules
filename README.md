# 🚀 coding-rule2: 万能プロジェクトテンプレート

**厳格なファイル整理 & AI統合機能付きの包括的プロジェクトテンプレート**

[![テンプレート準備完了](https://img.shields.io/badge/テンプレート-準備完了-brightgreen)](docs/TEMPLATE_USAGE.md)
[![ファイル整理](https://img.shields.io/badge/ファイル整理-自動化-blue)](docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md)
[![プロジェクトタイプ](https://img.shields.io/badge/プロジェクトタイプ-4種類対応-green)](scripts/setup/)
[![AI統合](https://img.shields.io/badge/AI統合-Claude%20%7C%20MCP-purple)](CLAUDE.md)
[![ワンコマンドセットアップ](https://img.shields.io/badge/セットアップ-ワンコマンド-orange)](scripts/setup/quick_project_setup.sh)

## 🎯 テンプレート概要

**coding-rule2**は、自動ファイル整理、AI統合、複数プロジェクトタイプ対応を備えた万能プロジェクトテンプレートです。このテンプレートをコピーして、ベストプラクティスが組み込まれた新しいプロジェクトを即座に開始できます。

### 🌟 主要機能

- **📁 厳格なファイル整理**: 12-20ファイルのルート制限による自動強制
- **🚀 ワンコマンドセットアップ**: `bash scripts/setup/quick_project_setup.sh`
- **🎯 複数プロジェクトタイプ**: Web、Python、AI/ML、カスタムプロジェクト
- **🤖 AI統合**: Claude Code、MCP、o3サポート内蔵
- **⚡ プリコミットフック**: 自動ファイル整理強制
- **🔧 テンプレートカスタマイズ**: プロジェクトタイプに自動適応

## 🚀 新プロジェクト用クイックスタート

### 1. テンプレートをコピー
```bash
# coding-rule2をクローンまたはダウンロード
git clone https://github.com/daideguchi/ai-rules.git my-new-project
cd my-new-project

# 元のgit履歴を削除（オプション）
rm -rf .git
git init
```

### 2. インタラクティブセットアップ
```bash
# インタラクティブなセットアップ（推奨）
bash scripts/setup/quick_project_setup.sh
```

### 3. 手動プロジェクトタイプセットアップ
```bash
make init-web-project      # Webプロジェクト用（React/Vue/Angular）
make init-python-project   # Pythonライブラリ/パッケージ用
make init-ai-project       # AI/MLプロジェクト用
make init-custom-project   # カスタムプロジェクト用
```

## 📁 対応プロジェクトタイプ

| タイプ | ルートファイル制限 | 主要機能 |
|------|-----------------|----------|
| **🌐 Web** | 15ファイル | React/Vue/Angular、Node.js、npmサポート |
| **🐍 Python** | 12ファイル | pip、setuptools、pytest統合 |
| **🤖 AI/ML** | 12ファイル | Claude Code、MCP、AI組織 |
| **⚙️ カスタム** | 20ファイル | 柔軟な構造、カスタマイズ可能 |

## 🔒 ファイル整理システム

### 自動強制機能
- **ルートディレクトリ制限**: 最大12-20ファイル（プロジェクトタイプにより変動）
- **プリコミットフック**: ルール違反時のコミット防止
- **自動配置**: ファイルを適切なディレクトリに移動
- **リアルタイム検証**: `make check-file-organization`

### フォルダ構造
```
PROJECT_ROOT/
├── .cursor/          # Cursor エディタワークスペース（ルートに配置）
├── config/           # 設定ファイル
├── docs/             # ドキュメント
├── scripts/          # 実行可能スクリプト
├── src/              # ソースコード
├── tests/            # テストファイル
└── [プロジェクト固有フォルダ]
```

## 🔧 利用可能コマンド

### ファイル整理
```bash
make check-file-organization   # コンプライアンス状況確認
make enforce-file-organization # コンプライアンス強制実行
make root-audit               # ファイル数クイックチェック
make dry-run-organization     # 変更のプレビュー
```

### プロジェクトセットアップ
```bash
make mcp-setup     # MCP統合セットアップ
make api-setup     # APIキー設定
make install       # 依存関係インストール
make test          # テスト実行
```

### テンプレート管理
```bash
# このテンプレートを使用する新プロジェクト用
bash scripts/setup/quick_project_setup.sh  # インタラクティブセットアップ
```

## 🤖 AI統合機能

### Claude Code統合
- **CLAUDE.md**: AI動作設定
- **MCPサポート**: AI機能拡張のためのModel Context Protocol
- **メモリシステム**: セッション間での永続的AIメモリ

### サポートされるAIツール
- **Claude**: 高度なAIアシスタント統合
- **o3**: OpenAIの推論AIモデル
- **Gemini**: Google AIモデルサポート

### MCP クイックセットアップ
```bash
# 新プロジェクト用ワンコマンドMCPセットアップ
make mcp-setup

# MCP状況確認
make mcp-status
```

## 📋 テンプレート使用ガイド

完全なテンプレート使用方法については、**[テンプレート使用ガイド](docs/TEMPLATE_USAGE.md)**をご覧ください

### 主要ドキュメント
- **[テンプレート使用ガイド](docs/TEMPLATE_USAGE.md)** - 完全使用ガイド
- **[厳格ファイル整理ルール](docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md)** - ファイル整理ルール
- **[CLAUDE.md](CLAUDE.md)** - AI統合設定（AIプロジェクト用）

## 🛡️ 保護機能

### ファイル整理保護
- **プリコミットフック**: 自動ファイル整理強制
- **リアルタイム検証**: 継続的コンプライアンスチェック
- **自動配置**: ファイルを正しいディレクトリに移動
- **プロジェクト固有ルール**: 各プロジェクトタイプにカスタマイズ

### テンプレート保護
- **プロジェクト検出**: 特定プロジェクトにのみルール適用
- **テンプレート整合性**: 元のテンプレート構造保持
- **カスタマイズ可能ルール**: プロジェクトニーズに適応

## 🎉 成功事例

このテンプレートは以下に最適化されています：
- ✅ **自動メンテナンス付きクリーンプロジェクト構造**
- ✅ **ワンコマンドセットアップによる高速開発**
- ✅ **共有整理ルールによるチーム協働**
- ✅ **AI強化開発**（AIプロジェクト用）
- ✅ **初日から本番環境対応**の構造

### 検証済み機能
- ✅ **ファイル整理強制**: プリコミットフックによる違反防止
- ✅ **複数プロジェクトタイプサポート**: Web、Python、AI、カスタム
- ✅ **テンプレートカスタマイズ**: プロジェクトニーズへの自動適応
- ✅ **AI統合**: Claude Code、MCP、o3サポート
- ✅ **ワンコマンドセットアップ**: インタラクティブプロジェクト初期化

## 🎯 コマンドリファレンス

### 必須テンプレートコマンド
```bash
bash scripts/setup/quick_project_setup.sh  # インタラクティブプロジェクトセットアップ
make check-file-organization              # ファイル整理確認
make enforce-file-organization            # ファイル整理修正
make help                                 # 全コマンド表示
```

### プロジェクト初期化
```bash
make init-web-project      # Webプロジェクトとして初期化
make init-python-project   # Pythonプロジェクトとして初期化
make init-ai-project       # AIプロジェクトとして初期化
make init-custom-project   # カスタムプロジェクトとして初期化
```

### MCP & AI セットアップ（AIプロジェクト用）
```bash
make mcp-setup     # 完全MCPセットアップ
make api-setup     # APIキー設定
make mcp-status    # MCP状況確認
```

### 開発コマンド
```bash
make install       # 依存関係インストール
make test          # テスト実行
make setup-hooks   # gitフック設定
make lint          # コードリンティング実行
```

## 🔧 カスタマイズ

### プロジェクト構造（テンプレート）
```
coding-rule2/
├── .cursor/                   # Cursor エディタワークスペース（ルートに配置）
├── config/                    # 設定ファイル
├── docs/                      # ドキュメント
├── scripts/                   # 実行可能スクリプト
│   ├── automation/           # ファイル整理自動化
│   └── setup/               # プロジェクトセットアップスクリプト
├── src/                      # ソースコード
├── tests/                    # テストファイル
└── [ルート最大12ファイル]   # プリコミットフックによる強制
```

### プロジェクト用カスタマイズ

1. **テンプレートコピー**: coding-rule2を新しいプロジェクトディレクトリにクローン
2. **セットアップ実行**: `bash scripts/setup/quick_project_setup.sh`
3. **ルールカスタマイズ**: `scripts/automation/strict-file-organizer.py`を編集
4. **ドキュメント更新**: `docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md`を修正

### テンプレート機能
- **自動ファイル配置**: ファイルを正しいディレクトリに移動
- **プリコミットフック**: ルール違反時のコミット防止
- **プロジェクトタイプ検出**: ルールの自動適応
- **カスタマイズ可能制限**: プロジェクトタイプごとのファイル制限調整

## 📚 ドキュメント

### テンプレート使用
- **[テンプレート使用ガイド](docs/TEMPLATE_USAGE.md)** - 完全テンプレート使用ガイド
- **[厳格ファイル整理ルール](docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md)** - ファイル整理ルール

### AI統合（AIプロジェクト用）
- **[CLAUDE.md](CLAUDE.md)** - AI動作設定
- **[Index.md](Index.md)** - プロジェクト概要（AIプロジェクト）

### 開発
- **[開発ガイド](docs/02_guides/)** - 開発ガイド
- **[技術仕様](docs/04_reference/)** - 技術仕様

## 🛡️ セキュリティ & ベストプラクティス

### ファイル整理セキュリティ
- **プリコミットフック**: 不正なファイル配置の防止
- **自動強制**: ルールの偶発的バイパス不可
- **テンプレート保護**: 元の構造保持

### APIキー管理（AIプロジェクト用）
- **環境変数**: `.env`ファイルでの保存（gitから除外）
- **MCP統合**: セキュアAPIキー処理
- **ハードコーディング禁止**: キーをリポジトリにコミットしない

### 推奨セットアップ
```bash
# APIキー設定（AIプロジェクト）
echo "OPENAI_API_KEY=your_key_here" > .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

## 🎉 このテンプレートの使用

このプロジェクトは万能テンプレートとして設計されています。あらゆる新プロジェクトでご利用ください：

1. **テンプレートコピー**: 新しいプロジェクトディレクトリにクローン
2. **セットアップ実行**: `bash scripts/setup/quick_project_setup.sh`
3. **カスタマイズ**: ファイル整理ルールをニーズに適応
4. **開発開始**: 初日からクリーンで整理された構造

### テンプレート自体への貢献

テンプレート自体を改善するには：
1. このリポジトリをフォーク
2. テンプレート機能の改善
3. 異なるプロジェクトタイプでテスト
4. プルリクエスト送信

## 📄 ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照

## 🔗 関連リンク

- **テンプレート使用ガイド**: [docs/TEMPLATE_USAGE.md](docs/TEMPLATE_USAGE.md)
- **ファイル整理ルール**: [docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md](docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md)
- **Claude Code統合**: [CLAUDE.md](CLAUDE.md)（AIプロジェクト）

---

**🚀 coding-rule2: 万能プロジェクトテンプレート**

**初日からクリーンで整理され、AI強化された開発** ✨