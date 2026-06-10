# PyStockSim Terminal
![Good First Project](https://img.shields.io/badge/Good_First_Project-Yes-orange)
![Beginner Friendly](https://img.shields.io/badge/Beginner-Friendly-brightgreen)

A feature-rich Python stock trading simulator featuring a modern dark-mode Tkinter GUI. Engineered with `yfinance` for live market data, `Matplotlib` for technical charts, multi-threading for real-time price alerts, and `pandas` for CSV data export.

---

## ✨ Features
* **Multi-User Authentication**: Register, login, and manage separate local virtual accounts securely.
* **Live Price Tracking**: Fetches instantaneous real-time stock data directly using the Yahoo Finance API.
* **Intelligent Order Execution**: Automatically tracks share quantities and computes your exact holding average cost dynamically.
* **Advanced Data Visualization**: Built-in 30-day historical technical charts and interactive multi-stock trends comparisons.
* **Asynchronous Price Alerts**: Background multi-threaded price monitors watch the market and pop warning messages when goals are hit without lagging the UI.
* **Data Portability**: Export your personal holding matrices directly to spreadsheet-ready CSV files with one click.

---

## 🛠️ Tech Stack & Dependencies
* **GUI Framework**: Tkinter
* **Financial Data Engine**: `yfinance`
* **Data Processing**: `pandas`
* **Plotting & Canvas Integration**: `matplotlib`
* **Storage format**: JSON Data Persistence (`portfolio.json`)

---

# 🚀 Quick Start
## Step 1: Clone the Repository

```bash
git clone https://github.com/kok-sk/PyStockSim.git
cd PyStockSim
```

## Step 2: Install Required Packages

```bash
pip install yfinance pandas matplotlib
```

## Step 3: Initialize Local User Data (Optional)

If you want to bypass the registration UI, create `portfolio.json` manually:

```json
{
    "GuestUser": {
        "balance": 10000.0,
        "currency": "SK",
        "holdings": {},
        "buy_prices": {}
    }
}
```

## Step 4: Launch the Simulator

```bash
python stock_trading_simulator.py
```
