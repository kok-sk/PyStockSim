# ---  STOCK TRADING SIMULATOR ---
import tkinter as tk
from tkinter import messagebox, ttk
import yfinance as yf 
import json
import os
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- DATA STORAGE ---
USER_DATA_FILE = "portfolio.json"

def load_all_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_all_users():
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

users_db = load_all_users()
current_user = None
active_alerts = {}

# --- AUTHENTICATION ---
def login_system():
    global current_user
    login_win = tk.Toplevel(root)
    login_win.title("Authentication")
    login_win.geometry("350x250")
    login_win.configure(bg="#1e293b")
    login_win.resizable(False, False)
    
    # Center the window
    login_win.update_idletasks()
    x = (login_win.winfo_screenwidth() // 2) - 175
    y = (login_win.winfo_screenheight() // 2) - 125
    login_win.geometry(f"+{x}+{y}")

    tk.Label(login_win, text="Stock Simulator Terminal", font=("Segoe UI", 14, "bold"), fg="white", bg="#1e293b").pack(pady=(20, 5))
    username_entry = tk.Entry(login_win, bg="#0f172a", fg="white", insertbackground="white", relief="flat", font=("Segoe UI", 11), justify="center")
    username_entry.pack(pady=10, ipady=4, ipadx=10)

    btn_frame = tk.Frame(login_win, bg="#1e293b")
    btn_frame.pack(pady=10)

    def handle_login():
        global current_user
        name = username_entry.get().strip()
        if name in users_db:
            current_user = name
            login_win.destroy()
            update_display()
        else: messagebox.showerror("Error", "User not found.")

    def handle_register():
        name = username_entry.get().strip()
        if name and name not in users_db:
            users_db[name] = {"balance": 10000.0, "currency": "SK", "holdings": {}, "buy_prices": {}}
            save_all_users()
            messagebox.showinfo("Success", "Account Created!")
        else: messagebox.showwarning("Error", "Invalid name or exists.")

    tk.Button(btn_frame, text="Login", command=handle_login, bg="#3b82f6", fg="white", font=("Segoe UI", 10, "bold"), width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Register", command=handle_register, bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"), width=10).pack(side="left", padx=5)
    login_win.grab_set()

# --- FUNCTIONS ---
def get_stock_price(symbol=None):
    ticker = symbol if symbol else ticker_entry.get().upper().strip() 
    if not ticker: return None
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        if symbol is None:
            result_label.config(text=f"Market: {ticker} | Price: {price:.2f} SK", fg="#38bdf8")
        return price
    except: return None

def trade_stock(action):
    ticker = ticker_entry.get().upper().strip() 
    price = get_stock_price(ticker)
    if price is None: return
    try:
        qty = int(quantity_entry.get())
        user_data = users_db[current_user]
        if action == "BUY" and user_data["balance"] >= price * qty:
            user_data["balance"] -= price * qty
            old_qty = user_data["holdings"].get(ticker, 0)
            old_avg = user_data["buy_prices"].get(ticker, price)
            user_data["holdings"][ticker] = old_qty + qty
            user_data["buy_prices"][ticker] = ((old_avg * old_qty) + (price * qty)) / (old_qty + qty)
        elif action == "SELL" and user_data["holdings"].get(ticker, 0) >= qty:
            user_data["balance"] += price * qty
            user_data["holdings"][ticker] -= qty
            if user_data["holdings"][ticker] == 0: 
                del user_data["holdings"][ticker]
                del user_data["buy_prices"][ticker]
        save_all_users(); update_display()
    except: messagebox.showerror("Error", "Invalid Quantity")

def show_chart():
    ticker = ticker_entry.get().upper().strip()
    hist = yf.Ticker(ticker).history(period="30d")
    if hist.empty: return
    fig = plt.Figure(figsize=(7, 3.8), dpi=90, facecolor='#0f172a')
    ax = fig.add_subplot(111); ax.set_facecolor('#1e293b')
    ax.plot(hist.index, hist['Close'], color='#38bdf8', linewidth=2)
    ax.set_title(f"30-Day Trend: {ticker}", color="white", fontsize=10, fontweight="bold")
    ax.tick_params(colors='white', labelsize=9)
    fig.autofmt_xdate(); fig.tight_layout()
    for w in chart_frame.winfo_children(): w.destroy()
    FigureCanvasTkAgg(fig, master=chart_frame).get_tk_widget().pack(fill="both", expand=True)

def compare_stocks():
    tickers = ticker_entry.get().upper().strip().split(",")
    fig = plt.Figure(figsize=(7, 3.8), dpi=90, facecolor='#0f172a')
    ax = fig.add_subplot(111); ax.set_facecolor('#1e293b')
    for t in tickers:
        clean_t = t.strip()
        hist = yf.Ticker(clean_t).history(period="30d")
        if not hist.empty: ax.plot(hist.index, hist['Close'], label=clean_t)
    ax.set_title(f"Comparison: {', '.join(tickers)}", color="white", fontsize=10, fontweight="bold")
    ax.legend(); ax.tick_params(colors='white', labelsize=9)
    fig.autofmt_xdate(); fig.tight_layout()
    for w in chart_frame.winfo_children(): w.destroy()
    FigureCanvasTkAgg(fig, master=chart_frame).get_tk_widget().pack(fill="both", expand=True)

def set_price_alert():
    ticker = ticker_entry.get().upper().strip()
    try:
        target = float(alert_entry.get())
        active_alerts[ticker] = target
        messagebox.showinfo("Alert", f"Monitoring {ticker} for target: {target} SK")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid numeric target price")

def alert_monitor_thread():
    while True:
        if active_alerts:
            for ticker, target in list(active_alerts.items()):
                current = get_stock_price(ticker)
                if current and ((current >= target and target > 0) or (current <= target and target < 0)):
                    messagebox.showinfo("Price Alert", f"{ticker} has reached your target of {target}!")
                    del active_alerts[ticker]
        time.sleep(60)

def export_data():
    if not current_user: return
    data = users_db[current_user]
    df = pd.DataFrame([{"Ticker": t, "Qty": q, "Avg Cost": data["buy_prices"][t]} for t, q in data["holdings"].items()])
    df.to_csv(f"{current_user}_portfolio.csv", index=False)
    messagebox.showinfo("Export", "Portfolio exported to CSV!")

def update_display():
    if not current_user: return
    data = users_db[current_user]
    balance_label.config(text=f"Available Cash: {data['balance']:.2f} SK")
    user_label.config(text=f"Account: {current_user}")
    tree.delete(*tree.get_children())
    total_val = data["balance"]
    for t, q in data["holdings"].items():
        p = get_stock_price(t) or 0
        bp = data.get("buy_prices", {}).get(t, 0)
        pl = (p - bp) * q
        total_val += p * q
        color = "#10b981" if pl >= 0 else "#ef4444"
        tree.insert("", "end", values=(t, q, f"{p:.2f}", f"{bp:.2f}", f"{pl:.2f}"))
    total_label.config(text=f"Total Net Worth: {total_val:.2f} SK")

def logout():
    global current_user
    current_user = None
    login_system()

def delete_account():
    if messagebox.askyesno("Delete", "Delete account permanently?"):
        del users_db[current_user]; save_all_users(); logout()

# --- GUI ---
root = tk.Tk()
root.title("Stock Trading Simulator")
root.geometry("1200x950")
root.configure(bg="#0f172a")

# Sidebar
sidebar = tk.Frame(root, bg="#1e293b", width=260); sidebar.pack(side="left", fill="y"); sidebar.pack_propagate(False)

def add_ui_group(label, entries, buttons):
    tk.Label(sidebar, text=label, fg="#94a3b8", bg="#1e293b", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(15, 2))
    for e_label, e_var in entries:
        tk.Label(sidebar, text=e_label, fg="white", bg="#1e293b", font=("Segoe UI", 8)).pack(anchor="w", padx=20)
        e_var.pack(fill="x", padx=20, pady=2, ipady=3)
    for b_text, b_cmd, b_clr in buttons:
        tk.Button(sidebar, text=b_text, command=b_cmd, bg=b_clr, fg="white", font=("Segoe UI", 10, "bold"), relief="flat").pack(fill="x", padx=20, pady=2)

ticker_entry = tk.Entry(sidebar, bg="#0f172a", fg="white", insertbackground="white", relief="flat")
quantity_entry = tk.Entry(sidebar, bg="#0f172a", fg="white", insertbackground="white", relief="flat")
alert_entry = tk.Entry(sidebar, bg="#0f172a", fg="white", insertbackground="white", relief="flat")

add_ui_group("TRADING", [("Ticker", ticker_entry), ("Qty", quantity_entry)], [("Check Price", get_stock_price, "#64748b"), ("BUY", lambda: trade_stock("BUY"), "#10b981"), ("SELL", lambda: trade_stock("SELL"), "#ef4444")])
add_ui_group("ALERTS", [("Target Price", alert_entry)], [("Set Alert", set_price_alert, "#f59e0b")])
add_ui_group("ANALYSIS", [], [("30-day chart", show_chart, "#3b82f6"), ("Compare Multi-stock", compare_stocks, "#8b5cf6")])
add_ui_group("TOOLS", [], [("Export Data", export_data, "#475569")])

# Content
content = tk.Frame(root, bg="#0f172a"); content.pack(side="right", fill="both", expand=True, padx=25, pady=15)

header = tk.Frame(content, bg="#0f172a"); header.pack(fill="x")
user_label = tk.Label(header, text="Account: ---", fg="#9ca3af", bg="#0f172a", font=("Segoe UI", 11))
user_label.pack(side="left")
tk.Button(header, text="Logout", command=logout, bg="#334155", fg="white", font=("Segoe UI", 8, "bold"), relief="flat").pack(side="left", padx=5)
tk.Button(header, text="Delete Account", command=delete_account, bg="#ef4444", fg="white", font=("Segoe UI", 8, "bold"), relief="flat").pack(side="left", padx=5)

balance_label = tk.Label(content, text="Available Cash: ---", fg="#FFD700", bg="#0f172a", font=("Segoe UI", 22, "bold"))
balance_label.pack(anchor="w", pady=(15, 5))
total_label = tk.Label(content, text="Total Net Worth: ---", fg="white", bg="#0f172a", font=("Segoe UI", 13))
total_label.pack(anchor="w", pady=(0, 10))
result_label = tk.Label(content, text="System Ready", fg="#64748b", bg="#0f172a"); result_label.pack(anchor="w")

# Portfolio Table
style = ttk.Style(); style.theme_use("clam")
style.configure("Treeview", background="#1e293b", foreground="white", fieldbackground="#1e293b", borderwidth=0)
style.configure("Treeview.Heading", background="#334155", foreground="white", font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[('selected', '#3b82f6')])

tree = ttk.Treeview(content, columns=("T", "Q", "P", "BP", "PL"), show='headings', height=10)
for col, name in zip(("T", "Q", "P", "BP", "PL"), ("Ticker", "Shares", "Price", "Avg Cost", "Profit/Loss")):
    tree.heading(col, text=name); tree.column(col, width=120, anchor="center")
tree.pack(fill="x", pady=20)

# Chart Frame
chart_frame = tk.Frame(content, bg="#1e293b", height=420)
chart_frame.pack(fill="both", expand=True, pady=(20, 10))
chart_frame.pack_propagate(False) 

# Start background alert monitor
threading.Thread(target=alert_monitor_thread, daemon=True).start()

root.after(100, login_system)
root.mainloop()