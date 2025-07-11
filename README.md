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
プレジデント〜ワーカーまで全て配置完了。AI組織が動作中。

---

## 📺 AI組織画面確認

```bash
tmux attach -t president  # プレジデント画面
tmux attach -t ai-org     # ワーカー4画面
```

## 📋 その他機能（オプション）

- **ファイル整理**: `make check-file-organization`
- **MCP設定**: `make mcp-setup`（後で設定可能）
- **API設定**: `make api-setup`（後で設定可能）

---

**🎯 まずは `make startup` でAI組織を立ち上げてください！**