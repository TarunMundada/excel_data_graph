from flask import Flask, request, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

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
    plt.savefig(os.path.join(app.config['STATIC_FOLDER'], 'line_chart.png'))
    plt.close()

def plot_candlestick_chart(df):
    mpf.plot(df, type='candle', style='charles', title='Candlestick Chart', ylabel='Price', savefig=os.path.join(app.config['STATIC_FOLDER'], 'candlestick_chart.png'))

def plot_superimposed_chart(df):
    add_plot = mpf.make_addplot(df['Close'], color='blue', linestyle='-', panel=0)
    mpf.plot(df, type='candle', style='charles', title='Candlestick Chart with Close Price Line', ylabel='Price', addplot=add_plot, savefig=os.path.join(app.config['STATIC_FOLDER'], 'superimposed_chart.png'))

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        df = load_data(file_path)

        chart_type = request.form.get('chart_type')
        if chart_type == 'line':
            plot_line_chart(df)
            return send_file(os.path.join(app.config['STATIC_FOLDER'], 'line_chart.png'), mimetype='image/png')
        elif chart_type == 'candlestick':
            plot_candlestick_chart(df)
            return send_file(os.path.join(app.config['STATIC_FOLDER'], 'candlestick_chart.png'), mimetype='image/png')
        elif chart_type == 'superimposed':
            plot_superimposed_chart(df)
            return send_file(os.path.join(app.config['STATIC_FOLDER'], 'superimposed_chart.png'), mimetype='image/png')
        else:
            return 'Invalid chart type'

if __name__ == '__main__':
    app.run(debug=True)

