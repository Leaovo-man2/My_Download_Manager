import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import urllib.request
from urllib.parse import urlparse
import threading
import time


class DownloadEngine:
    def __init__(self, master):
        self.master = master
        self.master.title("下载引擎")
        self.master.geometry("400x300")

        # 创建样式对象
        style = ttk.Style()

        # 设置窗口为圆角边框
        style.element_create("RoundedFrame", "from", "default")
        style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
        style.configure("TFrame", background='#87CEFA', borderwidth=0)
        style.configure("TLabel", background='#87CEFA', foreground='white')
        style.configure("TButton", background='#87CEFA', foreground='white', padding=5, relief="flat")

        # 创建组件
        self.frame = ttk.Frame(master, style="RoundedFrame")
        self.url_label = ttk.Label(self.frame, text="文件URL: ", style='TLabel')
        self.url_entry = ttk.Entry(self.frame, width=30)
        self.path_label = ttk.Label(self.frame, text="下载路径: ", style='TLabel')
        self.path_entry = ttk.Entry(self.frame, width=30)
        self.path_button = ttk.Button(self.frame, text="选择路径", command=self.choose_path, style='TButton')
        self.auto_filename_var = tk.BooleanVar()
        self.auto_filename_checkbox = ttk.Checkbutton(self.frame, text="自动识别文件名",
                                                      variable=self.auto_filename_var, style='TCheckbutton')
        self.download_button = ttk.Button(self.frame, text="下载", command=self.download_file, style='TButton')
        self.progress_bar = ttk.Progressbar(self.frame, length=200)
        self.status_label = ttk.Label(self.frame, text="", style='TLabel')
        self.speed_label = ttk.Label(self.frame, text="", style='TLabel')

        # 定位组件
        self.frame.pack(expand=True, padx=20, pady=20)
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.path_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.path_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.auto_filename_checkbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.download_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        self.status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.speed_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def choose_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def download_file(self):
        url = self.url_entry.get()
        path = self.path_entry.get()
        auto_filename = self.auto_filename_var.get()

        # 验证URL和路径是否为空
        if not url or not path:
            self.status_label.config(text="请提供文件URL和下载路径！")
            return

        # 如果需要自动识别文件名，解析URL并获取文件名部分
        if auto_filename:
            parsed_url = urlparse(url)
            file_name = parsed_url.path.split("/")[-1]

            # 如果文件名不存在，则使用默认文件名
            if not file_name:
                file_name = "downloaded_file"

            # 拼接完整的保存路径
            path = path.rstrip("/") + "/" + file_name

        # 下载文件的线程函数
        def download_thread():
            try:
                start_time = time.time()
                downloaded_bytes = 0

                # 打开URL并读取数据
                response = urllib.request.urlopen(url)
                total_size = int(response.headers["Content-Length"])

                # 写入数据到本地文件
                with open(path, "wb") as f:
                    while True:
                        data = response.read(1024)
                        if not data:
                            break
                        f.write(data)
                        downloaded_bytes += len(data)

                        # 计算下载速度
                        elapsed_time = time.time() - start_time
                        speed = downloaded_bytes / elapsed_time
                        self.speed_label.config(text=f"速度: {speed / 1024:.2f} KB/s")

                self.status_label.config(text="下载完成！")
            except:
                self.status_label.config(text="下载失败！")

        # 创建和启动下载线程
        t = threading.Thread(target=download_thread)
        t.start()

        # 更新界面显示下载进度
        self.progress_bar["value"] = 0
        self.status_label.config(text="正在下载...")
        self.update_progress()

    def update_progress(self):
        value = self.progress_bar["value"]
        if value < 100:
            self.progress_bar["value"] += 10
            self.master.after(500, self.update_progress)


def main():
    root = tk.Tk()
    download_engine = DownloadEngine(root)
    root.mainloop()


if __name__ == "__main__":
    main()
