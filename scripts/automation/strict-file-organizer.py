#!/usr/bin/env python3
"""
Strict File Organization Enforcer
厳格ファイル組織強制システム

Enforces absolute file organization rules with zero tolerance.
"""

import os
import sys
import shutil
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from datetime import datetime

class StrictFileOrganizer:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.violations = []
        self.moved_files = []
        
        # プロジェクトタイプを検出
        self.project_type = self._detect_project_type()
        
        # プロジェクトタイプ別設定を読み込み
        self._load_project_configuration()
        
    def _detect_project_type(self) -> str:
        """プロジェクトタイプを自動検出"""
        # coding-rule2元プロジェクトかチェック
        if self._is_original_coding_rule2():
            return 'ai-project'
        
        # CLAUDE.mdがあればAIプロジェクト（優先度高）
        if (self.project_root / 'CLAUDE.md').exists():
            return 'ai-project'
        
        # Makefileがあり、AI関連のターゲットが含まれていればAIプロジェクト
        makefile = self.project_root / 'Makefile'
        if makefile.exists():
            try:
                with open(makefile, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'ai-org-start' in content or 'declare-president' in content:
                        return 'ai-project'
            except:
                pass
        
        # package.jsonがあればwebプロジェクト
        if (self.project_root / 'package.json').exists():
            return 'web'
        
        # setup.pyがあり、CLAUDE.mdがなければpythonプロジェクト
        if (self.project_root / 'setup.py').exists():
            return 'python'
        
        # pyproject.tomlがあり、webやAI関連でなければpythonプロジェクト
        if (self.project_root / 'pyproject.toml').exists() and not (self.project_root / 'CLAUDE.md').exists():
            return 'python'
        
        # デフォルトはカスタム
        return 'custom'
    
    def _is_original_coding_rule2(self) -> bool:
        """元のcoding-rule2プロジェクトかチェック"""
        indicators = [
            'scripts/automation/strict-file-organizer.py',
            'docs/04_reference/STRICT_FILE_ORGANIZATION_RULES.md'
        ]
        
        for indicator in indicators:
            if not (self.project_root / indicator).exists():
                return False
                
        return True
    
    def _load_project_configuration(self):
        """プロジェクトタイプ別設定を読み込み"""
        configurations = {
            'web': {
                'file_limit': 15,
                'allowed_files': {
                    'README.md', 'package.json', 'package-lock.json',
                    'index.html', 'vite.config.js', '.gitignore',
                    'LICENSE', 'tsconfig.json', '.env'
                },
                'allowed_dirs': {
                    'src', 'public', 'docs', 'tests', 'scripts', 
                    'node_modules', 'dist', '.cursor'
                }
            },
            'python': {
                'file_limit': 12,
                'allowed_files': {
                    'README.md', 'setup.py', 'pyproject.toml', 'requirements.txt',
                    'LICENSE', '.gitignore', 'MANIFEST.in', 'tox.ini',
                    'CHANGELOG.md', '.env'
                },
                'allowed_dirs': {
                    'src', 'docs', 'tests', 'examples', 'scripts', 
                    '.tox', 'dist', '.cursor'
                }
            },
            'ai-project': {
                'file_limit': 12,
                'allowed_files': {
                    'README.md', 'Makefile', 'pyproject.toml', 'requirements.txt',
                    'LICENSE', 'CLAUDE.md', 'Index.md', '.gitignore',
                    '.env', '.mcp.json', '.mypy.ini', 'docker-compose.yml'
                },
                'allowed_dirs': {
                    'config', 'docs', 'scripts', 'src', 'tests', 
                    'runtime', 'data', '.cursor'
                }
            },
            'custom': {
                'file_limit': 20,
                'allowed_files': {
                    'README.md', '.gitignore', 'LICENSE'
                },
                'allowed_dirs': {
                    'src', 'docs', 'tests', 'scripts', '.cursor'
                }
            }
        }
        
        config = configurations.get(self.project_type, configurations['custom'])
        
        self.ROOT_FILE_LIMIT = config['file_limit']
        self.ALLOWED_ROOT_FILES = config['allowed_files']
        self.ALLOWED_ROOT_DIRS = config['allowed_dirs']
        
        # プロジェクトタイプ別ファイルルール
        if self.project_type == 'ai-project':
            self.FILE_RULES = {
                '.cursorrules': 'config/editor/',
                '.claude-project': 'config/editor/',
                '.cursorignore': 'config/editor/',
                '.cursorindexignore': 'config/editor/',
                '.forbidden-move': 'config/editor/',
                '.gitattributes': 'config/git/',
                '.pre-commit-config.yaml': 'config/git/',
                '.pylintrc': 'config/dev/',
                '.flake8': 'config/dev/',
                '.black': 'config/dev/',
                '.env.example': 'scripts/setup/',
                '.env.local': 'scripts/setup/',
                '.env.test': 'scripts/setup/',
            }
        else:
            # 他のプロジェクトタイプ用の一般的なルール
            self.FILE_RULES = {
                '.cursorrules': 'config/',
                '.claude-project': 'config/',
                '.cursorignore': 'config/',
                '.cursorindexignore': 'config/',
                '.gitattributes': 'config/',
                '.pre-commit-config.yaml': 'config/',
                '.pylintrc': 'config/',
                '.flake8': 'config/',
                '.black': 'config/',
                '.env.example': 'config/',
                '.env.local': 'config/',
                '.env.test': 'config/',
            }
        
        # パターンベースルール
        self.PATTERN_RULES = {
            r'.*\.md$': 'docs/',
            r'setup_.*\.py$': 'scripts/',
            r'.*_test\.py$': 'tests/',
            r'.*\.config\..*$': 'config/',
            r'.*\.ini$': 'config/',
        }
        
    def audit_root_directory(self) -> Dict:
        """ルートディレクトリの監査"""
        root_files = [f for f in os.listdir(self.project_root) 
                     if os.path.isfile(os.path.join(self.project_root, f))]
        
        violations = []
        misplaced = []
        
        for file in root_files:
            if file not in self.ALLOWED_ROOT_FILES:
                violations.append(file)
                
                # 移動先を決定
                target = self._get_target_location(file)
                if target:
                    misplaced.append((file, target))
        
        return {
            'total_files': len(root_files),
            'limit': self.ROOT_FILE_LIMIT,
            'over_limit': len(root_files) > self.ROOT_FILE_LIMIT,
            'violations': violations,
            'misplaced': misplaced,
            'compliant': len(violations) == 0 and len(root_files) <= self.ROOT_FILE_LIMIT,
            'project_type': self.project_type
        }
    
    def _get_target_location(self, filename: str) -> Optional[str]:
        """ファイルの移動先を決定"""
        # 許可されたファイルはルートに残す
        if filename in self.ALLOWED_ROOT_FILES:
            return None
            
        # 特定ファイル名ルール
        if filename in self.FILE_RULES:
            return self.FILE_RULES[filename]
            
        # パターンマッチング
        for pattern, target in self.PATTERN_RULES.items():
            if re.match(pattern, filename):
                # マークダウンファイルの特別処理
                if pattern.endswith(r'\.md$'):
                    if filename in ['README.md', 'CLAUDE.md', 'Index.md', 'CHANGELOG.md']:
                        return None  # ルートに残す
                return target
        
        # ファイル拡張子ベースの分類
        if filename.startswith('.'):
            return 'config/'
        elif filename.endswith('.md'):
            return 'docs/'
        elif filename.endswith('.py') and 'setup' in filename:
            return 'scripts/'
        elif filename.endswith('.sh'):
            return 'scripts/'
        elif filename.endswith(('.json', '.yaml', '.yml', '.toml')) and filename not in self.ALLOWED_ROOT_FILES:
            return 'config/'
        elif filename.endswith(('.txt', '.log')):
            return 'docs/'
        
        # 推奨場所を提案
        return 'docs/'  # デフォルトは docs/
    
    def enforce_organization(self, dry_run: bool = False) -> Dict:
        """ファイル組織を強制実行"""
        audit = self.audit_root_directory()
        
        if audit['compliant']:
            return {
                'status': 'compliant',
                'message': f"✅ ルートディレクトリは準拠済み: {audit['total_files']}/{self.ROOT_FILE_LIMIT} ファイル",
                'actions': [],
                'project_type': self.project_type
            }
        
        actions = []
        
        # 配置ミスファイルを移動
        for file, target_dir in audit['misplaced']:
            source = self.project_root / file
            target_path = self.project_root / target_dir
            
            # ターゲットディレクトリを作成
            target_path.mkdir(parents=True, exist_ok=True)
            
            target_file = target_path / file
            
            action = {
                'type': 'move',
                'source': str(source),
                'target': str(target_file),
                'reason': f'ルートディレクトリに許可されていないファイル'
            }
            
            if not dry_run:
                try:
                    shutil.move(str(source), str(target_file))
                    action['status'] = 'success'
                    self.moved_files.append((str(source), str(target_file)))
                except Exception as e:
                    action['status'] = 'failed'
                    action['error'] = str(e)
            else:
                action['status'] = 'dry_run'
                
            actions.append(action)
        
        # 移動後の最終監査
        if not dry_run:
            final_audit = self.audit_root_directory()
            compliance_status = 'compliant' if final_audit['compliant'] else 'non_compliant'
        else:
            compliance_status = 'dry_run'
            
        return {
            'status': compliance_status,
            'initial_audit': audit,
            'actions': actions,
            'files_moved': len([a for a in actions if a['status'] == 'success']),
            'project_type': self.project_type
        }
    
    def generate_compliance_report(self) -> Dict:
        """詳細なコンプライアンスレポートを生成"""
        audit = self.audit_root_directory()
        
        # ディレクトリ構造チェック
        if self.project_type == 'ai-project':
            required_dirs = ['config', 'docs', 'scripts', 'src', 'tests']
        elif self.project_type == 'web':
            required_dirs = ['src', 'docs', 'tests', 'scripts']
        elif self.project_type == 'python':
            required_dirs = ['src', 'docs', 'tests', 'examples']
        else:
            required_dirs = ['src', 'docs', 'tests']
            
        missing_dirs = []
        for dir_name in required_dirs:
            if not (self.project_root / dir_name).exists():
                missing_dirs.append(dir_name)
        
        # 重要度レベル取得
        severity = self._get_severity_level(audit['total_files'])
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'project_type': self.project_type,
            'compliance': audit,
            'severity': severity,
            'missing_directories': missing_dirs,
            'recommendations': self._generate_recommendations(audit, missing_dirs)
        }
        
        return report
    
    def _get_severity_level(self, file_count: int) -> Dict:
        """違反重要度レベルを判定"""
        if file_count <= self.ROOT_FILE_LIMIT:
            return {'level': 'GREEN', 'action': 'none', 'message': '✅ 準拠'}
        elif file_count <= self.ROOT_FILE_LIMIT + 5:
            return {'level': 'YELLOW', 'action': 'auto_move', 'message': '🟡 自動強制実行済み'}
        else:
            return {'level': 'RED', 'action': 'manual_cleanup', 'message': '🔴 緊急: 手動クリーンアップが必要'}
    
    def _generate_recommendations(self, audit: Dict, missing_dirs: List[str]) -> List[str]:
        """実行可能な推奨事項を生成"""
        recommendations = []
        
        if audit['over_limit']:
            recommendations.append(f"ルートファイル数を {audit['total_files']} から {self.ROOT_FILE_LIMIT} 以下に削減")
        
        if audit['violations']:
            recommendations.append(f"{len(audit['violations'])} 個の配置ミスファイルを適切なディレクトリに移動")
        
        if missing_dirs:
            recommendations.append(f"不足ディレクトリを作成: {', '.join(missing_dirs)}")
            
        if not recommendations:
            recommendations.append("現在の組織構造を維持")
            
        return recommendations

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='厳格ファイル組織強制システム')
    parser.add_argument('--check-only', action='store_true', help='変更せずにコンプライアンスをチェック')
    parser.add_argument('--force', action='store_true', help='ファイル再組織を強制実行')
    parser.add_argument('--dry-run', action='store_true', help='実際に移動せずに何が移動されるかを表示')
    parser.add_argument('--report', action='store_true', help='詳細なコンプライアンスレポートを生成')
    parser.add_argument('--project-root', type=str, help='プロジェクトルートディレクトリ')
    
    args = parser.parse_args()
    
    organizer = StrictFileOrganizer(args.project_root)
    
    if args.check_only:
        audit = organizer.audit_root_directory()
        print(f"📊 ルートディレクトリ監査")
        print(f"プロジェクトタイプ: {audit['project_type']}")
        print(f"ファイル数: {audit['total_files']}/{organizer.ROOT_FILE_LIMIT}")
        print(f"ステータス: {'✅ 準拠' if audit['compliant'] else '❌ 非準拠'}")
        
        if audit['violations']:
            print(f"\n🔴 違反 ({len(audit['violations'])} 件):")
            for file in audit['violations']:
                target = organizer._get_target_location(file)
                print(f"  • {file} → {target if target else 'ルートに配置可能'}")
                
        severity = organizer._get_severity_level(audit['total_files'])
        print(f"\n🚨 重要度: {severity['level']} - {severity['message']}")
        
        sys.exit(0 if audit['compliant'] else 1)
    
    elif args.report:
        report = organizer.generate_compliance_report()
        
        print(f"📋 コンプライアンスレポート")
        print(f"プロジェクトタイプ: {report['project_type']}")
        print(f"ステータス: {report['severity']['message']}")
        print(f"推奨事項: {len(report['recommendations'])} 件")
        
        for rec in report['recommendations']:
            print(f"  • {rec}")
    
    elif args.force or args.dry_run:
        result = organizer.enforce_organization(dry_run=args.dry_run)
        
        print(f"🔧 ファイル組織 {'ドライラン' if args.dry_run else '強制実行'}")
        print(f"プロジェクトタイプ: {result['project_type']}")
        print(f"ステータス: {result['status'].upper()}")
        
        if result['actions']:
            print(f"\n📋 実行内容 ({len(result['actions'])} 件):")
            for action in result['actions']:
                status_icons = {'success': '✅', 'failed': '❌', 'dry_run': '🔍'}
                status_icon = status_icons.get(action['status'], '❓')
                print(f"  {status_icon} {action['type'].upper()}: {Path(action['source']).name} → {action['target']}")
        
        if not args.dry_run and result['files_moved'] > 0:
            print(f"\n🎉 {result['files_moved']} ファイルを正常に移動しました")
            
        final_audit = organizer.audit_root_directory()
        print(f"\n📊 最終ステータス: {final_audit['total_files']}/{organizer.ROOT_FILE_LIMIT} ファイル")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()