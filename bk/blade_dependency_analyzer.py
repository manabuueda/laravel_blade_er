# step2_blade_dependency_analyzer.py
import os
import glob
import re
from typing import Dict, List


class BladeDependencyAnalyzer:
    def __init__(self, directory: str):
        # ホームディレクトリに基づくパスに変換
        self.directory = os.path.expanduser(directory)
        self.dependencies = {}

    def find_blade_files(self) -> List[str]:
        """指定されたディレクトリからBladeファイルのリストを取得する"""
        return glob.glob(os.path.join(self.directory, '**/*.blade.php'), recursive=True)

    def parse_blade_file(self, file_path: str) -> Dict[str, List[str]]:
        """Bladeファイルを解析して、依存関係を抽出する"""
        directives = {'extends': [], 'include': [], 'includewhen': [], 'yield': []}
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for directive in directives:
                pattern = r'@' + directive + r'\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
                directives[directive].extend(re.findall(pattern, content))
        relative_path = os.path.relpath(file_path, self.directory)
        self.dependencies[relative_path] = directives

    def analyze(self):
        """ディレクトリ内の全Bladeファイルを解析する"""
        blade_files = self.find_blade_files()
        for file_path in blade_files:
            self.parse_blade_file(file_path)

    def get_dependencies(self) -> Dict[str, Dict[str, List[str]]]:
        """解析結果の依存関係を取得する"""
        return self.dependencies


if __name__ == '__main__':
    # コマンドラインからディレクトリを指定して実行可能
    import sys

    if len(sys.argv) > 1:
        dir = sys.argv[1]
    else:
        dir = '~/Sites/event-form.jp/program/laravel/resources/views'  # デフォルトのディレクトリ
    analyzer = BladeDependencyAnalyzer(dir)
    analyzer.analyze()
    dependencies = analyzer.get_dependencies()
    print(dependencies)  # 解析結果を表示
