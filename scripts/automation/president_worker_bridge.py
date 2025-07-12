#!/usr/bin/env python3
"""
President-Worker Bridge System
プレジデントの指示を自動的にワーカーに転送するシステム
"""

import json
import re
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime

class PresidentWorkerBridge:
    def __init__(self):
        self.project_root = Path("/Users/dd/Desktop/1_dev/coding-rule2")
        self.log_file = self.project_root / "runtime/logs/president_worker_bridge.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.worker_mapping = {
            "BOSS1": "multiagent:0.0",
            "WORKER1": "multiagent:0.1", 
            "WORKER2": "multiagent:0.2",
            "WORKER3": "multiagent:0.3"
        }
        
        self.running = False
        self.last_content = ""
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"🔗 Bridge: {message}")
    
    def get_president_content(self):
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
            self.log(f"Error capturing president content: {e}")
            return ""
    
    def parse_role_assignments(self, content):
        """役職配布を解析"""
        assignments = {}
        
        # パターン1: BOSS1: 役職名
        pattern1 = r"(BOSS1|WORKER[1-3]):\s*([^\n]+?)(?:専門領域|担当|スペシャリスト|リード|アーキテクト)"
        matches = re.findall(pattern1, content, re.IGNORECASE)
        
        for worker, role in matches:
            assignments[worker.upper()] = role.strip()
        
        # パターン2: - ✅ BOSS1: 詳細な役職説明
        pattern2 = r"- ✅ (BOSS1|WORKER[1-3]):\s*([^\n]+)"
        matches = re.findall(pattern2, content, re.IGNORECASE)
        
        for worker, role in matches:
            assignments[worker.upper()] = role.strip()
            
        return assignments
    
    def parse_task_assignments(self, content):
        """タスク配布を解析"""
        tasks = {}
        
        # パターン: - BOSS1: 具体的なタスク
        pattern = r"- (BOSS1|WORKER[1-3]):\s*([^\n]+)"
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        for worker, task in matches:
            tasks[worker.upper()] = task.strip()
            
        return tasks
    
    def send_to_worker(self, worker_id, message):
        """ワーカーにメッセージ送信"""
        if worker_id not in self.worker_mapping:
            self.log(f"Unknown worker: {worker_id}")
            return False
            
        tmux_target = self.worker_mapping[worker_id]
        
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
            
            self.log(f"✅ Sent to {worker_id}: {message[:50]}...")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to send to {worker_id}: {e}")
            return False
    
    def process_president_output(self, content):
        """プレジデント出力を処理してワーカーに転送"""
        if content == self.last_content:
            return
            
        self.last_content = content
        
        # 役職配布の検出
        roles = self.parse_role_assignments(content)
        if roles:
            self.log(f"🎯 Detected role assignments: {len(roles)} workers")
            for worker, role in roles.items():
                message = f"あなたの新しい役職は「{role}」です。この役職に応じた専門業務を開始してください。担当領域を分析し、具体的なアクションプランを作成してください。"
                self.send_to_worker(worker, message)
        
        # タスク配布の検出
        tasks = self.parse_task_assignments(content)
        if tasks:
            self.log(f"📋 Detected task assignments: {len(tasks)} workers")
            for worker, task in tasks.items():
                message = f"具体的タスク: {task} このタスクを実行し、進捗状況を報告してください。"
                self.send_to_worker(worker, message)
    
    def start_monitoring(self):
        """監視開始"""
        self.running = True
        self.log("🚀 President-Worker Bridge started")
        
        while self.running:
            try:
                content = self.get_president_content()
                if content:
                    self.process_president_output(content)
                time.sleep(3)  # 3秒間隔で監視
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.log(f"Error in monitoring loop: {e}")
                time.sleep(5)
        
        self.log("🛑 President-Worker Bridge stopped")
    
    def stop_monitoring(self):
        """監視停止"""
        self.running = False

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "start":
        bridge = PresidentWorkerBridge()
        try:
            bridge.start_monitoring()
        except KeyboardInterrupt:
            bridge.stop_monitoring()
    else:
        print("Usage: python president_worker_bridge.py start")

if __name__ == "__main__":
    main()