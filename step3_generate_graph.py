import json
from graphviz import Digraph

def load_json(filename):
    """JSONファイルからデータを読み込む"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_dependency_graph(dependencies, file_map, output_filename="dependency_graph.dot"):
    """依存関係とファイルマッピングからGraphvizのDOTファイルを生成する
    dependencies: 依存関係データを含む辞書
    file_map: 各ノード番号に対応するファイルパスを含む辞書
    output_filename: 出力されるDOTファイルのファイル名
    """
    graph = Digraph(comment='Blade Template Dependencies')
    graph.attr(rankdir='LR')
    graph.attr('node', shape='box', style='filled', color='lightblue')

    # ノードの追加
    for num, path in file_map.items():
        graph.node(num, label=f"{path}")

    # 依存関係の追加
    for num, deps in dependencies.items():
        for dep in deps:
            if dep['type'] == 'extends':
                # 矢印の向きを子から親へ（継承）
                graph.edge(dep['num'], num, label='extends')
            elif dep['type'] == 'include':
                # 矢印の向きを親から子へ（含む）
                graph.edge(num, dep['num'], label='include')

    graph.render(output_filename, format='png', view=True)

def main():
    dependencies = load_json('blade_dependencies.json')
    file_map = load_json('blade_files.json')
    create_dependency_graph(dependencies, file_map, 'dependency_graph.dot')

if __name__ == "__main__":
    main()
