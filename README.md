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
### 1. Clone or Download the Repository
```bash
git clone [https://github.com/kok-sk/PyStockSim.git](https://github.com/kok-sk/PyStockSim.git)
cd PyStockSim

### 2. Install Required Packages
Make sure you have Python installed, then run the environment setup:
pip install yfinance pandas matplotlib

### 3. Initialize Local User Data (Optional)
If you want to bypass manual registration inside the application UI, you can directly initialize a pre-configured profile. Create a file named portfolio.json in the project root folder and paste the following mock structure:
{
    "GuestUser": {
        "balance": 10000.0,
        "currency": "SK",
        "holdings": {},
        "buy_prices": {}
    }
}

### 4. Launch the Simulator
python stock_trading_simulator.py
