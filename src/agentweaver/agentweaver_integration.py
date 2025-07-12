#!/usr/bin/env python3
"""
🤖 AgentWeaver Integration System - AgentWeaver統合システム
==========================================================
@agentデコレータと動的AI組織システムの完全融合
AIシステムスペシャリスト専用実装
"""

import functools
import inspect
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# 動的AI組織システムのインポート
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.ai_organization_system import DynamicAIOrganizationSystem, DynamicRole
from memory.breakthrough_memory_system import BreakthroughMemorySystem


@dataclass
class AgentConfig:
    """AgentWeaverエージェント設定"""
    role: str
    model: str
    tools: List[str]
    personality: str
    authority_level: int = 5
    specialization: str = "general"
    memory_enabled: bool = True
    organization_integrated: bool = True


@dataclass
class WorkflowConfig:
    """AgentWeaverワークフロー設定"""
    mode: str  # "sequential", "parallel", "conditional"
    error_handling: str = "retry_3_times"
    memory_inheritance: bool = True
    organization_coordination: bool = True


class AgentWeaverIntegration:
    """AgentWeaver統合システム - コア統合エンジン"""
    
    def __init__(self):
        self.project_root = Path("/Users/dd/Desktop/1_dev/coding-rule2")
        self.integration_state_file = self.project_root / "runtime" / "agentweaver" / "integration_state.json"
        self.integration_state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # システム統合
        self.ai_organization = DynamicAIOrganizationSystem()
        self.memory_system = BreakthroughMemorySystem()
        
        # AgentWeaverエージェント登録簿
        self.registered_agents: Dict[str, Callable] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.active_workflows: Dict[str, Dict] = {}
        
        # AIシステムスペシャリスト役職を作成
        self._create_ai_specialist_role()
        
        print("🤖 AgentWeaver統合システム初期化完了")

    def _create_ai_specialist_role(self):
        """AIシステムスペシャリスト役職の動的作成"""
        from ai.ai_organization_system import RoleCapability
        
        ai_specialist = DynamicRole(
            name="AI_SYSTEMS_SPECIALIST",
            display_name="AIシステムスペシャリスト",
            icon="🤖",
            responsibilities=[
                "AI組織・エージェントシステム統括",
                "AgentWeaver統合設計・実装",
                "記憶継承システム最適化",
                "エージェント間協調機能実装",
                "AI品質保証・パフォーマンス監視"
            ],
            authority_level=9,
            decision_scope=[
                "ai_architecture_decisions",
                "agent_coordination",
                "memory_system_optimization",
                "integration_strategy"
            ],
            collaboration_requirements=[
                "PRESIDENT承認取得",
                "全AI組織との連携",
                "o3・Gemini技術協議"
            ],
            generated_from="緊急役職配布 - 2025-07-12",
            specialization="ai_systems_integration",
            required_skills=[
                "ai_architecture",
                "agent_systems",
                "memory_management",
                "system_integration"
            ]
        )
        
        # 動的AI組織システムに登録
        self.ai_organization.dynamic_roles["AI_SYSTEMS_SPECIALIST"] = ai_specialist
        
        # RoleCapabilityも登録
        self.ai_organization.role_capabilities["AI_SYSTEMS_SPECIALIST"] = RoleCapability(
            role=ai_specialist,
            responsibilities=ai_specialist.responsibilities,
            authority_level=ai_specialist.authority_level,
            decision_scope=ai_specialist.decision_scope,
            collaboration_requirements=ai_specialist.collaboration_requirements
        )
        
        # 役職活性化
        activation_result = self.ai_organization.activate_role(
            "AI_SYSTEMS_SPECIALIST", 
            "AgentWeaver統合・記憶継承システム最適化タスク"
        )
        
        print(f"🤖 AIシステムスペシャリスト役職活性化: {activation_result['display_name']}")

    def agent(
        self,
        role: str,
        model: str = "claude-sonnet-4",
        tools: List[str] = None,
        personality: str = "professional, analytical",
        authority_level: int = 5,
        specialization: str = "general"
    ):
        """AgentWeaverエージェントデコレータ - 動的AI組織統合版"""
        
        def decorator(func: Callable) -> Callable:
            # エージェント設定作成
            config = AgentConfig(
                role=role,
                model=model,
                tools=tools or [],
                personality=personality,
                authority_level=authority_level,
                specialization=specialization
            )
            
            # 動的役職としてAI組織システムに登録
            dynamic_role = DynamicRole(
                name=f"AGENT_{role.upper()}",
                display_name=f"{role}エージェント",
                icon="🔧",
                responsibilities=[f"{role}タスクの専門実行"],
                authority_level=authority_level,
                decision_scope=[f"{specialization}_decisions"],
                collaboration_requirements=["AIシステムスペシャリスト連携"],
                generated_from="AgentWeaverデコレータ統合",
                specialization=specialization,
                required_skills=[specialization]
            )
            
            self.ai_organization.dynamic_roles[f"AGENT_{role.upper()}"] = dynamic_role
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 記憶継承システム統合
                memory_context = self.memory_system.build_memory_prompt(f"Agent {role} execution")
                
                # AI組織システムでの実行
                execution_result = self.ai_organization.execute_with_role(
                    f"AGENT_{role.upper()}",
                    f"Execute {func.__name__}",
                    {
                        "function_args": args,
                        "function_kwargs": kwargs,
                        "memory_context": memory_context,
                        "agent_config": asdict(config)
                    }
                )
                
                # 実際の関数実行
                try:
                    result = func(*args, **kwargs)
                    
                    # 実行ログ記録
                    self._log_agent_execution(role, func.__name__, result, execution_result)
                    
                    return result
                    
                except Exception as e:
                    # エラー処理とログ記録
                    error_log = {
                        "agent_role": role,
                        "function": func.__name__,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                        "execution_context": execution_result
                    }
                    self._log_error(error_log)
                    raise
            
            # エージェント登録
            self.registered_agents[role] = wrapper
            self.agent_configs[role] = config
            
            return wrapper
            
        return decorator

    def workflow(
        self,
        agents: List[Callable],
        mode: str = "sequential",
        error_handling: str = "retry_3_times"
    ):
        """AgentWeaverワークフロー - AI組織協調版"""
        
        def workflow_executor(input_data: Any, context: Dict[str, Any] = None):
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            config = WorkflowConfig(
                mode=mode,
                error_handling=error_handling
            )
            
            # AIシステムスペシャリストでワークフロー統括
            orchestration_result = self.ai_organization.execute_with_role(
                "AI_SYSTEMS_SPECIALIST",
                f"Execute AgentWeaver workflow: {workflow_id}",
                {
                    "workflow_config": asdict(config),
                    "agents_count": len(agents),
                    "input_data": input_data,
                    "context": context or {}
                }
            )
            
            results = []
            
            if mode == "sequential":
                # 順次実行
                current_data = input_data
                for i, agent_func in enumerate(agents):
                    try:
                        result = agent_func(current_data)
                        results.append({
                            "agent_index": i,
                            "result": result,
                            "timestamp": datetime.now().isoformat()
                        })
                        current_data = result  # 次のエージェントに結果を渡す
                    except Exception as e:
                        if error_handling == "retry_3_times":
                            # リトライ実装
                            for retry in range(3):
                                try:
                                    result = agent_func(current_data)
                                    results.append({
                                        "agent_index": i,
                                        "result": result,
                                        "retry_count": retry + 1,
                                        "timestamp": datetime.now().isoformat()
                                    })
                                    current_data = result
                                    break
                                except Exception:
                                    if retry == 2:  # 最後のリトライも失敗
                                        raise
                        else:
                            raise
            
            elif mode == "parallel":
                # 並列実行 (簡易実装)
                for i, agent_func in enumerate(agents):
                    try:
                        result = agent_func(input_data)
                        results.append({
                            "agent_index": i,
                            "result": result,
                            "timestamp": datetime.now().isoformat()
                        })
                    except Exception as e:
                        results.append({
                            "agent_index": i,
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        })
            
            # ワークフロー結果の統合
            workflow_result = {
                "workflow_id": workflow_id,
                "mode": mode,
                "total_agents": len(agents),
                "successful_executions": len([r for r in results if "error" not in r]),
                "results": results,
                "orchestration": orchestration_result,
                "completed_at": datetime.now().isoformat()
            }
            
            # 記憶継承システムに記録
            self.memory_system.ledger_upsert(
                f"AgentWeaverワークフロー実行: {workflow_id}, 成功率: {workflow_result['successful_executions']}/{workflow_result['total_agents']}",
                importance=8
            )
            
            self.active_workflows[workflow_id] = workflow_result
            
            return workflow_result
        
        return workflow_executor

    def _log_agent_execution(self, role: str, function_name: str, result: Any, execution_context: Dict):
        """エージェント実行ログ記録"""
        log_entry = {
            "agent_role": role,
            "function": function_name,
            "timestamp": datetime.now().isoformat(),
            "execution_context": execution_context,
            "success": True
        }
        
        log_file = self.project_root / "runtime" / "agentweaver" / "execution_logs.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def _log_error(self, error_log: Dict):
        """エラーログ記録"""
        error_file = self.project_root / "runtime" / "agentweaver" / "error_logs.jsonl"
        error_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(error_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(error_log, ensure_ascii=False) + "\n")

    def get_integration_status(self) -> Dict[str, Any]:
        """統合システム状況取得"""
        return {
            "timestamp": datetime.now().isoformat(),
            "ai_organization_roles": len(self.ai_organization.dynamic_roles),
            "registered_agents": len(self.registered_agents),
            "active_workflows": len(self.active_workflows),
            "memory_system_active": self.memory_system is not None,
            "ai_specialist_active": "AI_SYSTEMS_SPECIALIST" in self.ai_organization.dynamic_roles,
            "integration_features": {
                "agent_decorator": True,
                "workflow_orchestration": True,
                "memory_inheritance": True,
                "organization_coordination": True,
                "error_handling": True,
                "execution_logging": True
            }
        }


# グローバル統合インスタンス
_integration_system = AgentWeaverIntegration()

# パブリックAPI
def agent(
    role: str,
    model: str = "claude-sonnet-4",
    tools: List[str] = None,
    personality: str = "professional, analytical",
    authority_level: int = 5,
    specialization: str = "general"
):
    """AgentWeaverエージェントデコレータ (統合版)"""
    return _integration_system.agent(role, model, tools, personality, authority_level, specialization)


def workflow(agents: List[Callable], mode: str = "sequential", error_handling: str = "retry_3_times"):
    """AgentWeaverワークフロー (統合版)"""
    return _integration_system.workflow(agents, mode, error_handling)


def get_integration_status():
    """統合システム状況取得"""
    return _integration_system.get_integration_status()


if __name__ == "__main__":
    print("🤖 AgentWeaver統合システム - テスト実行")
    
    # テストエージェント定義
    @agent(
        role="researcher",
        model="claude-sonnet-4",
        tools=["web_search"],
        personality="analytical, thorough",
        specialization="research"
    )
    def research_agent(query: str) -> str:
        return f"研究結果: {query}についての詳細分析"
    
    @agent(
        role="writer",
        model="claude-sonnet-4",
        tools=["text_generation"],
        personality="creative, clear",
        specialization="content_creation"
    )
    def writer_agent(research_data: str) -> str:
        return f"記事作成: {research_data}に基づく包括的レポート"
    
    # ワークフロー作成とテスト実行
    research_workflow = workflow([research_agent, writer_agent], mode="sequential")
    
    result = research_workflow("AgentWeaver統合システムの評価")
    
    print(f"ワークフロー実行結果: {result['workflow_id']}")
    print(f"成功率: {result['successful_executions']}/{result['total_agents']}")
    
    # 統合状況確認
    status = get_integration_status()
    print(f"\n統合システム状況:")
    print(f"  AI組織役職数: {status['ai_organization_roles']}")
    print(f"  登録エージェント数: {status['registered_agents']}")
    print(f"  AIシステムスペシャリスト: {'✅' if status['ai_specialist_active'] else '❌'}")
    
    print("\n🤖 AgentWeaver統合システム テスト完了")