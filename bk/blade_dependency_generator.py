import os
import re
import subprocess
from datetime import datetime
from tqdm import tqdm  # 進捗表示用ライブラリ


# Bladeファイルの依存関係を解析する関数
def find_blade_dependencies(root_dir):
    dependencies = {}
    reverse_dependencies = {}

    for root, dirs, files in tqdm(os.walk(root_dir), desc="Scanning Blade files"):
        for file in tqdm(files, desc="Processing files", leave=False):
            if file.endswith('.blade.php'):
                filepath = os.path.relpath(os.path.join(root, file), root_dir)
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    patterns = ['@include\\([\'"]([^\'"]+)[\'"]\\)', '@extends\\([\'"]([^\'"]+)[\'"]\\)',
                                '@component\\([\'"]([^\'"]+)[\'"]\\)']
                    for pattern in patterns:
                        matches = re.findall(pattern, content)  # パターンマッチング
                        if matches:
                            # 依存関係のリストに追加
                            for match in matches:
                                target_path = match.replace('.', '/') + '.blade.php'  # ファイルパスに変換
                                dependencies.setdefault(filepath, set()).add(target_path)
                                reverse_dependencies.setdefault(target_path, set()).add(filepath)
    return dependencies, reverse_dependencies


# DOTファイルを生成する関数
def generate_dot(dependencies, output_file, start_file=None):
    with open(output_file, 'w') as f:
        f.write('digraph G { rankdir=LR; node [shape=box, style=filled, color=lightblue]; \n')

        if start_file:
            visited = set()
            stack = [start_file]
            while stack:
                current = stack.pop()
                if current in dependencies:
                    for target in dependencies[current]:
                        # 引用符の不一致や特殊文字を避ける
                        f.write(f' "{current}" -> "{target}";\n')
                        stack.append(target)

        else:
            for source, targets in dependencies.items():
                for target in targets:
                    f.write(f' "{source}" -> "{target}";\n')

        f.write('}\n')


# 画像ファイルを生成する関数
def generate_image_from_dot(dot_file, image_file):
    subprocess.run(['dot', '-Tpng', dot_file, '-o', image_file], check=True)


# 関係図を生成する関数
def generate_graphs(blade_directory, output_base_dir, start_file=None):
    dependencies, reverse_dependencies = find_blade_dependencies(blade_directory)

    dot_dir = os.path.join(output_base_dir, 'dot')
    png_dir = os.path.join(output_base_dir, 'png')
    create_output_directory(dot_dir)
    create_output_directory(png_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    dot_output = os.path.join(dot_dir, f'dependencies_graph_{timestamp}.dot')
    png_output = os.path.join(png_dir, f'dependency_graph_{timestamp}.png')

    generate_dot(dependencies, dot_output, start_file)
    generate_image_from_dot(dot_output, png_output)

    return png_output


# 出力ディレクトリを作成する関数
def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
