#!/usr/bin/env python3
"""
Auto Enter Supervisor - プロンプト停止監視・自動エンター実行システム
"""

import subprocess
import time


class AutoEnterSupervisor:
    def __init__(self):
        self.sessions = {
            "president": "president",
            "boss1": "multiagent:0.0",
            "worker1": "multiagent:0.1",
            "worker2": "multiagent:0.2",
            "worker3": "multiagent:0.3"
        }

        self.stall_indicators = [
            "> ",  # Claude Code prompt waiting
            "? for shortcuts",  # Ready but not processing
            "Thinking…",  # Stuck in thinking
            "Actualizing…",  # Processing but may be stuck
            "Shucking…",  # Processing but may be stuck
            "Crafting…",  # Processing but may be stuck
            "Coalescing…"  # Processing but may be stuck
        ]

        self.running = False

    def get_session_content(self, session_target):
        """セッション内容取得"""
        try:
            result = subprocess.run([
                "tmux", "capture-pane", "-t", session_target, "-p"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                return result.stdout
            return ""
        except Exception:
            return ""

    def send_enter(self, session_target):
        """エンター送信"""
        try:
            subprocess.run([
                "tmux", "send-keys", "-t", session_target, "C-m"
            ], check=True)
            return True
        except Exception:
            return False

    def check_session_stall(self, session_name, session_target):
        """セッション停止チェック"""
        content = self.get_session_content(session_target)
        if not content:
            return False

        # 最後の数行をチェック
        last_lines = content.strip().split('\n')[-3:]
        last_content = '\n'.join(last_lines)

        # 停止指標をチェック
        for indicator in self.stall_indicators:
            if indicator in last_content:
                print(f"🚨 {session_name.upper()} 停止検出: {indicator}")
                return True

        # 長時間同じ状態（Thinking等）をチェック
        if any(word in last_content for word in ["Thinking…", "Actualizing…", "Crafting…"]):
            # タイムスタンプや変化をチェック（簡易版）
            return True

        return False

    def supervise_all_sessions(self):
        """全セッション監視"""
        print("🔍 Auto Enter Supervisor 開始...")
        print("   監視対象: PRESIDENT + 4 WORKERS")

        self.running = True
        check_count = 0

        while self.running:
            try:
                check_count += 1
                print(f"\n📊 監視チェック #{check_count} - {time.strftime('%H:%M:%S')}")

                for session_name, session_target in self.sessions.items():
                    if self.check_session_stall(session_name, session_target):
                        print(f"⚡ {session_name.upper()} エンター送信...")
                        if self.send_enter(session_target):
                            print(f"✅ {session_name.upper()} エンター実行完了")
                        else:
                            print(f"❌ {session_name.upper()} エンター送信失敗")

                print("💤 5秒待機...")
                time.sleep(5)

            except KeyboardInterrupt:
                print("\n🛑 監視停止")
                break
            except Exception as e:
                print(f"❌ 監視エラー: {e}")
                time.sleep(5)

        self.running = False
        print("✅ Auto Enter Supervisor 停止")

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
