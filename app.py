from flask import Flask, render_template, request
from datetime import datetime

# Import the get_train function from your script
from Train import get_train

app = Flask(__name__)

def format_date(html_date):
    print(html_date)
    # HTML'den gelen tarih bilgisini "." karakterine göre böler
    parts = html_date.split('-')
    
    # Gün, ay ve yıl bilgilerini alır
    day = parts[2]
    month = parts[1]
    year = parts[0]
    
    # Yeniden düzenlenmiş tarih bilgisini oluşturur
    formatted_date = f"{day}.{month}.{year}"
    print(formatted_date)
    return formatted_date


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    tarih = request.form['tarih']
    tarih= format_date(tarih)
    nereden = request.form['nereden']
    nereye = request.form['nereye']
    trains = get_train(tarih, nereden, nereye)
    return render_template('result.html', trains=trains)

if __name__ == '__main__':
    app.run(debug=True)
