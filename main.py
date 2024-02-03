import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import urllib.request
from urllib.parse import urlparse
import threading
import time
import urllib.error

class DownloadEngine:
    def __init__(self, master):
        self.master = master
        self.master.title("下载引擎")
        self.master.geometry("400x350")  # Adjusted height to accommodate the additional elements

        # 创建样式对象
        style = ttk.Style()

        # 设置窗口为圆角边框
        style.element_create("RoundedFrame", "from", "default")
        style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])
        style.configure("TFrame", background='#87CEFA', borderwidth=0)
        style.configure("TLabel", background='#87CEFA', foreground='black', font=('Helvetica', 16, 'bold'))  # Increased font size and added bold
        style.configure("TButton", background='#87CEFA', foreground='black', padding=5, relief="flat")
        style.configure("TCheckbutton", background='#87CEFA', foreground='black', padding=5, relief="flat")

        # 创建组件
        self.frame = ttk.Frame(master, style="RoundedFrame")
        self.title_label = ttk.Label(self.frame, text="欢迎使用MDM", style='TLabel')  # Added a large title label
        self.url_label = ttk.Label(self.frame, text="文件URL: ", style='TLabel')
        self.url_entry = ttk.Entry(self.frame, width=30)
        self.path_label = ttk.Label(self.frame, text="下载路径: ", style='TLabel')
        self.path_entry = ttk.Entry(self.frame, width=30)
        self.path_button = ttk.Button(self.frame, text="选择路径", command=self.choose_path, style='TButton')
        self.auto_filename_var = tk.BooleanVar()
        self.auto_filename_checkbox = ttk.Checkbutton(self.frame, text="自动识别文件名",
                                                      variable=self.auto_filename_var, style='TCheckbutton')
        self.download_button = ttk.Button(self.frame, text="下载", command=self.download_file, style='TButton')
        self.progress_bar = ttk.Progressbar(self.frame, length=200, mode="determinate")
        self.status_label = ttk.Label(self.frame, text="", style='TLabel')
        self.speed_label = ttk.Label(self.frame, text="", style='TLabel')
        self.copyright_label = ttk.Label(self.frame, text="©2024 Leaovo-man2", style='TLabel', font=('Helvetica', 8))  # Added a small copyright label

        # 定位组件
        self.frame.pack(expand=True, padx=20, pady=20)
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)  # Positioned the title label
        self.url_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.path_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.path_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        self.path_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.auto_filename_checkbox.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.download_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")
        self.progress_bar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="we")
        self.status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.speed_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.copyright_label.grid(row=8, column=0, columnspan=3, pady=10)  # Positioned the copyright label

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

                        # 计算并设置下载进度百分比
                        progress_percent = (downloaded_bytes / total_size) * 100
                        self.progress_bar["value"] = progress_percent

                self.status_label.config(text="下载完成！")
            except urllib.error.URLError as e:
                self.status_label.config(text=f"下载失败！错误: {str(e)}")
            except urllib.error.HTTPError as e:
                self.status_label.config(text=f"下载失败！HTTP错误: {str(e)}")
            except Exception as e:
                self.status_label.config(text=f"下载失败！发生错误: {str(e)}")
            finally:
                # 重新启用控件
                self.enable_controls()

        # 禁用控件
        self.disable_controls()

        # 创建和启动下载线程
        t = threading.Thread(target=download_thread)
        t.start()

    def disable_controls(self):
        # 禁用相关控件
        self.url_entry.config(state="disabled")
        self.path_entry.config(state="disabled")
        self.path_button.config(state="disabled")
        self.auto_filename_checkbox.config(state="disabled")
        self.download_button.config(state="disabled")

    def enable_controls(self):
        # 重新启用相关控件
        self.url_entry.config(state="normal")
        self.path_entry.config(state="normal")
        self.path_button.config(state="normal")
        self.auto_filename_checkbox.config(state="normal")
        self.download_button.config(state="normal")

def main():
    root = tk.Tk()
    download_engine = DownloadEngine(root)
    root.mainloop()

if __name__ == "__main__":
    main()
