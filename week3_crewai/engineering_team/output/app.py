# app.py
import gradio as gr
from accounts import Account, InsufficientFundsError, InsufficientSharesError
import time
import pandas as pd

# Initialize the account
account = Account("user1", initial_deposit=1000.0)

def deposit(amount):
    try:
        amount = float(amount)
        account.deposit(amount)
        return f"Deposit successful. Current balance: {account.balance}"
    except ValueError:
        return "Invalid input. Please enter a number."

def withdraw(amount):
    try:
        amount = float(amount)
        account.withdraw(amount)
        return f"Withdrawal successful. Current balance: {account.balance}"
    except ValueError:
        return "Invalid input. Please enter a number."
    except InsufficientFundsError as e:
        return str(e)

def buy(symbol, quantity):
    try:
        quantity = int(quantity)
        account.buy(symbol, quantity)
        return f"Buy successful. Current balance: {account.balance}. Holdings: {account.holdings}"
    except ValueError:
        return "Invalid quantity. Please enter an integer."
    except InsufficientFundsError as e:
        return str(e)

def sell(symbol, quantity):
    try:
        quantity = int(quantity)
        account.sell(symbol, quantity)
        return f"Sell successful. Current balance: {account.balance}. Holdings: {account.holdings}"
    except ValueError:
        return "Invalid quantity. Please enter an integer."
    except InsufficientSharesError as e:
        return str(e)

def get_portfolio_value():
    return f"Portfolio value: {account.get_portfolio_value()}"

def get_profit_loss():
    return f"Profit/Loss: {account.get_profit_loss()}"

def get_transactions():
    transactions = account.list_transactions()
    transaction_data = []
    for transaction in transactions:
        transaction_data.append([
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(transaction.timestamp)),
            transaction.transaction_type,
            transaction.symbol or '',
            transaction.quantity or '',
            transaction.price or '',
            transaction.balance,
            transaction.shares
        ])

    df = pd.DataFrame(transaction_data, columns=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Balance", "Shares"])
    return df

def get_holdings():
    return str(account.get_holdings())

def get_profit_loss_at_time(timestamp):
    try:
        timestamp = float(timestamp)
        return f"Profit/Loss at {timestamp}: {account.get_profit_loss_at_time(timestamp)}"
    except ValueError:
        return "Invalid timestamp. Please enter a number."

with gr.Blocks() as demo:
    gr.Markdown("# Simple Trading Account")

    with gr.Tab("Account Management"):
        deposit_amount = gr.Textbox(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
        deposit_output = gr.Textbox(label="Deposit Result")
        deposit_button.click(deposit, inputs=deposit_amount, outputs=deposit_output)

        withdraw_amount = gr.Textbox(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
        withdraw_output = gr.Textbox(label="Withdraw Result")
        withdraw_button.click(withdraw, inputs=withdraw_amount, outputs=withdraw_output)

    with gr.Tab("Trading"):
        symbol = gr.Textbox(label="Symbol (AAPL, TSLA, GOOGL)")
        buy_quantity = gr.Textbox(label="Buy Quantity")
        buy_button = gr.Button("Buy")
        buy_output = gr.Textbox(label="Buy Result")
        buy_button.click(buy, inputs=[symbol, buy_quantity], outputs=buy_output)

        sell_quantity = gr.Textbox(label="Sell Quantity")
        sell_button = gr.Button("Sell")
        sell_output = gr.Textbox(label="Sell Result")
        sell_button.click(sell, inputs=[symbol, sell_quantity], outputs=sell_output)

    with gr.Tab("Reporting"):
        portfolio_button = gr.Button("Get Portfolio Value")
        portfolio_output = gr.Textbox(label="Portfolio Value")
        portfolio_button.click(get_portfolio_value, outputs=portfolio_output)

        profit_loss_button = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Profit/Loss")
        profit_loss_button.click(get_profit_loss, outputs=profit_loss_output)

        transactions_button = gr.Button("List Transactions")
        transactions_output = gr.DataFrame()
        transactions_button.click(get_transactions, outputs=transactions_output)

        holdings_button = gr.Button("Get Holdings")
        holdings_output = gr.Textbox(label="Holdings")
        holdings_button.click(get_holdings, outputs=holdings_output)

        timestamp_input = gr.Textbox(label="Timestamp for P/L")
        profit_loss_at_time_button = gr.Button("Get P/L at Time")
        profit_loss_at_time_output = gr.Textbox(label="P/L at Time")
        profit_loss_at_time_button.click(get_profit_loss_at_time, inputs=timestamp_input, outputs=profit_loss_at_time_output)


demo.launch()
