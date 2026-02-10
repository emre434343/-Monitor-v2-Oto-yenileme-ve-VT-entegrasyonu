import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import threading
import webbrowser
import os

class UsomPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("USOM Siber Tehdit Takip Paneli PRO")
        self.root.geometry("1000x700")
        self.root.configure(bg="#121212")

        # Değişkenler
        self.all_data = []
        self.marquee_text = "Veriler yükleniyor..."
        
        # --- ÜST PANEL ---
        self.top_frame = tk.Frame(root, bg="#1f1f1f", height=60)
        self.top_frame.pack(fill="x", side="top")
        
        self.title_label = tk.Label(self.top_frame, text="🛡️ USOM PRO MONITOR", fg="#00ff00", bg="#1f1f1f", font=("Segoe UI", 16, "bold"))
        self.title_label.pack(side="left", padx=20)
        
        self.clock_label = tk.Label(self.top_frame, text="", fg="#00d4ff", bg="#1f1f1f", font=("Consolas", 12))
        self.clock_label.pack(side="right", padx=20)

        # --- ARAÇ ÇUBUĞU ---
        self.toolbar = tk.Frame(root, bg="#121212", pady=10)
        self.toolbar.pack(fill="x")
        
        tk.Label(self.toolbar, text="🔍 Filtre:", fg="white", bg="#121212").pack(side="left", padx=10)
        self.search_entry = tk.Entry(self.toolbar, width=25, bg="#2a2a2a", fg="white", insertbackground="white")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda event: self.filter_data()) # Yazdıkça ara

        self.btn_report = tk.Button(self.toolbar, text="💾 Raporu Kaydet", command=self.save_report, bg="#28a745", fg="white", relief="flat")
        self.btn_report.pack(side="left", padx=10)

        self.status_label = tk.Label(self.toolbar, text="Oto-Yenileme Aktif (5dk)", fg="#888", bg="#121212", font=("Arial", 9))
        self.status_label.pack(side="right", padx=15)

        # --- VERİ TABLOSU ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", borderwidth=0)
        self.style.map("Treeview", background=[('selected', '#007acc')])

        columns = ("id", "url", "type", "date")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("url", text="Zararlı Adres / URL (VT için Tıkla)")
        self.tree.heading("type", text="Tip")
        self.tree.heading("date", text="Tespit Tarihi")
        
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("url", width=450)
        self.tree.column("type", width=100, anchor="center")
        self.tree.column("date", width=180, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10)
        
        self.tree.bind("<Double-1>", self.open_virus_total) # Çift tıklama VT açar

        # --- KAYAN YAZI ---
        self.marquee_frame = tk.Frame(root, bg="#c00", height=25)
        self.marquee_frame.pack(fill="x", side="bottom")
        self.marquee_label = tk.Label(self.marquee_frame, text="", fg="white", bg="#c00", font=("Arial", 10, "bold"))
        self.marquee_label.place(x=1000, y=2)

        # Başlatıcılar
        self.update_clock()
        self.auto_refresh_loop() # Oto yenileme döngüsü
        self.animate_marquee()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def fetch_data(self):
        try:
            response = requests.get("https://www.usom.gov.tr/api/address/index", timeout=10)
            data = response.json()
            self.all_data = data.get('models', [])
            self.update_table(self.all_data)
            
            latest = [item['url'] for item in self.all_data[:8]]
            self.marquee_text = " [KRİTİK TEHDİTLER] " + " • ".join(latest)
        except Exception as e:
            print(f"Veri çekme hatası: {e}")

    def auto_refresh_loop(self):
        self.fetch_data()
        # 300.000 ms = 5 dakika
        self.root.after(300000, self.auto_refresh_loop)

    def update_table(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in data_list:
            self.tree.insert("", "end", values=(item['id'], item['url'], item['type'], item['date']))

    def filter_data(self):
        query = self.search_entry.get().lower()
        filtered = [item for item in self.all_data if query in item['url'].lower() or query in item['type'].lower()]
        self.update_table(filtered)

    def save_report(self):
        try:
            filename = "tehditler.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"USOM TEHDİT RAPORU - {datetime.now()}\n")
                f.write("-" * 50 + "\n")
                for item in self.all_data:
                    f.write(f"ID: {item['id']} | Adres: {item['url']} | Tip: {item['type']} | Tarih: {item['date']}\n")
            messagebox.showinfo("Başarılı", f"Rapor '{filename}' olarak kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilemedi: {e}")

    def open_virus_total(self, event):
        item_id = self.tree.selection()[0]
        url_to_check = self.tree.item(item_id)['values'][1]
        # VirusTotal arama linki (URL arama için)
        vt_url = f"https://www.virustotal.com/gui/search/{url_to_check}"
        webbrowser.open(vt_url)

    def animate_marquee(self):
        current_x = self.marquee_label.winfo_x()
        if current_x < -2000:
            current_x = self.root.winfo_width()
        self.marquee_label.place(x=current_x - 2, y=2)
        self.marquee_label.config(text=self.marquee_text)
        self.root.after(20, self.animate_marquee)

if __name__ == "__main__":
    root = tk.Tk()
    app = UsomPanel(root)
    root.mainloop()