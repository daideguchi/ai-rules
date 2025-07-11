#!/bin/bash
# 新プロジェクト用クイックセットアップスクリプト
# Quick Project Setup Script for New Projects

set -e

echo "🚀 coding-rule2 テンプレート クイックセットアップ"
echo "================================================="
echo ""

# 元のcoding-rule2プロジェクトではないかチェック
if [[ "$(basename "$(pwd)")" == "coding-rule2" ]] && [[ -f "CLAUDE.md" ]] && grep -q "AI Safety Governance" README.md 2>/dev/null; then
    echo "❌ 元のcoding-rule2プロジェクトで実行しようとしています！"
    echo "💡 このスクリプトは新プロジェクト用です。"
    echo "💡 まずこのテンプレートを新しいディレクトリにコピーしてください。"
    echo ""
    echo "🔧 正しい手順:"
    echo "  1. git clone https://github.com/daideguchi/ai-rules.git 新プロジェクト名"
    echo "  2. cd 新プロジェクト名"
    echo "  3. bash scripts/setup/quick_project_setup.sh"
    exit 1
fi

echo "📋 ステップ 1: プロジェクト情報入力"
echo "--------------------------------"
read -p "🏷️  プロジェクト名を入力してください: " PROJECT_NAME
if [[ -z "$PROJECT_NAME" ]]; then
    echo "❌ プロジェクト名は必須です！"
    exit 1
fi

echo ""
echo "📂 ステップ 2: プロジェクトタイプ選択"
echo "------------------------------"
echo "1) 🌐 Webプロジェクト (React/Vue/Angular)"
echo "2) 🐍 Pythonライブラリ/パッケージ"
echo "3) 🤖 AI/MLプロジェクト"
echo "4) ⚙️  カスタムプロジェクト"
echo ""
read -p "プロジェクトタイプを選択してください (1-4): " PROJECT_TYPE

case $PROJECT_TYPE in
    1) TYPE_NAME="web" ;;
    2) TYPE_NAME="python" ;;
    3) TYPE_NAME="ai-project" ;;
    4) TYPE_NAME="custom" ;;
    *) echo "❌ 無効な選択です！"; exit 1 ;;
esac

echo ""
echo "🔧 ステップ 3: プロジェクト初期化"
echo "-----------------------------"
echo "プロジェクト '$PROJECT_NAME' を $TYPE_NAME プロジェクトとして初期化中..."

# プロジェクト初期化の実行
if python3 scripts/setup/initialize_new_project.py "$PROJECT_NAME" --type "$TYPE_NAME"; then
    echo "✅ プロジェクト初期化が完了しました！"
else
    echo "❌ プロジェクト初期化に失敗しました！"
    echo "🔧 手動で以下のコマンドをお試しください:"
    echo "   make init-${TYPE_NAME}-project"
    exit 1
fi

echo ""
echo "🔑 ステップ 4: APIキーセットアップ（オプション）"
echo "---------------------------------------------"
if [[ "$TYPE_NAME" == "ai-project" ]]; then
    echo "📝 AIプロジェクトのため、APIキーセットアップを推奨します"
    read -p "APIキーを今すぐセットアップしますか？ (y/N): " SETUP_APIS
else
    read -p "APIキーをセットアップしますか？ (y/N): " SETUP_APIS
fi

if [[ "$SETUP_APIS" =~ ^[YyｙYes]$ ]]; then
    echo "APIキーをセットアップ中..."
    if python3 scripts/setup/quick_api_setup.py 2>/dev/null; then
        echo "✅ APIキーセットアップが完了しました"
    else
        echo "⚠️  APIキーセットアップでエラーが発生しました"
        echo "💡 後で以下のコマンドで設定できます: make api-setup"
    fi
else
    echo "⏭️  APIキーセットアップをスキップしました"
    if [[ "$TYPE_NAME" == "ai-project" ]]; then
        echo "💡 後で以下のコマンドで設定できます: make mcp-setup"
    fi
fi

echo ""
echo "📦 ステップ 5: 依存関係インストール"
echo "-------------------------------"

# Python環境チェック
if command -v python3 >/dev/null 2>&1; then
    if [[ -f "requirements.txt" ]]; then
        read -p "Python依存関係をインストールしますか？ (y/N): " INSTALL_PYTHON_DEPS
        if [[ "$INSTALL_PYTHON_DEPS" =~ ^[YyｙYes]$ ]]; then
            if command -v pip3 >/dev/null 2>&1; then
                echo "Python依存関係をインストール中..."
                pip3 install -r requirements.txt || echo "⚠️  依存関係は後で手動でインストールしてください: pip3 install -r requirements.txt"
            elif command -v pip >/dev/null 2>&1; then
                echo "Python依存関係をインストール中..."
                pip install -r requirements.txt || echo "⚠️  依存関係は後で手動でインストールしてください: pip install -r requirements.txt"
            else
                echo "⚠️  pipが見つかりません。後で手動でインストールしてください: pip install -r requirements.txt"
            fi
        fi
    fi
elif [[ -f "package.json" ]]; then
    if command -v npm >/dev/null 2>&1; then
        read -p "Node.js依存関係をインストールしますか？ (y/N): " INSTALL_NODE_DEPS
        if [[ "$INSTALL_NODE_DEPS" =~ ^[YyｙYes]$ ]]; then
            echo "Node.js依存関係をインストール中..."
            npm install || echo "⚠️  依存関係は後で手動でインストールしてください: npm install"
        fi
    else
        echo "⚠️  npmが見つかりません。Node.jsをインストールしてから npm install を実行してください"
    fi
fi

echo ""
echo "🎯 ステップ 6: セットアップ検証"
echo "----------------------"
echo "ファイル整理システムをチェック中..."

# makeコマンドがあるかチェック
if command -v make >/dev/null 2>&1; then
    make check-file-organization 2>/dev/null || {
        echo "⚠️  ファイル整理の問題が検出されました - 詳細は上記をご確認ください"
        echo "🔧 修正方法: make enforce-file-organization"
    }
else
    echo "⚠️  makeコマンドが見つかりません。ファイル整理の確認をスキップします"
    echo "💡 makeをインストールしてから以下をお試しください:"
    echo "   make check-file-organization"
fi

echo ""
echo "🎉 セットアップ完了！"
echo "=================="
echo ""
echo "📋 プロジェクト '$PROJECT_NAME' の準備が整いました！"
echo ""
echo "🔧 利用可能コマンド:"
echo "  make check-file-organization  - ファイル整理確認"
echo "  make enforce-file-organization - ファイル整理修正"
if [[ "$TYPE_NAME" == "ai-project" ]]; then
    echo "  make mcp-setup               - MCP統合セットアップ"
fi
echo "  make api-setup               - APIキーセットアップ"
echo "  make help                    - 全コマンド表示"
echo ""
echo "📖 ドキュメント:"
echo "  docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md - ファイル整理ルール"
if [[ "$TYPE_NAME" == "ai-project" ]]; then
    echo "  CLAUDE.md                    - AI設定"
fi
echo "  docs/TEMPLATE_USAGE.md       - 完全使用ガイド"
echo ""
echo "🚀 次のステップ:"
echo "  1. docs/でプロジェクト構造を確認"
echo "  2. 必要に応じてファイル整理ルールをカスタマイズ"
if [[ "$TYPE_NAME" == "ai-project" ]] && [[ "$SETUP_APIS" != [YyｙYes] ]]; then
    echo "  3. AIプロジェクト用のAPIキーセットアップ: make mcp-setup"
    echo "  4. プロジェクト開発を開始！"
else
    echo "  3. プロジェクト開発を開始！"
fi
echo ""
echo "✨ 楽しい開発を！"