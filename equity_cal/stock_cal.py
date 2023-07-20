def calculate_profit_loss_fifo(transactions, current_price):
    shares_owned = 0
    total_cost_basis = 0
    realized_profit_loss = 0
    unrealized_profit_loss = 0

    for transaction in transactions:
        transaction_type, shares, price = transaction

        # Buy transaction
        if transaction_type == 'BUY':
            shares_owned += shares
            total_cost_basis += shares * price

        # Sell transaction
        elif transaction_type == 'SELL':
            # Calculate realized profit/loss on this sale
            shares_sold = min(shares, shares_owned)
            realized_profit_loss += shares_sold * (price - total_cost_basis / shares_owned)
            shares_owned -= shares_sold

            # Update total cost basis to reflect shares sold
            total_cost_basis -= shares_sold * (total_cost_basis / shares_owned)

    # Calculate unrealized profit/loss based on current share price
    unrealized_profit_loss = shares_owned * (current_price - total_cost_basis / shares_owned)

    # Calculate total profit/loss
    total_profit_loss = realized_profit_loss + unrealized_profit_loss

    return total_profit_loss, realized_profit_loss, unrealized_profit_loss
