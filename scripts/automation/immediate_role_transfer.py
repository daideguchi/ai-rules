#!/usr/bin/env python3
"""
Immediate Role Transfer - 現在のプレジデント出力を即座に処理
"""

import subprocess
import time


def get_president_content():
    """プレジデントセッションの内容を取得"""
    try:
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", "president", "-p"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def send_to_worker(worker_id, message):
    """ワーカーにメッセージ送信"""
    worker_mapping = {
        "BOSS1": "multiagent:0.0",
        "WORKER1": "multiagent:0.1",
        "WORKER2": "multiagent:0.2",
        "WORKER3": "multiagent:0.3"
    }

    if worker_id not in worker_mapping:
        print(f"Unknown worker: {worker_id}")
        return False

    tmux_target = worker_mapping[worker_id]

    try:
        # メッセージ送信
        subprocess.run([
            "tmux", "send-keys", "-t", tmux_target, message
        ], check=True)

        time.sleep(1)

        # エンター送信
        subprocess.run([
            "tmux", "send-keys", "-t", tmux_target, "C-m"
        ], check=True)

        print(f"✅ Sent to {worker_id}: {message[:50]}...")
        return True

    except Exception as e:
        print(f"❌ Failed to send to {worker_id}: {e}")
        return False

def main():
    print("🔗 Immediate Role Transfer - プレジデント出力解析中...")

    content = get_president_content()
    if not content:
        print("❌ プレジデントセッションの内容を取得できませんでした")
        return

    print("📋 プレジデント出力:")
    print("=" * 50)
    print(content[-1000:])  # 最後の1000文字
    print("=" * 50)

    # 検出された役職配布情報に基づいて送信
    roles = {
        "BOSS1": "セキュリティ・コンプライアンススペシャリスト - AI安全性・規制遵守・リスク管理",
        "WORKER1": "AIシステムスペシャリスト - AI組織・エージェントシステム・記憶継承",
        "WORKER2": "テクニカルリード・アーキテクト - システムアーキテクチャ分析・パフォーマンス最適化",
        "WORKER3": "品質保証・達成状況モニタリングスペシャリスト - 品質監視・Cursor Rules準拠確認"
    }

    tasks = {
        "BOSS1": "AI Compliance Engineセキュリティ分析・NIST AI RMF準拠評価を開始してください",
        "WORKER1": "AgentWeaver統合・記憶継承システム最適化を開始してください",
        "WORKER2": "システムアーキテクチャ分析・パフォーマンス最適化を開始してください",
        "WORKER3": "達成状況評価・品質監視・Cursor Rules準拠確認を開始してください"
    }

    print("🚀 役職・タスク自動配布開始...")

    for worker_id in ["BOSS1", "WORKER1", "WORKER2", "WORKER3"]:
        role = roles[worker_id]
        task = tasks[worker_id]

        message = f"🎯 新しい役職配布: {role}\n\n📋 具体的タスク: {task}\n\n各自の専門分野で分析・実装を開始し、進捗状況を報告してください。"

        print(f"📤 {worker_id}に送信中...")
        send_to_worker(worker_id, message)
        time.sleep(2)

    print("✅ 全ワーカーに役職・タスク配布完了！")

if __name__ == "__main__":
    main()
