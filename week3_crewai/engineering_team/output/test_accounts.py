import unittest

# accounts.py content (embedded to avoid import issues)
from typing import Dict, List, Tuple

class InsufficientFundsError(Exception):
    """Raised when an account has insufficient funds for a transaction."""
    pass

class InsufficientSharesError(Exception):
    """Raised when an account has insufficient shares to sell."""
    pass

class Transaction:
    """
    Represents a single transaction in the account.
    """
    def __init__(self, timestamp: float, transaction_type: str, symbol: str, quantity: int, price: float, balance: float, shares: Dict[str,int]):
        """
        Initializes a new Transaction object.

        Args:
            timestamp: The time the transaction occurred.
            transaction_type: "deposit", "withdrawal", "buy", or "sell".
            symbol: The stock symbol involved (if applicable).
            quantity: The number of shares bought or sold (if applicable).
            price: The price per share at the time of the transaction (if applicable).
            balance: The account balance after the transaction.
            shares: The account's shares held after the transaction
        """
        self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.balance = balance
        self.shares = shares

    def __repr__(self):
        return (
            f"Transaction(timestamp={self.timestamp}, type='{self.transaction_type}', "
            f"symbol='{self.symbol}', quantity={self.quantity}, price={self.price}, "
            f"balance={self.balance}, shares={self.shares})"
        )

class Account:
    """
    Represents a user's trading account.
    """

    def __init__(self, account_id: str, initial_deposit: float = 0.0):
        """
        Initializes a new Account object.

        Args:
            account_id: A unique identifier for the account.
            initial_deposit: The initial deposit amount (default: 0.0).
        """
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings: Dict[str, int] = {}  # {symbol: quantity}
        self.transactions: List[Transaction] = []
        self.record_transaction(transaction_type = "deposit", symbol = None, quantity = None, price = None, amount = initial_deposit)


    def deposit(self, amount: float) -> None:
        """
        Deposits funds into the account.

        Args:
            amount: The amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.record_transaction(transaction_type = "deposit", symbol = None, quantity = None, price = None, amount = amount)


    def withdraw(self, amount: float) -> None:
        """
        Withdraws funds from the account.

        Args:
            amount: The amount to withdraw.

        Raises:
            InsufficientFundsError: If the account has insufficient funds.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise InsufficientFundsError("Insufficient funds.")
        self.balance -= amount
        self.record_transaction(transaction_type = "withdrawal", symbol = None, quantity = None, price = None, amount = amount)


    def buy(self, symbol: str, quantity: int) -> None:
        """
        Buys shares of a given stock.

        Args:
            symbol: The stock symbol to buy.
            quantity: The number of shares to buy.

        Raises:
            InsufficientFundsError: If the account has insufficient funds.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity

        if self.balance < total_cost:
            raise InsufficientFundsError("Insufficient funds to buy shares.")

        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.record_transaction(transaction_type = "buy", symbol = symbol, quantity = quantity, price = price_per_share, amount = total_cost)


    def sell(self, symbol: str, quantity: int) -> None:
        """
        Sells shares of a given stock.

        Args:
            symbol: The stock symbol to sell.
            quantity: The number of shares to sell.

        Raises:
            InsufficientSharesError: If the account has insufficient shares.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise InsufficientSharesError("Insufficient shares to sell.")

        price_per_share = get_share_price(symbol)
        total_revenue = price_per_share * quantity

        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.record_transaction(transaction_type = "sell", symbol = symbol, quantity = quantity, price = price_per_share, amount = total_revenue)


    def get_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio.

        Returns:
            The total portfolio value.
        """
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.

        Returns:
            The profit or loss.
        """
        initial_deposit = 0.0
        for transaction in self.transactions:
            if transaction.transaction_type == "deposit" and transaction.symbol is None:
                initial_deposit += transaction.amount

        return self.get_portfolio_value() - initial_deposit


    def get_holdings(self, timestamp: float = None) -> Dict[str, int]:
        """
        Returns the holdings of the user at a given point in time.  If timestamp is None, return current holdings.

        Args:
            timestamp: The point in time to retrieve holdings for.

        Returns:
            A dictionary representing the holdings at the given time.
        """

        if timestamp is None:
            return self.holdings.copy()
        else:
            historical_holdings: Dict[str, int] = {}
            for transaction in self.transactions:
                if transaction.timestamp <= timestamp:
                    if transaction.transaction_type == "buy":
                        historical_holdings[transaction.symbol] = historical_holdings.get(transaction.symbol, 0) + transaction.quantity
                    elif transaction.transaction_type == "sell":
                        historical_holdings[transaction.symbol] = historical_holdings.get(transaction.symbol, 0) - transaction.quantity
                        if historical_holdings[transaction.symbol] == 0:
                            del historical_holdings[transaction.symbol]
            return historical_holdings


    def get_profit_loss_at_time(self, timestamp: float) -> float:
          """
          Calculates profit/loss at a point in time

          Args:
              timestamp: The point in time to calculate P&L for.

          Returns:
              The profit or loss at the specific time.
          """
          initial_deposit = 0.0
          for transaction in self.transactions:
              if transaction.timestamp <= timestamp and transaction.transaction_type == "deposit" and transaction.symbol is None:
                  initial_deposit += transaction.amount

          historical_balance = 0.0
          historical_holdings = self.get_holdings(timestamp)

          for transaction in self.transactions:
            if transaction.timestamp <= timestamp:
                if transaction.transaction_type == "deposit":
                    if transaction.symbol is None:
                        historical_balance = transaction.balance
                elif transaction.transaction_type == "withdrawal":
                    historical_balance = transaction.balance
                elif transaction.transaction_type == "buy":
                    historical_balance = transaction.balance
                elif transaction.transaction_type == "sell":
                    historical_balance = transaction.balance

          portfolio_value = historical_balance
          for symbol, quantity in historical_holdings.items():
              portfolio_value += get_share_price(symbol) * quantity

          return portfolio_value - initial_deposit


    def list_transactions(self) -> List[Transaction]:
        """
        Lists all transactions for the account.

        Returns:
            a list of Transaction objects.
        """
        return self.transactions

    def record_transaction(self, transaction_type: str, symbol: str, quantity: int, price: float, amount: float) -> None:
        """
        Records a transaction in the account history.

        Args:
            transaction_type: The type of transaction ("deposit", "withdrawal", "buy", or "sell").
            symbol: The stock symbol involved (if applicable).
            quantity: The number of shares bought or sold (if applicable).
            price: The price per share at the time of the transaction (if applicable).
            amount: The total ammount, could be a deposit, withdrawal, or buy/sell amount
        """

        import time
        timestamp = time.time()
        shares = self.holdings.copy() #important, log the current shares as part of the transaction
        transaction = Transaction(timestamp, transaction_type, symbol, quantity, price, self.balance, shares)
        self.transactions.append(transaction)

# Mock implementation of get_share_price for testing purposes
def get_share_price(symbol: str) -> float:
    """
    Returns the current price of a share for a given symbol.

    Args:
        symbol: The stock symbol.

    Returns:
        The current price of the share.
    """
    if symbol == "AAPL":
        return 150.0
    elif symbol == "TSLA":
        return 700.0
    elif symbol == "GOOGL":
        return 2500.0
    else:
        return 100.0

# End accounts.py content

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account("test_account", 1000.0)

    def test_deposit(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1].transaction_type, "deposit")
        self.assertEqual(self.account.transactions[-1].amount, 500.0)

    def test_deposit_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    def test_withdraw(self):
        self.account.withdraw(200.0)
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1].transaction_type, "withdrawal")
        self.assertEqual(self.account.transactions[-1].amount, 200.0)

    def test_withdraw_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-50.0)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1500.0)

    def test_buy(self):
        self.account.buy("AAPL", 5)
        self.assertEqual(self.account.balance, 250.0)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[-1].transaction_type, "buy")
        self.assertEqual(self.account.transactions[-1].symbol, "AAPL")
        self.assertEqual(self.account.transactions[-1].quantity, 5)
        self.assertEqual(self.account.transactions[-1].price, 150.0)

    def test_buy_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.account.buy("AAPL", -2)

    def test_buy_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.buy("TSLA", 2) # Requires 1400, balance is 1000

    def test_sell(self):
        # First buy some shares
        self.account.buy("AAPL", 5)
        # Then sell them
        self.account.sell("AAPL", 3)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.holdings["AAPL"], 2)
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[-1].transaction_type, "sell")
        self.assertEqual(self.account.transactions[-1].symbol, "AAPL")
        self.assertEqual(self.account.transactions[-1].quantity, 3)
        self.assertEqual(self.account.transactions[-1].price, 150.0)

    def test_sell_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.account.sell("AAPL", -1)

    def test_sell_insufficient_shares(self):
        with self.assertRaises(InsufficientSharesError):
            self.account.sell("TSLA", 1)

    def test_sell_more_than_owned(self):
        self.account.buy("AAPL", 5)
        with self.assertRaises(InsufficientSharesError):
            self.account.sell("AAPL", 6)

    def test_get_portfolio_value(self):
        self.account.buy("AAPL", 2)
        self.account.buy("TSLA", 1)
        expected_value = self.account.balance + (2 * 150.0) + (1 * 700.0)
        self.assertEqual(self.account.get_portfolio_value(), expected_value)

    def test_get_profit_loss(self):
        self.account.buy("AAPL", 2)
        self.account.sell("AAPL", 1)
        profit_loss = self.account.get_profit_loss()
        # Initial deposit = 1000, spent 300, received 150, balance 850. Holdings 1 AAPL @ 150 = 1000. get_profit_loss returns portfolio value - initial deposit
        expected_profit_loss = self.account.get_portfolio_value() - 1000
        self.assertEqual(profit_loss, expected_profit_loss)

    def test_get_holdings(self):
        self.account.buy("AAPL", 5)
        self.account.buy("TSLA", 2)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings["AAPL"], 5)
        self.assertEqual(holdings["TSLA"], 2)

    def test_get_holdings_at_time(self):
        import time
        self.account.buy("AAPL", 5)
        time.sleep(0.1)
        timestamp = time.time()
        time.sleep(0.1)
        self.account.buy("TSLA", 2)
        holdings = self.account.get_holdings(timestamp)
        self.assertEqual(holdings["AAPL"], 5)
        self.assertNotIn("TSLA", holdings)

    def test_get_profit_loss_at_time(self):
        import time
        self.account.buy("AAPL", 2)