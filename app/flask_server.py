import json
import logging
import os
import sys
import requests
import time

from flask import Flask, jsonify, render_template

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('AIOGRAM_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}/sendmessage'

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/update_data', methods=['GET'])
def update_data():
    data = json.load(open('static/data/players.json', 'r', encoding='utf-8'))
    return jsonify(data)


@app.route('/question/<int:num>')
def questions(num):
    data = json.load(open('static/data/players.json', 'r', encoding='utf-8'))
    questions = json.load(open('static/data/questions.json', 'r', encoding='utf-8'))
    try:
        question_data = questions[str(num)]
        questions['current'] = str(num)
        open('static/data/questions.json', 'w', encoding='utf-8').write(
            json.dumps(questions),
        )
        start = time.time()
        reply_markup = {"keyboard": [['a', 'b'], ['c', 'd']], "resize_keyboard": False}
        for id in data.keys():
            question = question_data['question']
            answers = question_data['answers']
            text = f'{num}: {question}\na.{answers[0]}\nb.{answers[1]}\nc.{answers[2]}\nd.{answers[3]}'
            data = {'chat_id': str(id[2:]), 'text': text, 'reply_markup': json.dumps(reply_markup)}
            r = requests.post(URL, data=data)
            logging.info(f'{id[2:]}: {r.status_code}')
        logging.error(f'it took {time.time() - start}')
        return render_template(
            'question.html',
            num=num,
            data=json.dumps(question_data),
        )
    except Exception:
        raise ValueError


@app.route('/results')
def results():
    data = json.load(open('static/data/players.json', 'r', encoding='utf-8'))
    zero_data = data
    logging.info(data)
    for player in zero_data.keys():
        zero_data[player]['given'] = False
    open('static/data/players.json', 'w', encoding='utf-8').write(
        json.dumps(zero_data),
    )
    # new num question
    num_data = json.load(
        open('static/data/questions.json', 'r', encoding='utf-8'),
    )
    num_data['current'] = str(int(num_data['current']) + 1)
    next_num = num_data['current']
    open('static/data/questions.json', 'w', encoding='utf-8').write(
        json.dumps(num_data),
    )
    data = dict(sorted(data.items(), key=lambda x: x[1]["score"]))
    return render_template('results.html', data=json.dumps(data), num=next_num)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.run(debug=False, host='127.0.0.1', port=80)
