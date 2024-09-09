import requests
import logging
import json
import os
import argparse
import tkinter as tk
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(filename='currency_converter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get real-time exchange rate
def get_real_time_rate(api_key, base_currency, target_currencies):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        data = response.json()
        rates = {}
        for target_currency in target_currencies:
            target_currency = target_currency.strip()  # Remove any surrounding whitespace
            rate = data['conversion_rates'].get(target_currency)
            if rate:
                rates[target_currency] = rate
            else:
                logging.warning(f"Currency {target_currency} not found.")
                print(f"Currency {target_currency} not found.")
        return rates
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        print(f"An error occurred: {err}")
    return None

# Function to cache rates
def cache_rates(base_currency, rates):
    with open(f"{base_currency}_rates.json", 'w') as f:
        json.dump(rates, f)
    logging.info(f"Cached rates for {base_currency}")

# Function to load cached rates
def load_cached_rates(base_currency):
    if os.path.exists(f"{base_currency}_rates.json"):
        with open(f"{base_currency}_rates.json", 'r') as f:  # Corrected the unmatched parenthesis
            rates = json.load(f)
        logging.info(f"Loaded cached rates for {base_currency}")
        return rates
    else:
        logging.info(f"No cached rates found for {base_currency}")
        return None

# Function to plot rates
def plot_rates(base_currency, rates, amount):
    currencies = list(rates.keys())
    converted_amounts = [amount * rate for rate in rates.values()]
    
    # Set all bars to green
    colors = ['#00FF00'] * len(currencies)
    
    plt.bar(currencies, converted_amounts, color=colors)
    plt.xlabel('Target Currencies')
    plt.ylabel(f'Amount in Target Currency')
    plt.title(f'Conversion of {amount} {base_currency} to Target Currencies')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI Function
def convert_currency():
    base_currency = base_currency_entry.get().upper()
    target_currencies = target_currencies_entry.get().upper().split(',')
    amount = float(amount_entry.get())
    rates = get_real_time_rate(api_key, base_currency, target_currencies)
    if rates:
        result_label.grid(row=4, column=0, columnspan=2)  # Center the "Conversion Results:" title
        result_label.config(text="Conversion Results:", fg="white")  # Set the title text to white
        
        row = 5  # Start placing result labels after the title
        for target_currency, rate in rates.items():
            converted_amount = amount * rate
            result_text = f"{amount} {base_currency} = "
            converted_text = f"{converted_amount:.2f} {target_currency}"
            
            # Create a label for the explanation part (in white)
            result_label = tk.Label(root, text=result_text, fg="white", anchor="w")
            result_label.grid(row=row, column=0, sticky="w", padx=(10, 0))
            
            # Create a label for the converted amount part with the appropriate color
            if converted_amount > amount:
                converted_label = tk.Label(root, text=converted_text, fg="green", anchor="w")  # Profit (higher amount) in green
            else:
                converted_label = tk.Label(root, text=converted_text, fg="red", anchor="w")  # Loss (lower amount) in red
            
            converted_label.grid(row=row, column=1, sticky="w", padx=(0, 10))  # Display the result
            row += 1  # Move to the next row for each new result
            
        plot_rates(base_currency, rates, amount)

# Main function
if __name__ == "__main__":
    api_key = "2398eeee305514f1ade4b905"  # Your actual API key

    # Setup CLI arguments
    parser = argparse.ArgumentParser(description="Currency Converter CLI")
    parser.add_argument('--cli', action='store_true', help="Use the command-line interface")
    args = parser.parse_args()

    if args.cli:
        # Command-line interface mode
        base_currency = input("Enter base currency (e.g., USD): ").upper()
        target_currencies = input("Enter target currencies (comma-separated, e.g., EUR,GBP,JPY): ").upper().split(',')
        amount = float(input(f"Enter amount in {base_currency}: "))

        # Check for cached rates
        cached_rates = load_cached_rates(base_currency)
        if cached_rates:
            rates = cached_rates
        else:
            rates = get_real_time_rate(api_key, base_currency, target_currencies)
            if rates:
                cache_rates(base_currency, rates)

        if rates:
            print(f"\nConversion rates for {amount} {base_currency}:")
            for target_currency, rate in rates.items():
                converted_amount = amount * rate
                print(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
            plot_rates(base_currency, rates, amount)
    else:
        # GUI mode
        root = tk.Tk()
        root.title("Currency Converter")

        # UI elements
        tk.Label(root, text="Base Currency:").grid(row=0)
        tk.Label(root, text="Target Currencies (comma-separated):").grid(row=1)
        tk.Label(root, text="Amount:").grid(row=2)
        base_currency_entry = tk.Entry(root)
        target_currencies_entry = tk.Entry(root)
        amount_entry = tk.Entry(root)
        base_currency_entry.grid(row=0, column=1)
        target_currencies_entry.grid(row=1, column=1)
        amount_entry.grid(row=2, column=1)
        convert_button = tk.Button(root, text="Convert", command=convert_currency)
        convert_button.grid(row=3, column=1)
        
        result_label = tk.Label(root, text="", fg="white")  # Main header label
        result_label.grid(row=4, column=0, columnspan=2)  # Center the title

        # Run the GUI event loop
        root.mainloop()