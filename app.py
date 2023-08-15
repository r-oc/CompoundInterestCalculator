from datetime import date
import yfinance as yf
import pandas as pd
import streamlit as st

# TODO:
#   - USER INPUT
#   -

def main():
    # purchase_year = str(input("Enter the year you bought the stocks (defaults to first available date): "))
    # sell_year = str(input("Enter the year you sold the stocks (defaults to today's date): "))
    # ticker = str(input("Enter the stock (ticker): "))
    # shares = input("Enter the total shares you own: ")

    st.sidebar.header("Enter the symbol ticker you want to look at...")
    start_date = st.sidebar.text_input("Start Date", "1998-01-01")
    end_date = st.sidebar.text_input("End Date", "2023-08-09")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AAPL")

    purchase_year = "1900"
    # sell_year = "2023"
    sell_year = str(date.today().year)
    ticker = "MSFT"
    shares = 1000
    balance = 0

    ticker = stock_symbol
    purchase_year = start_date[:4]
    sell_year = end_date[:4]

    stock = yf.Ticker(ticker)

    # print(f'Test: {ticker}, {purchase_year} --> {sell_year}.')

    dividends = stock.dividends[purchase_year:sell_year]
    df = pd.DataFrame(columns=['Date', 'Shares', 'Total Value'])

    # table = PrettyTable()
    # table.padding_width = 3
    # table.field_names = [
    #     "Date",
    #     "Share Price",
    #     "Shares",
    #     "Market$Value",
    #     "Dividend/share",
    #     "Total Dividends",
    #     "DRIP (shares)",
    #     "Current Balance"
    # ]

    start_year = str(purchase_year) + "-01-01"
    end_year = str(sell_year) + "-12-31"
    stock_history = yf.download(ticker, start_year, end_year)["Close"]
    a = stock_history[0] * shares
    total_value = 0

    for quarter_date, dividend in dividends.items():
        quarter_date = str(quarter_date).split(' ')[0]
        stock_price = stock_history[quarter_date]
        total_dividend = dividend * shares
        total_value = stock_price * shares

        drip = (total_dividend + balance) // stock_price

        # table.add_row([
        #     quarter_date,
        #     "$" + format(stock_price, ',.2f'),
        #     format(shares, ',d'),
        #     "$" + format(total_value, ",.2f"),
        #     "$" + format(dividend, ',.4f'),
        #     "$" + str(round(total_dividend, 4)),
        #     format(drip, ',.0f'),
        #     "$" + format(balance, ',.5f')
        # ])

        new_row = {'Date': quarter_date, 'Shares': shares, 'Total Value': total_value}
        df.loc[len(df)] = new_row

        balance += total_dividend - drip * stock_price

        shares += int(drip)
        while balance >= stock_price:
            balance -= stock_price
            shares += 1

    # print(table)
    df.set_index('Date', inplace=True)

    # print(df)
    st.title('Welcome to Ryan.O.C Compound Interest Calculator!\n')

    st.write("""Checking stock: """, ticker)

    st.line_chart(df['Total Value'])

    s = "${0:,.2f}".format(a)
    st.write("""start with """, s)
    e = "${0:,.2f}".format(total_value)
    st.write("""current value """, e)

    st.write(""" # Total share growth over time""")
    st.line_chart(df['Shares'])

if __name__ == "__main__":
    main()
