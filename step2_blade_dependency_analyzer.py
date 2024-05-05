import json
import re
import os
import sys


class BladeDependencyAnalyzer:
    """Bladeファイルの依存関係を解析するクラス"""

    def __init__(self, json_path, root_directory):
        self.json_path = json_path
        self.root_directory = os.path.expanduser(root_directory)  # ホームディレクトリを展開
        self.dependencies = {}

    def load_blade_files(self):
        """JSONからBladeファイルのリストを読み込む"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.blade_files = json.load(f)
        self.inverse_blade_files = {v: k for k, v in self.blade_files.items()}

    def analyze_dependencies(self):
        """Bladeファイル間の依存関係を解析する"""
        for num, path in self.blade_files.items():
            full_path = os.path.join(self.root_directory, 'resources', 'views', path)
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # print(content)
            self.dependencies[num] = self.find_dependencies(content)

    def find_dependencies(self, content):
        """ファイル内容から依存関係を探す"""
        dependencies = []
        patterns = {
            'include': r"@include\('([^']+)'\)",
            'extends': r"@extends\('([^']+)'\)"
        }
        for dep_type, pattern in patterns.items():
            for match in re.finditer(pattern, content):
                path_dotted = match.group(1)
                path_slashed = path_dotted.replace('.', '/') + '.blade.php'
                if path_slashed in self.inverse_blade_files:
                    dependencies.append({'num': self.inverse_blade_files[path_slashed], 'type': dep_type})
        return dependencies

    def save_dependencies(self):
        """解析結果をJSONファイルに保存する"""
        with open('blade_dependencies.json', 'w', encoding='utf-8') as f:
            json.dump(self.dependencies, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) != 3:
        print("使用方法: python step2_blade_dependency_analyzer.py <json_path> <root_directory>")
        sys.exit(1)
    json_path = sys.argv[1]
    root_directory = sys.argv[2]
    # print(json_path, root_directory)

    analyzer = BladeDependencyAnalyzer(json_path, root_directory)
    analyzer.load_blade_files()
    analyzer.analyze_dependencies()
    analyzer.save_dependencies()


if __name__ == "__main__":
    main()
