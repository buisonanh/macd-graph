import os
from vnstock import *
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns

# Your program code here
class main():
    df = stock_historical_data(symbol="FPT", type="stock", start_date=str(dt.date.today()-dt.timedelta(120)), end_date=str(dt.date.today()))
    df['time'] = df['time'].astype(str)
    df.set_index('time', inplace=True)

    # Calculate MACD
    short_period = 12
    long_period = 26
    signal_period = 9

    df['ShortEMA'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['LongEMA'] = df['close'].ewm(span=long_period, adjust=False).mean()
    df['MACD'] = df['ShortEMA'] - df['LongEMA']
    df['Signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()

    # Calculate the MACD Histogram
    df['Histogram'] = df['MACD'] - df['Signal']

    
    # Determine colors for the MACD Histogram bars
    colors = []

    for i in range(len(df)):
        if i > 0 and df['Histogram'][i - 1] >= 0 and df['Histogram'][i] < df['Histogram'][i - 1]:
            colors.append('lightgreen')  # Indicates a change in trend (lighter color)
        elif  i > 0 and df['Histogram'][i] < 0 and df['Histogram'][i - 1] < 0 and df['Histogram'][i] > df['Histogram'][i - 1]:
            colors.append('pink')
        else:
            colors.append('g' if df['Histogram'][i] >= 0 else 'r')



    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(18, 8))
    fig.patch.set_facecolor('#001f3f')

    ax1.set_facecolor('#001f3f')
    ax2.set_facecolor('#001f3f')

    # Plot stock price on the top subplot
    ax1.plot(df.index, df['close'], label='Stock Price', color='magenta')
    ax1.set_ylabel('Stock Price', color='white')
    ax1.grid(color='gray', alpha=0.3)  # Adjust grid color

    ax1.yaxis.set_tick_params(labelcolor='white')

    # Plot MACD and Histogram on the bottom subplot with custom colors
    ax2.plot(df.index, df['MACD'], label='MACD', color='cyan')
    ax2.plot(df.index, df['Signal'], label='Signal Line', color='orange')

    # Plot the MACD Histogram with custom colors
    ax2.bar(df.index, df['Histogram'], width=1, label='Histogram', color=colors, edgecolor='white')

    ax2.set_ylabel('MACD', color='white')
    ax2.grid(color='gray', alpha=0.3)

    # Add title and legend
    plt.title('Stock Price and MACD', color='white')

    ax1.legend()
    ax2.legend()       

    # Rotate the x-axis date labels for better visibility
    plt.xticks(rotation=90, color='white')
    plt.yticks(color='white')


    plt.show()




if __name__ == "__main__":
    main()
