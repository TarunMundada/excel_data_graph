import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def load_data(file_path):
    df = pd.read_excel(file_path)

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    return df

def plot_line_chart(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Close Price Over Time')
    plt.legend()
    plt.grid(True)
    plt.show() 
    
def plot_candlestick_chart(df):
    mpf.plot(df, type='candle', style='charles', title='Candlestick Chart', ylabel='Price')
    

def plot_superimposed_chart(df):
    add_plot = mpf.make_addplot(df['Close'], color='blue', linestyle='-', panel=0)
    mpf.plot(df, type='candle', style='charles', title='Candlestick Chart with Close Price Line', ylabel='Price', addplot=add_plot)

    plt.show()

def main():
    file_path = input("Enter the path to the Excel file: ")
    df = load_data(file_path)
    
    choice = input("Enter 1 for separate line and candlestick charts or 2 for superimposed chart: ")

    if choice == '1':
        plot_candlestick_chart(df)
        plot_line_chart(df)
        
    elif choice == '2':
        plot_superimposed_chart(df)
    else:
        print("Invalid choice. Please enter 1 or 2.")



