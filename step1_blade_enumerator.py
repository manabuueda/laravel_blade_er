import os
import json
import sys

class BladeEnumerator:
    """ディレクトリ内のBladeファイルを列挙し、番号付けしてJSONに保存するクラス"""

    def __init__(self, directory):
        self.directory = directory
        self.blade_files = {}

    def enumerate_blade_files(self):
        """Bladeファイルを列挙して番号を割り当て、JSONに出力する"""
        file_number = 1
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.blade.php'):
                    relative_path = os.path.relpath(os.path.join(root, file), self.directory)
                    self.blade_files[file_number] = relative_path
                    file_number += 1
        self.save_to_json()

    def save_to_json(self):
        """BladeファイルのマッピングをJSONファイルに保存する"""
        with open('blade_files.json', 'w', encoding='utf-8') as f:
            json.dump(self.blade_files, f, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) != 2:
        print("使用方法: python step1_blade_enumerator.py ~/Sites/event-form.jp/program/laravel/resources/views")
        sys.exit(1)
    directory = sys.argv[1]
    enumerator = BladeEnumerator(directory)
    enumerator.enumerate_blade_files()

if __name__ == "__main__":
    main()
