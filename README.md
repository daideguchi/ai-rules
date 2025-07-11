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
**🚀 Claude Code起動 + プロンプトセット + エンター処理 + 役職配置 = 完全自動完了**  
- 👑 プレジデント: Claude Code起動済み・プロンプト設定済み・エンター処理済み  
- 👥 4ワーカー: 全員Claude Code起動済み・役職配置済み・エンター処理済み  
- 🎨 ステータスバー: 配置完了  
- 📺 プレジデント画面に自動切り替え

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