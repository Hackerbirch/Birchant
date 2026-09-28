import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
import threading
import psutil

KEYWORDS = [
    "keylogger",
    "webhook",
    "token",
    "stealer"
]

class SecurityScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("birchantv")
        self.root.geometry("800x600")

        self.folder = ""

        tk.Button(root, text="Вибрати папку",
                  command=self.select_folder).pack(pady=5)

        tk.Button(root, text="Сканувати файли",
                  command=self.start_file_scan).pack(pady=5)

        tk.Button(root, text="Показати процеси",
                  command=self.show_processes).pack(pady=5)

        self.output = scrolledtext.ScrolledText(root)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def select_folder(self):
        self.folder = filedialog.askdirectory()
        if self.folder:
            self.log(f"Обрано: {self.folder}")

    def start_file_scan(self):
        if not self.folder:
            self.log("Спочатку вибери папку.")
            return

        threading.Thread(target=self.scan_files,
                         daemon=True).start()

    def scan_files(self):
        self.log("Початок сканування...")

        for root_dir, dirs, files in os.walk(self.folder):
            for file in files:
                path = os.path.join(root_dir, file)

                try:
                    with open(path, "r",
                              encoding="utf-8",
                              errors="ignore") as f:
                        data = f.read().lower()

                    for word in KEYWORDS:
                        if word in data:
                            self.log(
                                f"Підозріле слово '{word}' у файлі:\n{path}"
                            )
                            break

                except:
                    pass

        self.log("Сканування завершено.")

    def show_processes(self):
        self.log("\n=== Запущені процеси ===")

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                self.log(
                    f"PID: {proc.info['pid']} | "
                    f"{proc.info['name']}"
                )
            except:
                pass

        self.log("=== Кінець списку ===\n")

root = tk.Tk()
app = SecurityScanner(root)
root.mainloop()
