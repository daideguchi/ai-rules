#!/bin/bash
# AI組織システム クイックセットアップ

set -e

echo "🚀 AI組織システム立ち上げ"
echo "========================="
echo ""
echo "🎯 AI組織を今すぐ立ち上げますか？"
echo ""
read -p "Enter を押してAI組織を開始 (Ctrl+C で中止): " 

echo ""
echo "🤖 AI組織システム起動中..."
echo ""

# make startupを実行
if make startup; then
    echo ""
    echo "🎉 AI組織立ち上げ完了！"
    echo "========================="
    echo ""
    echo "🤖 利用可能コマンド:"
    echo "  make ai-org-status    - AI組織状況確認"
    echo "  make ai-org-start     - ダッシュボード再起動"
    echo "  make declare-president - PRESIDENT宣言"
    echo ""
    echo "✨ AI組織が動作中です！"
else
    echo ""
    echo "❌ AI組織の立ち上げに失敗しました"
    echo ""
    echo "🔧 手動で以下をお試しください:"
    echo "  make declare-president"
    echo "  make ai-org-start"
fi