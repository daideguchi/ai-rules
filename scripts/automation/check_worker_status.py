#!/usr/bin/env python3
"""
Worker Status Checker - ワーカーの現在状況確認
"""

import subprocess

def check_worker_content(worker_id, tmux_target):
    """ワーカーの現在内容を確認"""
    try:
        result = subprocess.run(
            ["tmux", "capture-pane", "-t", tmux_target, "-p"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            content = result.stdout.strip()
            return content[-500:]  # 最後の500文字
        return ""
    except Exception as e:
        return f"Error: {e}"

def main():
    workers = {
        "BOSS1": "multiagent:0.0",
        "WORKER1": "multiagent:0.1", 
        "WORKER2": "multiagent:0.2",
        "WORKER3": "multiagent:0.3"
    }
    
    print("📊 ワーカー状況確認...")
    print("=" * 60)
    
    for worker_id, tmux_target in workers.items():
        print(f"\n🔍 {worker_id} ({tmux_target}):")
        content = check_worker_content(worker_id, tmux_target)
        
        if "新しい役職配布" in content:
            print("✅ 役職配布受信済み")
        elif "待機してください" in content:
            print("⏳ 初期待機状態")
        else:
            print("❓ 状態不明")
        
        # 内容の一部を表示
        if content:
            lines = content.split('\n')
            for line in lines[-3:]:  # 最後の3行
                if line.strip():
                    print(f"   📝 {line.strip()[:60]}...")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()