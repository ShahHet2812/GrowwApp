import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import time
sectors = {
    "Technology": {"AAPL": 0.2, "MSFT": 0.2, "GOOGL": 0.2, "NVDA": 0.2, "META": 0.2},
    "Healthcare": {"PFE": 0.3, "JNJ": 0.3, "MRNA": 0.4},
    "Automotive": {"TSLA": 0.4, "F": 0.3, "GM": 0.3},
    "Ecommerce": {"AMZN": 0.5, "EBAY": 0.3, "ETSY": 0.2}
}
class User:
    def __init__(self, name, email, password, phone_number, balance=0):
        self.name = name
        self.email = email
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.phone_number = phone_number
        self.balance = balance
        self.portfolio = {}
        self.watchlist = set()
    def check_password(self, password_attempt):
        hashed_attempt = hashlib.sha256(password_attempt.encode()).hexdigest()
        return hashed_attempt == self.password
    def add_money(self, amount):
        if amount <= 0:
            print("Amount must be positive.")
            return False
        self.balance += amount
        print(f"Successfully added ${amount}. New balance: ${self.balance}")
        return True
    def withdraw_money(self, amount):
        if amount <= 0:
            print("Amount must be positive.")
            return False
        if amount > self.balance:
            print(f"Insufficient funds. Current balance: ${self.balance}")
            return False
        self.balance -= amount
        print(f"Successfully withdrew ${amount}. New balance: ${self.balance}")
        return True
    def get_details(self):
        return (self.email, self.password, self.phone_number, self.balance, self.portfolio)
    def update_details(self, email=None, password=None, phone_number=None):
        if email:
            self.email = email
        if password:
            self.password = hashlib.sha256(password.encode()).hexdigest()
        if phone_number:
            self.phone_number = phone_number
        print("User details updated successfully.")
class GrowX:
    def __init__(self, user):
        self.user = user
        self.running = True
    def display_menu(self):
        print("\n" + "=" * 40)
        print("GROWX STOCK TRADING PLATFORM".center(40))
        print("=" * 40)
        print(f"Welcome, {self.user.name}!")
        print(f"Current Balance: ${self.user.balance}")
        print("-" * 40)
        print("1. Add Money")
        print("2. Withdraw Money")
        print("3. View Stock")
        print("4. Buy Stock")
        print("5. Sell Stock")
        print("6. Calculate Portfolio Value")
        print("7. SIP Investment")
        print("8. Stock Recommendations")
        print("9. Manage Watchlist")
        print("10. Logout")
        print("11. Exit")
        print("-" * 40)
    def add_money(self):
        try:
            amount = float(input("Enter amount to add: $"))
            self.user.add_money(amount)
        except ValueError:
            print("Please enter a valid amount.")
    def withdraw_money(self):
        try:
            amount = float(input("Enter amount to withdraw: $"))
            self.user.withdraw_money(amount)
        except ValueError:
            print("Please enter a valid amount.")
    
    def view_stock(self):
        ticker = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if 'regularMarketPrice' not in info:
                print(f"Could not find data for ticker: {ticker}")
                return
        except Exception as e:
            print(f"Error retrieving stock data: {e}")
            return
        print("\nSelect time period:")
        print("1. 1 Day")
        print("2. 5 Days")
        print("3. 1 Month")
        print("4. 1 Year")
        print("5. 5 Years")
        choice = input("Enter your choice (1-5): ")
        periods = {
            '1': '1d',
            '2': '5d',
            '3': '1mo',
            '4': '1y',
            '5': '5y'
        }
        if choice in periods:
            period = periods[choice]
            try:
                hist = stock.history(period=period)
                if hist.empty:
                    print(f"No data available for {ticker} for the selected period.")
                    return
                plt.figure(figsize=(8, 8))
                plt.plot(hist.index, hist['Close'])
                plt.title(f"{ticker} Stock Price - {period}")
                plt.xlabel('Date')
                plt.ylabel('Price ($)')
                plt.grid(True)
                plt.tight_layout()
                plt.show()
                latest_price = hist['Close'].iloc[-1]
                print(f"\nLatest price for {ticker}: ${latest_price:.2f}")
            except Exception as e:
                print(f"Error plotting stock data: {e}")
        else:
            print("Invalid choice.")
    
    def buy_stock(self):
        ticker = input("Enter stock ticker to buy (e.g., AAPL): ").upper()
        
        try:
            # Get stock information
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if 'regularMarketPrice' not in info:
                print(f"Could not find data for ticker: {ticker}")
                return
            
            current_price = info['regularMarketPrice']
            print(f"Current price of {ticker}: ${current_price:.2f}")
            
            # Ask for quantity
            try:
                quantity = int(input("Enter number of shares to buy: "))
                if quantity <= 0:
                    print("Quantity must be positive.")
                    return
            except ValueError:
                print("Please enter a valid quantity.")
                return
            
            # Calculate total cost
            total_cost = current_price * quantity
            
            # Check if user has enough balance
            if total_cost > self.user.balance:
                print(f"Insufficient funds. Required: ${total_cost:.2f}, Available: ${self.user.balance:.2f}")
                return
            
            # Update user's balance
            self.user.balance -= total_cost
            
            # Update portfolio
            if ticker in self.user.portfolio:
                existing_quantity, avg_price, existing_investment = self.user.portfolio[ticker]
                new_quantity = existing_quantity + quantity
                new_investment = existing_investment + total_cost
                new_avg_price = new_investment / new_quantity
                self.user.portfolio[ticker] = (new_quantity, new_avg_price, new_investment)
            else:
                self.user.portfolio[ticker] = (quantity, current_price, total_cost)
            
            print(f"Successfully purchased {quantity} shares of {ticker} for ${total_cost:.2f}")
            print(f"New balance: ${self.user.balance:.2f}")
            
        except Exception as e:
            print(f"Error during purchase: {e}")
    
    def sell_stock(self):
        if not self.user.portfolio:
            print("You don't own any stocks to sell.")
            return
        
        # Display current portfolio
        print("\nYour Portfolio:")
        for ticker, (quantity, avg_price, investment) in self.user.portfolio.items():
            print(f"{ticker}: {quantity} shares, avg price: ${avg_price:.2f}, total investment: ${investment:.2f}")
        
        ticker = input("\nEnter stock ticker to sell (e.g., AAPL): ").upper()
        
        if ticker not in self.user.portfolio:
            print(f"You don't own any shares of {ticker}.")
            return
        
        # Get owned quantity
        owned_quantity, avg_price, investment = self.user.portfolio[ticker]
        
        try:
            # Ask for quantity to sell
            quantity_to_sell = int(input(f"Enter number of shares to sell (max {owned_quantity}): "))
            
            if quantity_to_sell <= 0:
                print("Quantity must be positive.")
                return
            
            if quantity_to_sell > owned_quantity:
                print(f"You only own {owned_quantity} shares of {ticker}.")
                return
            
            # Get current price
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info['regularMarketPrice']
                print(f"Current price of {ticker}: ${current_price:.2f}")
            except Exception as e:
                print(f"Error retrieving current price: {e}")
                return
            
            # Calculate sale value
            sale_value = current_price * quantity_to_sell
            
            # Calculate profit/loss
            cost_basis = avg_price * quantity_to_sell
            profit_loss = sale_value - cost_basis
            
            # Update portfolio
            if quantity_to_sell == owned_quantity:
                # Remove stock from portfolio if selling all shares
                del self.user.portfolio[ticker]
            else:
                # Update quantity and investment, keep avg_price the same
                new_quantity = owned_quantity - quantity_to_sell
                new_investment = investment - (avg_price * quantity_to_sell)
                self.user.portfolio[ticker] = (new_quantity, avg_price, new_investment)
            
            # Update balance
            self.user.balance += sale_value
            
            print(f"\nSuccessfully sold {quantity_to_sell} shares of {ticker} for ${sale_value:.2f}")
            if profit_loss > 0:
                print(f"You made a profit of ${profit_loss:.2f}")
            else:
                print(f"You took a loss of ${-profit_loss:.2f}")
            print(f"New balance: ${self.user.balance:.2f}")
            
        except ValueError:
            print("Please enter a valid quantity.")
        except Exception as e:
            print(f"Error during sale: {e}")
    
    def calculate_portfolio(self):
        if not self.user.portfolio:
            print("You don't own any stocks.")
            return
        
        total_current_value = 0
        total_investment = 0
        
        print("\n" + "=" * 60)
        print("PORTFOLIO SUMMARY".center(60))
        print("=" * 60)
        print(f"{'Stock':<10} {'Shares':<10} {'Avg Price':<15} {'Current':<15} {'Value':<15} {'P/L':<15}")
        print("-" * 60)
        
        # For pie chart
        stock_values = {}
        
        for ticker, (quantity, avg_price, investment) in self.user.portfolio.items():
            try:
                # Get current price
                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info['regularMarketPrice']
                
                current_value = current_price * quantity
                profit_loss = current_value - investment
                profit_loss_percent = (profit_loss / investment) * 100 if investment > 0 else 0
                
                print(f"{ticker:<10} {quantity:<10} ${avg_price:<14.2f} ${current_price:<14.2f} ${current_value:<14.2f} ${profit_loss:<10.2f} ({profit_loss_percent:+.2f}%)")
                total_current_value += current_value
                total_investment += investment
                stock_values[ticker] = current_value
            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")
        print("-" * 60)
        total_profit_loss = total_current_value - total_investment
        total_profit_loss_percent = (total_profit_loss / total_investment) * 100 if total_investment > 0 else 0
        print(f"{'TOTAL':<10} {'':<10} {'':<15} {'':<15} ${total_current_value:<14.2f} ${total_profit_loss:<10.2f} ({total_profit_loss_percent:+.2f}%)")
        print("=" * 60)
        print(f"Cash Balance: ${self.user.balance:.2f}")
        print(f"Total Account Value: ${(total_current_value + self.user.balance):.2f}")
        print("=" * 60)
        if stock_values:
            plt.figure(figsize=(8, 6))
            plt.pie(stock_values.values(), labels=stock_values.keys(), autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
            plt.title(f"{self.user.name}'s Portfolio Distribution")
            plt.axis("equal")
            plt.show()
    
    def sip_investment(self):
        print("Available Sectors: ")
        for sector in sectors:
            print(sector) 
        choice = input("Choose a sector to invest in: ").capitalize()
        if choice not in sectors:
            print("Invalid sector selection.")
            return
        try:
            amount = float(input("Enter monthly investment amount: "))
            if amount > self.user.balance:
                print(f"Insufficient funds. Required: ${amount:.2f}, Available: ${self.user.balance:.2f}")
                return
                
            allocation = sectors[choice]
            print(f"Investing ${amount:.2f} in {choice} sector.")
            
            total_invested = 0
            
            for ticker, percentage in allocation.items():
                invest_amount = amount * percentage
                try:
                    stock = yf.Ticker(ticker)
                    price = stock.history(period="1d")["Close"][-1]
                    quantity = invest_amount // price
                    
                    if quantity > 0:
                        total_cost = quantity * price
                        total_invested += total_cost
                        
                        # Update portfolio
                        if ticker in self.user.portfolio:
                            existing_quantity, avg_price, existing_investment = self.user.portfolio[ticker]
                            new_quantity = existing_quantity + quantity
                            new_investment = existing_investment + total_cost
                            new_avg_price = new_investment / new_quantity
                            self.user.portfolio[ticker] = (new_quantity, new_avg_price, new_investment)
                        else:
                            self.user.portfolio[ticker] = (quantity, price, total_cost)
                        print(f"Bought {int(quantity)} shares of {ticker} at ${price:.2f} each. Total: ${total_cost:.2f}")
                except Exception as e:
                    print(f"Error fetching data for {ticker}: {str(e)}")
            self.user.balance -= total_invested
            print(f"SIP investment completed! Total invested: ${total_invested:.2f}")
            print(f"New balance: ${self.user.balance:.2f}")
            
        except ValueError:
            print("Please enter a valid amount.")
    
    def stock_recommendation(self):
        print("\nStock Recommendations\n")
        stock_list = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA", "PFE", "JNJ", "MRNA", "F", "GM"]
        recommendations = []

        for ticker in stock_list:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1y")
                if hist.empty:
                    continue
                hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
                hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
                
                latest_price = hist['Close'][-1]
                sma_20 = hist['SMA_20'][-1]
                sma_50 = hist['SMA_50'][-1]

                # Rule-based recommendation:
                # - If SMA_20 > SMA_50, the stock is in an uptrend
                # - If SMA_20 < SMA_50, the stock is in a downtrend
                if sma_20 > sma_50:
                    recommendations.append((ticker, latest_price, "Strong Buy"))
                elif sma_20 < sma_50:
                    recommendations.append((ticker, latest_price, "Avoid"))
                else:
                    recommendations.append((ticker, latest_price, "Neutral"))

            except Exception as e:
                print(f"Error fetching data for {ticker}: {str(e)}")
                
        if recommendations:
            print("\nRecommended Stocks:")
            for stock in recommendations:
                print(f"{stock[0]} - ${stock[1]:.2f} - {stock[2]}")
        else:
            print("No recommendations available.")
    
    def add_to_watchlist(self):
        ticker = input("Enter stock ticker to add to watchlist: ").upper()
        self.user.watchlist.add(ticker)
        print(f"{ticker} added to your watchlist.")
    
    def remove_from_watchlist(self):
        ticker = input("Enter stock ticker to remove from watchlist: ").upper()
        if ticker in self.user.watchlist:
            self.user.watchlist.remove(ticker)
            print(f"{ticker} removed from your watchlist.")
        else:
            print("Stock not found in your watchlist.")
    
    def view_watchlist(self):
        if not self.user.watchlist:
            print("Your watchlist is empty.")
            return
        
        print("\nYour Watchlist:")
        for ticker in self.user.watchlist:
            try:
                stock = yf.Ticker(ticker)
                price = stock.history(period="1d")["Close"][-1]
                print(f"{ticker}: ${price:.2f}")
            except Exception as e:
                print(f"Error fetching price for {ticker}: {str(e)}")
    
    def manage_watchlist(self):
        while True:
            print("\nWatchlist Menu:")
            print("1. View Watchlist")
            print("2. Add Stock to Watchlist")
            print("3. Remove Stock from Watchlist")
            print("4. Back to Main Menu")
            
            choice = input("Enter your choice: ")
            if choice == "1":
                self.view_watchlist()
            elif choice == "2":
                self.add_to_watchlist()
            elif choice == "3":
                self.remove_from_watchlist()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Try again.")
    
    def logout(self):
        confirm = input("Are you sure you want to logout? (y/n): ").lower()
        if confirm == 'y':
            print(f"Goodbye, {self.user.name}!")
            self.running = False
    
    def exit_app(self):
        confirm = input("Are you sure you want to exit the application? (y/n): ").lower()
        if confirm == 'y':
            print("Thank you for using Stock Market App. Goodbye!")
            self.running = False
            return True  # Signal to completely exit the app
        return False
    
    def run(self):
        while self.running:
            self.display_menu()
            choice = input("Enter your choice (1-11): ")
            
            actions = {
                '1': self.add_money,
                '2': self.withdraw_money,
                '3': self.view_stock,
                '4': self.buy_stock,
                '5': self.sell_stock,
                '6': self.calculate_portfolio,
                '7': self.sip_investment,
                '8': self.stock_recommendation,
                '9': self.manage_watchlist,
                '10': self.logout,
                '11': self.exit_app
            }
            
            if choice in actions:
                actions[choice]()
            else:
                print("Invalid choice. Please try again.")
            time.sleep(1)
        
        return False
class StockMarketApp:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.running = True
    def display_welcome(self):
        print("\n" + "=" * 40)
        print("WELCOME TO STOCK MARKET APP".center(40))
        print("=" * 40)
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        print("-" * 40)
    def login(self):
        name = input("Enter your name: ")
        if name not in self.users:
            print("User not found. Please sign up first.")
            return
        password = input("Enter your password: ")
        user = self.users[name]
        if user.check_password(password):
            print(f"Welcome back, {name}!")
            self.current_user = user
            platform = GrowX(user)
            if platform.run():
                self.running = False
        else:
            print("Incorrect password. Please try again.")
    def signup(self):
        name = input("Enter your name: ")
        if name in self.users:
            print("User already exists. Please use a different name or login.")
            return
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        phone_number = input("Enter your phone number: ")
        user = User(name, email, password, phone_number)
        self.users[name] = user
        print(f"Account created successfully. Welcome, {name}!")
        try:
            initial_deposit = input("Would you like to add initial funds? (y/n): ").lower()
            if initial_deposit == 'y':
                amount = float(input("Enter amount to deposit: $"))
                user.add_money(amount)
        except ValueError:
            print("Invalid amount. No funds added.")
        self.current_user = user
        platform = GrowX(user)
        if platform.run():
            self.running = False
    def exit_app(self):
        print("Thank you for using Stock Market App. Goodbye!")
        self.running = False
    def run(self):
        print("Starting Stock Market App...")
        while self.running:
            self.display_welcome()
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                self.login()
            elif choice == '2':
                self.signup()
            elif choice == '3':
                self.exit_app()
            else:
                print("Invalid choice. Please try again.")
            time.sleep(1)
if __name__ == "__main__":
    app = StockMarketApp()
    app.run()