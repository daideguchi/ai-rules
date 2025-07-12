# 🚀 coding-rule2: AI組織システム

**3ステップでAI組織を立ち上げ**

## ⚡ 3ステップ クイックスタート

### 1. インストール
```bash
git clone https://github.com/daideguchi/ai-rules.git
cd ai-rules
```

### 2. AI組織立ち上げ
```bash
make startup
```

### 3. 完了！
**🚀 動的役職システム搭載・一気通貫AI組織完全自動化**  
- 👑 プレジデント: プロジェクト分析・動的役職決定・Claude Code自動起動完了  
- 👥 4ワーカー: forループ一括起動・動的役職待機状態・自動送信完了  
- 🎨 ステータスバー: 薄いグレー背景で見やすく配置完了  
- 📺 プレジデント画面に自動切り替え・動的組織運営開始  
- 🔄 **役職はプロジェクトに応じて最適化されます**

---

## 📺 AI組織画面確認

```bash
tmux attach -t president    # プレジデント画面
tmux attach -t multiagent   # ワーカー4画面
```

### 🔴 重要：Claude Code認証
**初回起動時は自動でブラウザが起動して認証を行います**
- `make startup`実行時、認証が必要な場合は自動でブラウザが開きます
- ブラウザで認証完了後、AI組織が自動起動します

### 🔴 重要：プレジデント→ワーカー指示時の操作
**指示を入力した後、必ずエンターキーを押してください**  
エンターを押さないとワーカーに指示が届きません

## 🔧 高度な機能（オプション）

### 🤖 CI/CD統合
```bash
# .github/workflows/claude-ci.yml が自動で以下を実行:
- 型エラー自動修正（mypy）
- コードレビュー（PR時）
- テスト自動実行
```

### 📝 XMLタグ構造化
`templates/CLAUDE_TEMPLATE.md` でプロンプトを構造化:
- `<instructions>`: 明確な指示
- `<context>`: 背景情報
- `<requirements>`: 要件定義

### 🌐 MCPサーバー活用
`config/mcp-servers.json` で外部ツール統合:
- GitHub連携
- データベース接続
- 最新ドキュメント取得

### 💰 トークン管理
```bash
python scripts/monitoring/token_monitor.py --summary  # 使用量確認
```

---

**🎯 まずは `make startup` でAI組織を立ち上げてください！**