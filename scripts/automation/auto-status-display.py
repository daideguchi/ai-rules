#!/usr/bin/env python3
"""
自動ステータス表示システム
プロジェクトルートに常に最新のタスク状況を表示
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class AutoStatusDisplay:
    """自動ステータス表示"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.status_file = self.project_root / "STATUS.md"
        self.progress_file = self.project_root / "PROGRESS.md"

    def generate_status_md(self) -> str:
        """STATUS.md生成"""
        # 各システムから状況収集
        commitments = self._get_commitments()
        kanban = self._get_kanban_status()
        todos = self._get_claude_todos()

        status_md = f"""# 📋 Current Project Status

**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🎯 Active Tasks

### GitHub Commitments
{self._format_commitments(commitments)}

### Kanban Board
{self._format_kanban(kanban)}

### Claude Code Todos
{self._format_todos(todos)}

## 📊 Quick Stats
- **Active Commitments**: {len(commitments.get("active", []))}
- **In Progress**: {kanban.get("in_progress_count", 0)}
- **Pending Todos**: {len([t for t in todos if t.get("status") == "pending"])}

## 🚨 Alerts
{self._check_alerts(commitments, kanban)}

---
*Auto-generated by the integrity recovery system*
*Check with: `python3 scripts/kanban-board.py show`*
"""
        return status_md

    def _get_commitments(self) -> Dict:
        """コミットメント取得"""
        commitments_file = self.project_root / "runtime" / "commitments.json"
        if commitments_file.exists():
            with open(commitments_file) as f:
                data = json.load(f)
                active = [
                    c
                    for c in data.get("commitments", [])
                    if c.get("status") != "completed"
                ]
                return {"active": active, "total": len(data.get("commitments", []))}
        return {"active": [], "total": 0}

    def _get_kanban_status(self) -> Dict:
        """Kanbanステータス取得"""
        kanban_file = self.project_root / "runtime" / "kanban-board.json"
        if kanban_file.exists():
            with open(kanban_file) as f:
                data = json.load(f)
                columns = data.get("columns", {})
                return {
                    "todo_count": len(columns.get("todo", [])),
                    "in_progress_count": len(columns.get("in_progress", [])),
                    "review_count": len(columns.get("review", [])),
                    "done_count": len(columns.get("done", [])),
                }
        return {
            "todo_count": 0,
            "in_progress_count": 0,
            "review_count": 0,
            "done_count": 0,
        }

    def _get_claude_todos(self) -> List[Dict]:
        """Claude Code Todos（モック - 実際は外部から取得）"""
        # 実際の実装では TodoRead の結果を使用
        return [
            {"content": "重複分析完了", "status": "completed", "priority": "high"},
            {"content": "docs再編完了", "status": "completed", "priority": "medium"},
        ]

    def _format_commitments(self, commitments: Dict) -> str:
        """コミットメント表示フォーマット"""
        if not commitments["active"]:
            return "✅ No active commitments"

        lines = []
        for commit in commitments["active"]:
            status_icon = "🔄" if commit.get("status") == "pending" else "⚠️"
            lines.append(f"- {status_icon} {commit.get('description', 'Unknown')}")

        return "\n".join(lines)

    def _format_kanban(self, kanban: Dict) -> str:
        """Kanban表示フォーマット"""
        return f"""- 📋 TODO: {kanban["todo_count"]}
- 🔄 IN PROGRESS: {kanban["in_progress_count"]} / 2 (WIP limit)
- 👁️ REVIEW: {kanban["review_count"]}
- ✅ DONE: {kanban["done_count"]}"""

    def _format_todos(self, todos: List[Dict]) -> str:
        """Todos表示フォーマット"""
        if not todos:
            return "✅ No todos"

        status_counts = {}
        for todo in todos:
            status = todo.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        lines = []
        for status, count in status_counts.items():
            icon = {"pending": "📋", "in_progress": "🔄", "completed": "✅"}.get(
                status, "❓"
            )
            lines.append(f"- {icon} {status.upper()}: {count}")

        return "\n".join(lines)

    def _check_alerts(self, commitments: Dict, kanban: Dict) -> str:
        """アラートチェック"""
        alerts = []

        # WIP制限チェック
        if kanban["in_progress_count"] >= 2:
            alerts.append("⚠️ WIP limit reached (2/2 in progress)")

        # 長期pending commitments
        for commit in commitments["active"]:
            if commit.get("status") == "pending":
                # 実際は時間チェックを実装
                alerts.append(
                    f"🚨 Pending commitment: {commit.get('description', 'Unknown')}"
                )

        return "\n".join(alerts) if alerts else "✅ No alerts"

    def update_status_files(self):
        """ステータスファイル更新"""
        # STATUS.md生成
        status_content = self.generate_status_md()
        with open(self.status_file, "w", encoding="utf-8") as f:
            f.write(status_content)

        print(f"✅ Updated: {self.status_file}")

        # 簡易表示も生成
        self._generate_simple_display()

    def _generate_simple_display(self):
        """シンプル表示生成"""
        commitments = self._get_commitments()
        kanban = self._get_kanban_status()

        simple_status = f"""🎯 Tasks: {kanban["in_progress_count"]}/2 active | ✅ {kanban["done_count"]} done | 📋 {commitments["total"]} commitments"""

        # .task_status ファイル（一行表示用）
        with open(self.project_root / ".task_status", "w") as f:
            f.write(simple_status)

    def show_brief_status(self):
        """簡易ステータス表示"""
        commitments = self._get_commitments()
        kanban = self._get_kanban_status()

        print("=" * 50)
        print("🎯 QUICK STATUS")
        print("=" * 50)
        print(f"📋 Active Tasks: {kanban['in_progress_count']}/2")
        print(f"✅ Completed: {kanban['done_count']}")
        print(f"🎯 Commitments: {len(commitments['active'])}/{commitments['total']}")

        if kanban["in_progress_count"] > 0:
            print(f"🔄 Currently working on {kanban['in_progress_count']} tasks")

        print("=" * 50)
        print("📄 Full status: cat STATUS.md")
        print("=" * 50)


def main():
    """メイン実行"""
    display = AutoStatusDisplay()

    import sys

    if "--brief" in sys.argv:
        display.show_brief_status()
    else:
        display.update_status_files()
        display.show_brief_status()


if __name__ == "__main__":
    main()
