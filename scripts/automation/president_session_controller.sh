#!/bin/bash
# プレジデントセッション内で実行される自動化スクリプト

export TOKENIZERS_PARALLELISM=false
export PATH=/opt/homebrew/bin:$PATH

echo "👑 プレジデントセッション内自動化開始..."
cd /Users/dd/Desktop/1_dev/coding-rule2

echo "🚀 Claude Code起動..."
claude --dangerously-skip-permissions &
CLAUDE_PID=$!
sleep 8

echo "📋 プレジデント初期プロンプトセット中..."
echo "   ※ Claude Code起動待機→プロンプト自動送信→エンター実行"
PRESIDENT_PROMPT="あなたはプレジデントです。まずこのプロジェクトの性質・技術スタック・要件を詳細に分析してください。その後、プロジェクトに最適な組織構成を決定し、BOSS1、WORKER1、WORKER2、WORKER3に動的役職を配布してください。固定的な役職ではなく、プロジェクトに応じた最適な専門分野（例：UI/UX、データ分析、セキュリティ、DevOps等）を決定してください。各ワーカーへの指示後は必ずエンターキーを押して実行確認してください。"

echo "📤 プロンプト送信中..."
tmux send-keys -t president "$PRESIDENT_PROMPT"
sleep 2
echo "⚡ エンター実行中..."
tmux send-keys -t president C-m
sleep 3
echo "✅ プレジデントプロンプト実行完了"

echo "👥 ワーカーセッション作成..."
tmux new-session -d -s multiagent -c $(pwd)
sleep 1
tmux split-window -h -t multiagent
tmux split-window -v -t multiagent:0.0
tmux split-window -v -t multiagent:0.2
tmux select-layout -t multiagent tiled

echo "🎭 ワーカー役職配置..."
tmux select-pane -t multiagent:0.0 -T "👔 BOSS1"
tmux select-pane -t multiagent:0.1 -T "💻 WORKER1"
tmux select-pane -t multiagent:0.2 -T "🔧 WORKER2"
tmux select-pane -t multiagent:0.3 -T "🎨 WORKER3"

echo "🚀 ワーカー全員Claude Code一括起動..."
for i in 0 1 2 3; do 
    tmux send-keys -t multiagent:0.$i "export PATH=/opt/homebrew/bin:\$PATH && export TOKENIZERS_PARALLELISM=false && cd $(pwd)" C-m
done
sleep 2
for i in 0 1 2 3; do 
    tmux send-keys -t multiagent:0.$i "claude --dangerously-skip-permissions" C-m
done
sleep 12

echo "📋 ワーカー待機プロンプト送信中..."
echo "   ※ 各ワーカーに動的役職待機指示→プロンプト送信→エンター実行"

echo "📤 BOSS1プロンプト送信..."
tmux send-keys -t multiagent:0.0 "あなたはBOSS1です。プレジデントから動的に配布される役職と具体的タスクを待機してください。"
sleep 1
echo "⚡ BOSS1エンター実行..."
tmux send-keys -t multiagent:0.0 C-m
sleep 1

echo "📤 WORKER1プロンプト送信..."
tmux send-keys -t multiagent:0.1 "あなたはWORKER1です。プレジデントから動的に配布される役職と具体的タスクを待機してください。"
sleep 1
echo "⚡ WORKER1エンター実行..."
tmux send-keys -t multiagent:0.1 C-m
sleep 1

echo "📤 WORKER2プロンプト送信..."
tmux send-keys -t multiagent:0.2 "あなたはWORKER2です。プレジデントから動的に配布される役職と具体的タスクを待機してください。"
sleep 1
echo "⚡ WORKER2エンター実行..."
tmux send-keys -t multiagent:0.2 C-m
sleep 1

echo "📤 WORKER3プロンプト送信..."
tmux send-keys -t multiagent:0.3 "あなたはWORKER3です。プレジデントから動的に配布される役職と具体的タスクを待機してください。"
sleep 1
echo "⚡ WORKER3エンター実行..."
tmux send-keys -t multiagent:0.3 C-m
sleep 1

echo "✅ ワーカー全員プロンプト・エンター実行完了"

echo "🎨 ステータスバー適用..."
make statusbar-enforce 2>/dev/null || true

echo "👑 プレジデント最終指示セット中..."
echo "   ※ 役職配布促進プロンプト送信→エンター実行"
FINAL_PROMPT="プロジェクト分析完了後、各ワーカー（BOSS1、WORKER1、WORKER2、WORKER3）に具体的な動的役職と初期タスクを配布してください。指示後は必ずエンターキーを押して実行確認してください。"
echo "📤 最終指示送信中..."
tmux send-keys -t president "$FINAL_PROMPT"
sleep 2
echo "⚡ エンター実行中..."
tmux send-keys -t president C-m
sleep 3
echo "✅ プレジデント最終指示実行完了"

echo "🔗 President-Worker Bridge起動..."
echo "   ※ プレジデントの指示を自動的にワーカーに転送します"
python3 $(pwd)/scripts/automation/president_worker_bridge.py start &
BRIDGE_PID=$!
sleep 2

echo "✅ AI組織システム起動完了！"
echo "📊 稼働中システム:"
echo "   👑 プレジデント: Claude Code (PID: $CLAUDE_PID)"
echo "   🔗 指示転送ブリッジ: Python監視システム (PID: $BRIDGE_PID)"
echo "   👥 ワーカー4名: Claude Code待機中"
echo ""
echo "🎯 プレジデントの指示は自動的にワーカーに転送されます"

# プロセス監視
wait $CLAUDE_PID