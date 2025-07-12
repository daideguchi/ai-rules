# CLAUDE.md テンプレート - XMLタグ構造化プロンプト

## プロジェクト設定

<project_info>
- プロジェクト名: ${PROJECT_NAME}
- プロジェクトタイプ: ${PROJECT_TYPE}
- 主要言語: ${PRIMARY_LANGUAGE}
</project_info>

## AI動作ルール

<instructions>
あなたはこのプロジェクトの開発アシスタントです。
以下のルールに従って動作してください：

1. **コード品質**: 型安全性とテストカバレッジを重視
2. **セキュリティ**: APIキーや機密情報を絶対にハードコードしない
3. **パフォーマンス**: 効率的なアルゴリズムを選択
4. **可読性**: 明確な変数名とコメントを使用
</instructions>

## コンテキスト管理

<context_rules>
- セッション開始時: プロジェクト構造を確認
- タスク切り替え時: /clearでコンテキストリセット
- 長時間作業時: /compactで要約を作成
- エラー発生時: 詳細なログを残す
</context_rules>

## トークン管理

<token_management>
- 最大トークン: 8000/リクエスト
- 警告閾値: 6000トークン
- 自動圧縮: 7000トークン時点
- 重要コンテキスト: 常に保持
</token_management>

## タスクテンプレート

### 機能実装時
<task_template type="feature">
<requirements>
- 機能の詳細仕様
- 入力/出力の形式
- エラーハンドリング要件
</requirements>

<examples>
- 期待される動作例
- エッジケースの処理
</examples>

<constraints>
- パフォーマンス要件
- 互換性要件
</constraints>
</task_template>

### バグ修正時
<task_template type="bugfix">
<bug_info>
- エラーメッセージ
- 再現手順
- 期待される動作
</bug_info>

<investigation>
- 調査すべきファイル
- 確認すべきログ
</investigation>
</task_template>

## コマンドエイリアス

<commands>
- /analyze: コード分析と改善提案
- /optimize: パフォーマンス最適化
- /secure: セキュリティチェック
- /test: テストケース生成
- /document: ドキュメント生成
</commands>

## Git連携

<git_rules>
- コミット頻度: 機能単位で細かくコミット
- メッセージ形式: `<type>: <description>`
  - feat: 新機能
  - fix: バグ修正
  - refactor: リファクタリング
  - test: テスト追加
  - docs: ドキュメント更新
</git_rules>

## エラー処理

<error_handling>
- 即座に停止: Escキーで中断
- ロールバック: `claude "undo last action"`
- 詳細ログ: すべてのエラーを記録
</error_handling>

## MCP統合

<mcp_integration>
利用可能なMCPサーバー:
- github: GitHubリポジトリ操作
- puppeteer: Webスクレイピング
- context7: 最新ドキュメント取得
- o3: 高度な推論タスク
- database: データベース操作
</mcp_integration>