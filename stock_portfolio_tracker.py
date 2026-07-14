import datetime

# ---------------------------------------------------------
# Predefined stock prices (at least 10 stocks)
# ---------------------------------------------------------
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 320,
    "AMZN": 150,
    "META": 300,
    "NFLX": 450,
    "NVDA": 900,
    "IBM": 170,
    "ORCL": 130
}


# ---------------------------------------------------------
# Function: display_stocks
# Shows all available stock symbols and their prices.
# ---------------------------------------------------------
def display_stocks():
    print("\nAvailable Stocks:")
    print("-" * 30)
    print(f"{'Symbol':<10}{'Price':>10}")
    print("-" * 30)
    for symbol, price in STOCK_PRICES.items():
        print(f"{symbol:<10}{'₹' + str(price):>10}")
    print("-" * 30)


# ---------------------------------------------------------
# Function: add_stock
# Prompts the user to build their portfolio by entering
# stock symbols and quantities. Validates all input and
# handles errors gracefully with try-except.
# Returns a dictionary: {symbol: quantity}
# ---------------------------------------------------------
def add_stock():
    portfolio = {}  # Stores {stock_symbol: quantity}

    print("\nEnter stock symbol and quantity to add to your portfolio.")
    print("Type 'done' as the stock symbol when you're finished.\n")

    while True:
        symbol_input = input("Enter stock symbol (or 'done' to finish): ").strip().upper()

        # Exit condition for the data-entry loop
        if symbol_input == "DONE":
            break

        # Validate that the stock symbol exists
        if symbol_input not in STOCK_PRICES:
            print(f"'{symbol_input}' is not a recognized stock symbol. Please try again.")
            continue

        # Validate the quantity using exception handling
        try:
            quantity = int(input(f"Enter quantity of {symbol_input} shares: ").strip())
            if quantity <= 0:
                print("Quantity must be a positive integer. Please try again.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a whole number (e.g., 5).")
            continue

        # Add to portfolio, combining quantities if the stock is entered again
        if symbol_input in portfolio:
            portfolio[symbol_input] += quantity
        else:
            portfolio[symbol_input] = quantity

        print(f"Added {quantity} share(s) of {symbol_input}.\n")

    return portfolio


# ---------------------------------------------------------
# Function: calculate_portfolio
# Computes investment details for each stock and overall
# portfolio statistics.
# Returns a dictionary containing all calculated results.
# ---------------------------------------------------------
def calculate_portfolio(portfolio):
    investment_details = {}   # {symbol: (qty, price, investment)}
    total_investment = 0
    total_shares = 0

    for symbol, quantity in portfolio.items():
        price = STOCK_PRICES[symbol]
        investment = price * quantity
        investment_details[symbol] = (quantity, price, investment)
        total_investment += investment
        total_shares += quantity

    # Determine highest and lowest investment stocks (guard against empty portfolio)
    highest_stock = None
    lowest_stock = None
    if investment_details:
        highest_stock = max(investment_details, key=lambda s: investment_details[s][2])
        lowest_stock = min(investment_details, key=lambda s: investment_details[s][2])

    results = {
        "details": investment_details,
        "total_investment": total_investment,
        "num_stocks": len(portfolio),
        "total_shares": total_shares,
        "highest_stock": highest_stock,
        "lowest_stock": lowest_stock
    }
    return results


# ---------------------------------------------------------
# Function: display_summary
# Prints a neatly formatted portfolio summary table and
# overall statistics. Optionally saves the summary to a
# text file.
# ---------------------------------------------------------
def display_summary(results):
    details = results["details"]

    if not details:
        print("\nYour portfolio is empty. No summary to display.")
        return

    # Build the summary as a list of lines so it can be printed
    # to the screen AND saved to a file using the same content.
    lines = []
    lines.append("=" * 58)
    lines.append("PORTFOLIO SUMMARY")
    lines.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 58)
    lines.append(f"{'Stock':<10}{'Qty':>8}{'Price':>12}{'Investment':>18}")
    lines.append("-" * 58)

    for symbol, (quantity, price, investment) in details.items():
        lines.append(f"{symbol:<10}{quantity:>8}{'₹' + str(price):>12}{'₹' + str(investment):>18}")

    lines.append("-" * 58)
    lines.append(f"Total Portfolio Investment : ₹{results['total_investment']}")
    lines.append(f"Number of Different Stocks : {results['num_stocks']}")
    lines.append(f"Total Shares Owned         : {results['total_shares']}")
    lines.append(f"Highest Investment Stock   : {results['highest_stock']}")
    lines.append(f"Lowest Investment Stock    : {results['lowest_stock']}")
    lines.append("=" * 58)

    # Print the summary to the terminal
    summary_text = "\n".join(lines)
    print("\n" + summary_text)

    # Bonus: offer to save the summary to a text file
    save_choice = input("\nSave this summary to 'portfolio_summary.txt'? (Y/N): ").strip().upper()
    if save_choice == "Y":
        try:
            with open("portfolio_summary.txt", "w", encoding="utf-8") as file:
                file.write(summary_text)
            print("Summary saved to 'portfolio_summary.txt'.")
        except OSError as error:
            print(f"Could not save file due to an error: {error}")


# ---------------------------------------------------------
# Function: show_menu
# Displays the main menu and returns the user's choice.
# ---------------------------------------------------------
def show_menu():
    print("\n" + "=" * 40)
    print("        STOCK PORTFOLIO TRACKER MENU")
    print("=" * 40)
    print("1. View Stock Prices")
    print("2. Build/Add to Portfolio")
    print("3. View Portfolio Summary")
    print("4. Start New Portfolio")
    print("5. Exit")
    return input("Choose an option (1-5): ").strip()


# ---------------------------------------------------------
# Main program loop
# Ties together all functions using a simple menu system.
# ---------------------------------------------------------
def main():
    print("Welcome to the Stock Portfolio Tracker!")
    display_stocks()

    portfolio = {}       # Current user's portfolio: {symbol: quantity}
    results = None       # Cached calculation results

    running = True
    while running:
        choice = show_menu()

        if choice == "1":
            display_stocks()

        elif choice == "2":
            new_entries = add_stock()
            # Merge new entries into the existing portfolio
            for symbol, quantity in new_entries.items():
                portfolio[symbol] = portfolio.get(symbol, 0) + quantity
            print("Portfolio updated.")

        elif choice == "3":
            results = calculate_portfolio(portfolio)
            display_summary(results)

        elif choice == "4":
            # Start a completely new portfolio
            portfolio = {}
            results = None
            print("Started a new, empty portfolio.")

        elif choice == "5":
            print("\nThank you for using the Stock Portfolio Tracker. Goodbye!")
            running = False

        else:
            print("Invalid option. Please choose a number between 1 and 5.")


# ---------------------------------------------------------
# Entry point of the program
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
