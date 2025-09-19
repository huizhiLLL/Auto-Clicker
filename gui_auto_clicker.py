import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import keyboard
import time
import threading
import sys

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # 初始化自动点击器核心功能
        self.running = False
        self.paused = False
        self.click_thread = None
        self.click_interval = 0.7  # 默认点击间隔为0.7秒
        self.click_button = 'left'  # 默认使用左键点击
        
        # 创建界面
        self.create_widgets()
        
        # 设置热键
        self.setup_hotkeys()
        
        # 确保程序退出时清理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="Auto Clicker Tool", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 点击间隔设置
        interval_frame = ttk.LabelFrame(main_frame, text="Click Interval", padding="10")
        interval_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(interval_frame, text="Interval (seconds):").grid(row=0, column=0, sticky=tk.W)
        self.interval_var = tk.DoubleVar(value=self.click_interval)
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var, width=10)
        interval_entry.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        interval_entry.bind('<Return>', lambda e: self.update_interval())
        
        ttk.Button(interval_frame, text="Update Interval", command=self.update_interval).grid(row=0, column=2, padx=(10, 0))
        
        # 点击按键设置
        button_frame = ttk.LabelFrame(main_frame, text="Click Button", padding="10")
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(button_frame, text="Select button:").grid(row=0, column=0, sticky=tk.W)
        
        self.button_var = tk.StringVar(value=self.click_button)
        button_combo = ttk.Combobox(button_frame, textvariable=self.button_var, 
                                   values=['left', 'right', 'middle', 'space'], 
                                   state="readonly", width=10)
        button_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        button_combo.bind('<<ComboboxSelected>>', lambda e: self.update_button())
        
        ttk.Button(button_frame, text="Update Button", command=self.update_button).grid(row=0, column=2, padx=(10, 0))
        
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start (F6)", command=self.toggle_start_stop)
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.pause_button = ttk.Button(control_frame, text="Pause (F8)", command=self.toggle_pause_resume, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=(5, 5))
        
        self.stop_button = ttk.Button(control_frame, text="Stop (F9)", command=self.stop_clicking, state="disabled")
        self.stop_button.grid(row=0, column=2, padx=(5, 0))
        
        # 状态显示
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0)
        
        # 热键说明
        hotkey_frame = ttk.LabelFrame(main_frame, text="Hotkey Instructions", padding="10")
        hotkey_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(hotkey_frame, text="F6: Start/Stop auto click").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(hotkey_frame, text="F8: Pause/Resume auto click").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(hotkey_frame, text="F9: Stop auto click").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(hotkey_frame, text="Esc: Exit program").grid(row=3, column=0, sticky=tk.W)

    def setup_hotkeys(self):
        keyboard.add_hotkey('f6', self.toggle_start_stop)
        keyboard.add_hotkey('f8', self.toggle_pause_resume)
        keyboard.add_hotkey('f9', self.stop_clicking)
        keyboard.add_hotkey('esc', self.on_closing)

    def update_interval(self):
        try:
            new_interval = float(self.interval_var.get())
            if new_interval <= 0:
                messagebox.showerror("Error", "Interval time must be greater than 0")
                return False
            self.click_interval = new_interval
            self.status_var.set(f"Click interval updated to {self.click_interval} seconds")
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid interval time, please enter a valid number")
            return False

    def update_button(self):
        button = self.button_var.get()
        if button in ['left', 'right', 'middle', 'space']:
            self.click_button = button
            if self.click_button == 'space':
                self.status_var.set("Click button changed to space key")
            else:
                self.status_var.set(f"Click button changed to {self.click_button}")
            return True
        else:
            messagebox.showerror("Error", "Invalid button")
            return False

    def toggle_start_stop(self):
        if not self.running:
            self.start_clicking()
        else:
            self.stop_clicking()

    def toggle_pause_resume(self):
        self.paused = not self.paused
        status = "paused" if self.paused else "resumed"
        self.status_var.set(f"Auto click {status}")
        self.pause_button.config(text=f"{'Resume' if self.paused else 'Pause'} (F8)")

    def start_clicking(self):
        if self.running:
            return
        
        self.running = True
        self.paused = False
        self.start_button.config(text="Start (F6)", state="disabled")
        self.pause_button.config(text="Pause (F8)", state="normal")
        self.stop_button.config(state="normal")
        
        if self.click_button == 'space':
            self.status_var.set(f"Auto click started - Interval: {self.click_interval}s, Button: space key")
        else:
            self.status_var.set(f"Auto click started - Interval: {self.click_interval}s, Button: {self.click_button}")
        
        self.click_thread = threading.Thread(target=self.clicking_loop)
        self.click_thread.daemon = True
        self.click_thread.start()

    def stop_clicking(self):
        self.running = False
        self.paused = False
        self.start_button.config(text="Start (F6)", state="normal")
        self.pause_button.config(text="Pause (F8)", state="disabled")
        self.stop_button.config(state="disabled")
        self.status_var.set("Auto click stopped")

    def clicking_loop(self):
        while self.running:
            if not self.paused:
                if self.click_button == 'space':
                    pyautogui.press('space')
                else:
                    pyautogui.click(button=self.click_button)
            time.sleep(self.click_interval)

    def on_closing(self):
        self.running = False
        self.root.destroy()
        sys.exit(0)

def main():
    root = tk.Tk()
    app = AutoClickerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()