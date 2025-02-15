import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
users = {"het": "2812", "moksh": "1234"}
portfolios = {"het": {}, "moksh": {}}
sectors = {
    "Tech": {"AAPL": 0.4, "MSFT": 0.3, "GOOGL": 0.3},
    "Medical": {"PFE": 0.5, "JNJ": 0.3, "MRNA": 0.2},
    "Automobile": {"TSLA": 0.6, "F": 0.2, "GM": 0.2}
}


def login():
    print("Welcome to Groww-like App")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid credentials.")
        return None

def show_stocks():
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA): ").upper()
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")  # Fetch last month's data
    except Exception as e:
        print("Error fetching data:", str(e))
    else:
        print(f"Showing data for {ticker}:\n", hist.tail())
        
        # Plotting the stock price graph
        hist['Close'].plot(title=f"{ticker} - Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Close Price")
        plt.grid(True)
        plt.show()

def buy_stock(username):
    ticker = input("Enter stock ticker to buy: ").upper()
    quantity = int(input("Enter quantity: "))
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'][-1]  # Latest close price
        cost = price * quantity
        
        portfolios[username][ticker] = portfolios[username].get(ticker, 0) + quantity
        print(f"Bought {quantity} shares of {ticker} at {price:.2f} each. Total cost: {cost:.2f}")
    except Exception as e:
        print("Error buying stock:", str(e))

def sell_stock(username):
    ticker = input("Enter stock ticker to sell: ").upper()
    quantity = int(input("Enter quantity to sell: "))
    if ticker in portfolios[username] and portfolios[username][ticker] >= quantity:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'][-1]  # Latest close price
        proceeds = price * quantity
        portfolios[username][ticker] -= quantity
        if portfolios[username][ticker] == 0:
            del portfolios[username][ticker]
        print(f"Sold {quantity} shares of {ticker} at {price:.2f} each. Total proceeds: {proceeds:.2f}")
    else:
        print("Not enough shares to sell.")

def view_portfolio(username):
    print("Your Portfolio:")
    if portfolios[username]:
        for ticker, qty in portfolios[username].items():
            print(f"{ticker}: {qty} shares")
    else:
        print("Portfolio is empty.")

def sip_investment(username):
    print("Available Sectors: ")
    for sector in sectors:
        print(sector)
    
    choice = input("Choose a sector to invest in: ").capitalize()
    if choice not in sectors:
        print("Invalid sector selection.")
        return
    
    amount = float(input("Enter monthly investment amount: "))
    allocation = sectors[choice]
    
    print(f"Investing ${amount:.2f} in {choice} sector.")
    for ticker, percentage in allocation.items():
        invest_amount = amount * percentage
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"][-1]
        quantity = invest_amount // price
        
        if quantity > 0:
            portfolios[username][ticker] = portfolios[username].get(ticker, 0) + quantity
            print(f"Bought {int(quantity)} shares of {ticker} at {price:.2f} each. Total: ${invest_amount:.2f}")
    print("SIP investment completed!")

def main():
    username = None
    while not username:
        username = login()

    while True:
        print("1. See Stocks")
        print("2. Buy Stocks")
        print("3. Sell Stocks")
        print("4. View Portfolio")
        print("5. Invest in SIP")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            show_stocks()
        elif choice == "2":
            buy_stock(username)
        elif choice == "3":
            sell_stock(username)
        elif choice == "4":
            view_portfolio(username)
        elif choice=="5":
            sip_investment(username)
        elif choice == "6":
            print("Exiting... Thank you for using the app!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
