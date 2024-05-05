import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import os
import threading
from blade_dependency_generator import generate_graphs  # Blade依存関係生成スクリプトをインポート

# デフォルトディレクトリを変数で設定
default_dir = os.path.expanduser('~/Sites/event-form.jp/program/laravel/resources/views')  # デフォルトディレクトリ


# GUIアプリケーションクラス
class BladeDependencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Laravel Blade Dependency Viewer")

        # 画面いっぱいに設定
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")  # ウィンドウサイズを画面いっぱいに

        # スクロール可能なCanvasとスクロールバー
        self.outer_frame = tk.Frame(self)
        self.outer_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.outer_frame, bg="white")
        self.scroll_x = tk.Scrollbar(self.outer_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.outer_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 進捗バー
        self.progress_bar = Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(pady=10)

        # ディレクトリ選択ボタン
        self.select_dir_button = tk.Button(self, text="Select Blade Directory", command=self.select_directory)
        self.select_dir_button.pack(pady=10)

        self.blade_directory = None
        self.selected_item = None  # 選択されたアイテム

        # マウススクロールのイベントを設定
        self.bind_mouse_scroll()  # マウスホイールイベントをバインド

        # キャンバス上でクリックしたときのイベントを設定
        self.canvas.bind("<Button-1>", self.on_canvas_click)  # 左クリックイベントをバインド

    def bind_mouse_scroll(self):
        # 縦スクロール
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # WindowsとMac用
        self.canvas.bind_all("<Button-4>", self.on_mouse_wheel)  # Linux用
        self.canvas.bind_all("<Button-5>", self.on_mouse_wheel)  # Linux用

        # 横スクロール
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mouse_wheel)  # WindowsとMac用

    def on_mouse_wheel(self, event):
        # 縦スクロールの処理
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")  # 下にスクロール
        else:
            self.canvas.yview_scroll(-1, "units")  # 上にスクロール

    def on_shift_mouse_wheel(self, event):
        # 横スクロールの処理
        if event.num == 5 or event.delta < 0:
            self.canvas.xview_scroll(1, "units")  # 右にスクロール
        else:
            self.canvas.xview_scroll(-1, "units")  # 左にスクロール

    def select_directory(self):
        # ディレクトリ選択ダイアログ
        self.blade_directory = filedialog.askdirectory(title="Select Blade Directory", initialdir=default_dir)
        if self.blade_directory:
            self.process_directory()  # ディレクトリ選択後の処理

    def process_directory(self):
        self.progress_bar.start()  # 進捗バーを開始

        def process():
            # 関係図を生成
            png_file = generate_graphs(self.blade_directory, "../graph_output")
            self.show_graph(png_file)  # 生成された画像を表示

            self.progress_bar.stop()  # 進捗バーを停止

        threading.Thread(target=process).start()  # スレッドで処理

    def on_canvas_click(self, event):
        # キャンバス上でクリックしたときの処理
        item = self.canvas.find_closest(event.x, event.y)  # クリックされたアイテムを取得
        self.selected_item = item  # 選択されたアイテムを設定

        # アイテムのタイプを確認し、テキストの場合にのみ処理を行う
        item_type = self.canvas.type(self.selected_item)  # アイテムのタイプを確認
        if item_type == "text":  # アイテムがテキストの場合にのみ処理
            item_text = self.canvas.itemcget(self.selected_item, "text")  # アイテムのテキストを取得

            # 矢印の色を青に変更する処理
            all_items = self.canvas.find_all()  # キャンバス上のすべてのアイテムを取得
            for arrow in all_items:
                # 前後関係を示す矢印の色を青に変更
                if item_text in self.canvas.itemcget(arrow, "text"):
                    self.canvas.itemconfig(arrow, fill='blue')  # 矢印の色を青に変更

    def show_graph(self, png_file):
        if self.blade_directory:
            # 画像を読み込み、キャンバスに表示
            image = Image.open(png_file)
            self.canvas.config(scrollregion=(0, 0, image.width, image.height))  # スクロール領域を設定
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)  # 左上基点で表示

        else:
            messagebox.showwarning("Error", "Please select a Blade directory first.")


# GUIアプリケーションの実行
if __name__ == "__main__":
    app = BladeDependencyApp()
    app.mainloop()
