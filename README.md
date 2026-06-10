# PyStockSim Terminal
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

## 🚀 Quick Start
```bash
# Step 1: Clone the repository and enter the project folder
git clone [https://github.com/kok-sk/PyStockSim.git](https://github.com/kok-sk/PyStockSim.git)
cd PyStockSim

# Step 2: Install required packages
pip install yfinance pandas matplotlib

# Step 3: (Optional) Initialize Local User Data
# If you want to bypass the registration UI, create 'portfolio.json' manually with your account data, for example:
{
    "GuestUser": {
        "balance": 10000.0,
        "currency": "SK",
        "holdings": {},
        "buy_prices": {}
    }
}

# Step 4: Launch the Simulator
python stock_trading_simulator.py
