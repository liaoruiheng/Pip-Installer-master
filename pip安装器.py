import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox

class PipInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pip Installer")

        self.mirror_sources = [
            "默认源 https://pypi.org/simple",
            "清华大学源 https://pypi.tuna.tsinghua.edu.cn/simple",
            "阿里云源 https://mirrors.aliyun.com/pypi/simple",
            "豆瓣源 https://pypi.douban.com/simple",
            "华中科技大学源 https://pypi.hust.edu.cn/simple"
        ]

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="选择镜像源:").grid(column=0, row=0, padx=10, pady=10)
        self.mirror_combobox = ttk.Combobox(self.root, values=self.mirror_sources)
        self.mirror_combobox.grid(column=1, row=0)
        self.mirror_combobox.current(0)

        ttk.Label(self.root, text="输入库名:").grid(column=0, row=1, padx=10, pady=10)
        self.package_name = ttk.Entry(self.root)
        self.package_name.grid(column=1, row=1)

        self.install_button = ttk.Button(self.root, text="安装", command=self.install_package)
        self.install_button.grid(column=0, row=2, padx=10, pady=10)

        self.uninstall_button = ttk.Button(self.root, text="卸载", command=self.uninstall_package)  # 新增卸载按钮
        self.uninstall_button.grid(column=1, row=2, padx=10, pady=10)  # 设置在右边

        self.command_button = ttk.Button(self.root, text="生成命令", command=self.generate_command)
        self.command_button.grid(column=2, row=2)

        self.command_output = tk.Text(self.root, height=5, width=50)
        self.command_output.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

        self.hide_cmd_var = tk.BooleanVar()
        self.hide_cmd_checkbox = ttk.Checkbutton(self.root, text="隐藏 CMD", variable=self.hide_cmd_var)
        self.hide_cmd_checkbox.grid(column=0, row=4, columnspan=3, pady=10)

        self.permanent_button = ttk.Button(self.root, text="永久设置镜像源", command=self.permanently_set_mirror)
        self.permanent_button.grid(column=0, row=5, columnspan=3, pady=10)

    def install_package(self):
        package = self.package_name.get().strip()
        if not package:
            messagebox.showwarning("警告", "请输入库名！")
            return
        mirror = self.mirror_combobox.get()
        command = f"pip install -i {mirror.split(' ')[-1]} {package}"
        self.run_command(command)

    def uninstall_package(self):  # 新增卸载方法
        package = self.package_name.get().strip()
        if not package:
            messagebox.showwarning("警告", "请输入库名！")
            return
        command = f"pip uninstall -y {package}"  # 使用 -y 选项自动确认卸载
        self.run_command(command)

    def generate_command(self):
        package = self.package_name.get().strip()
        if not package:
            messagebox.showwarning("警告", "请输入库名！")
            return
        mirror = self.mirror_combobox.get()
        command = f"pip install -i {mirror.split(' ')[-1]} {package}"
        self.command_output.delete(1.0, tk.END)
        self.command_output.insert(tk.END, command)

    def permanently_set_mirror(self):
        selected_mirror = self.mirror_combobox.get()
        mirror_url = selected_mirror.split(' ')[-1]

        command = f"pip config set global.index-url {mirror_url}"
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            messagebox.showinfo("信息", "已设置镜像源为: " + mirror_url)
        except subprocess.CalledProcessError as e:
            error_output = e.output.decode('utf-8', errors='ignore')
            messagebox.showerror("错误", f"设置镜像源失败:\n{error_output}")

    def run_command(self, command):
        # 如果选择隐藏CMD，则在后台运行
        if self.hide_cmd_var.get():
            try:
                # 使用 subprocess.run 执行命令，并捕获输出
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:  # 成功
                    messagebox.showinfo("信息", "命令已在后台进行！")
                else:  # 失败
                    messagebox.showerror("错误", f"命令执行失败:\n{result.stderr}")
            except Exception as e:
                messagebox.showerror("错误", f"执行命令失败:\n{e}")
        else:
            try:
                # 用 start 命令在新窗口中运行，并在完成后自动关闭
                cmd_command = f'start cmd /c {command}'
                subprocess.Popen(cmd_command, shell=True)
                messagebox.showinfo("信息", "命令已在 CMD 窗口中进行！")
            except Exception as e:
                messagebox.showerror("错误", f"执行命令失败:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PipInstallerApp(root)
    root.mainloop()
