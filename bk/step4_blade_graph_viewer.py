import tkinter as tk
from tkinter import Canvas, Scrollbar, PhotoImage
from graphviz import render


class BladeGraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blade Template Dependency Viewer")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

        # Canvasとスクロールバーの設定
        self.canvas = Canvas(self, bg='white')
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # マウスホイールによるスクロールイベントの追加
        self.canvas.bind_all("<MouseWheel>", self.on_vertical_scroll)  # Windows/Linuxでの垂直スクロール
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_horizontal_scroll)  # 横スクロールのためのShift + マウスホイール
        if self.tk.call('tk', 'windowingsystem') == 'aqua':  # Mac OS Xの特定
            self.canvas.bind_all("<Button-4>", self.on_vertical_scroll)  # Macでのマウスホイールアップ
            self.canvas.bind_all("<Button-5>", self.on_vertical_scroll)  # Macでのマウスホイールダウン

        # Dotファイルから画像を生成
        self.graph_image_path = self.generate_graph_image('../dependency_graph.dot', 'png')

        # 画像の表示
        self.display_graph()

    def generate_graph_image(self, dot_path, format):
        """Dotファイルから画像を生成してパスを返す"""
        output_path = dot_path.replace('.dot', '.' + format)
        render('dot', format, dot_path, outfile=output_path)
        return output_path

    def display_graph(self):
        """生成したグラフ画像を表示する"""
        img = PhotoImage(file=self.graph_image_path)
        self.canvas.create_image(0, 0, anchor="nw", image=img)
        self.canvas.image = img  # 画像の参照を保持しておく
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_vertical_scroll(self, event):
        """垂直スクロールを処理する"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def on_horizontal_scroll(self, event):
        """水平スクロールを処理する"""
        if event.delta < 0:
            self.canvas.xview_scroll(1, "units")
        elif event.delta > 0:
            self.canvas.xview_scroll(-1, "units")


if __name__ == "__main__":
    app = BladeGraphApp()
    app.mainloop()
