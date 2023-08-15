from datetime import date
import yfinance as yf
import pandas as pd
from prettytable import PrettyTable
import streamlit as st

def main():
    # purchase_year = str(input("Enter the year you bought the stocks (defaults to first available date): "))
    # sell_year = str(input("Enter the year you sold the stocks (defaults to today's date): "))
    # ticker = str(input("Enter the stock (ticker): "))
    # shares = input("Enter the total shares you own: ")

    purchase_year = "1900"
    # sell_year = "2023"
    sell_year = str(date.today().year)
    ticker = "MSFT"
    shares = 1000
    balance = 0

    """
        Get stock (use for dividends, current price, etc.)
    """
    stock = yf.Ticker(ticker)

    print(f'Test: {ticker}, {purchase_year} --> {sell_year}.')

    """
        Get dividends between a specified period, two string objects [yyyy:yyyy].
    """
    dividends = stock.dividends[purchase_year:sell_year]
    df = pd.DataFrame(columns=['Date', 'Shares', 'Total Value'])

    table = PrettyTable()
    table.padding_width = 3
    table.field_names = [
        "Date",
        "Share Price",
        "Shares",
        "Market$Value",
        "Dividend/share",
        "Total Dividends",
        "DRIP (shares)",
        "Current Balance"
    ]

    """
        Get the stock price from the date given by the current quarter of dividend price. I.e. dividend price
        is given by quarter with a specified date for that quarter.
    """
    start_year = str(purchase_year) + "-01-01"
    end_year = str(sell_year) + "-12-31"
    stock_history = yf.download(ticker, start_year, end_year)["Close"]

    for quarter_date, dividend in dividends.items():
        quarter_date = str(quarter_date).split(' ')[0]
        stock_price = stock_history[quarter_date]
        total_dividend = dividend * shares
        total_value = stock_price * shares

        drip = (total_dividend + balance) // stock_price

        table.add_row([
            quarter_date,
            "$" + format(stock_price, ',.2f'),
            format(shares, ',d'),
            "$" + format(total_value, ",.2f"),
            "$" + format(dividend, ',.4f'),
            "$" + str(round(total_dividend, 4)),
            format(drip, ',.0f'),
            "$" + format(balance, ',.5f')
        ])

        new_row = {'Date': quarter_date, 'Shares': shares, 'Total Value': total_value}
        df.loc[len(df)] = new_row

        balance += total_dividend - drip * stock_price

        shares += int(drip)
        while balance >= stock_price:
            balance -= stock_price
            shares += 1

    print(table)
    df.set_index('Date', inplace=True)

    print(df)
    st.title('Welcome to Ryan.O.C Compound Interest Calculator!\n')

    st.line_chart(df['Total Value'])


if __name__ == "__main__":
    main()
