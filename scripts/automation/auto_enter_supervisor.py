#!/usr/bin/env python3
"""
Auto Enter Supervisor - 軽量定期エンター送信システム（30秒間隔・5分アイドル自動停止）
"""

import hashlib
import subprocess
import time


class AutoEnterSupervisor:
    def __init__(self):
        self.sessions = [
            "president",
            "multiagent:0.0",  # BOSS1
            "multiagent:0.1",  # WORKER1
            "multiagent:0.2",  # WORKER2
            "multiagent:0.3"   # WORKER3
        ]

        self.running = False
        self.last_content_hashes = {}  # 各セッションの最終コンテンツハッシュ
        self.idle_counts = {}  # 各セッションのアイドルカウント
        self.max_idle_cycles = 10  # 30秒 × 10 = 5分

    def get_session_content_hash(self, session):
        """セッション内容のハッシュ取得"""
        try:
            result = subprocess.run([
                "tmux", "capture-pane", "-t", session, "-p"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                # 最後の200文字をハッシュ化（軽量化）
                content = result.stdout.strip()[-200:]
                return hashlib.md5(content.encode()).hexdigest()
            return ""
        except Exception:
            return ""

    def check_activity(self):
        """全セッションの活動状況チェック"""
        active_sessions = 0

        for session in self.sessions:
            current_hash = self.get_session_content_hash(session)
            last_hash = self.last_content_hashes.get(session, "")

            if current_hash != last_hash:
                # 変化あり - アクティブ
                self.idle_counts[session] = 0
                active_sessions += 1
            else:
                # 変化なし - アイドル増加
                self.idle_counts[session] = self.idle_counts.get(session, 0) + 1

            self.last_content_hashes[session] = current_hash

        return active_sessions

    def is_all_idle_too_long(self):
        """全セッションが長時間アイドルかチェック"""
        for session in self.sessions:
            if self.idle_counts.get(session, 0) < self.max_idle_cycles:
                return False
        return True

    def send_enter_to_all(self):
        """全セッションにエンター送信"""
        success_count = 0
        for session in self.sessions:
            try:
                subprocess.run([
                    "tmux", "send-keys", "-t", session, "C-m"
                ], check=True, capture_output=True)
                success_count += 1
            except Exception:
                pass  # エラーは無視（セッションが存在しない場合等）
        return success_count

    def supervise_all_sessions(self):
        """軽量定期エンター送信（30秒間隔・5分アイドル自動停止）"""
        print("🔍 軽量Auto Enter Supervisor 開始...")
        print("   30秒間隔エンター送信 + 5分アイドル自動停止機能")

        self.running = True
        cycle_count = 0

        while self.running:
            try:
                cycle_count += 1

                # 活動状況チェック
                active_sessions = self.check_activity()

                # エンター送信
                sent_count = self.send_enter_to_all()

                # ステータス表示
                print(f"⚡ #{cycle_count} - {time.strftime('%H:%M:%S')} - {sent_count}/5送信完了 - アクティブ: {active_sessions}")

                # 全セッション長時間アイドルチェック
                if self.is_all_idle_too_long():
                    print("💤 全セッション5分間アイドル検出 - 自動停止します")
                    break

                # 30秒待機
                time.sleep(30)

            except KeyboardInterrupt:
                print("\n🛑 手動停止")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
                time.sleep(30)

        self.running = False
        print("✅ 軽量Auto Enter Supervisor 停止")

    def stop(self):
        """監視停止"""
        self.running = False

def main():
    supervisor = AutoEnterSupervisor()
    try:
        supervisor.supervise_all_sessions()
    except KeyboardInterrupt:
        supervisor.stop()

if __name__ == "__main__":
    main()
