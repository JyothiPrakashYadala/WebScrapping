from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def scrape_data():
    url1 = 'https://www.bbc.com/news/technology'
    url2 = 'https://edition.cnn.com/business/tech'

    response1 = requests.get(url1)
    response2 = requests.get(url2)

    soup1 = BeautifulSoup(response1.content,'html.parser')
    soup2 = BeautifulSoup(response2.content,'html.parser')

    result1 = soup1.find_all(class_='gs-c-promo-heading__title')
    result2 = soup2.find_all(class_='container__headline container_vertical-strip__headline')

    BBC_HeadLines = [res.get_text().strip() for res in result1[1:8]]
    CNN_HeadLines = [res2.get_text().strip() for res2 in result2[1:8]]

    min_length = min(len(BBC_HeadLines),len(CNN_HeadLines))
    BBC_HeadLines = BBC_HeadLines[:min_length]
    CNN_HeadLines = CNN_HeadLines[:min_length]

    result = pd.DataFrame({
        'BBC_HeadLines'   :   BBC_HeadLines,
        'CNN_HeadLines'   :   CNN_HeadLines,
    })

    return result

@app.route('/')
def display_headlines():
    data = scrape_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
