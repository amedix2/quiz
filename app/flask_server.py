import json
import logging
import sys
from flask import Flask, render_template

__all__ = ['app']

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/question/<int:num>')
def questions(num):
    logging.info(str(num))
    data = json.load(open('static/data/questions.json', 'r', encoding='utf-8'))
    try:
        question_data = data[str(num)]
        data['current'] = str(num)
        open('static/data/questions.json', 'w', encoding='utf-8').write(json.dumps(data))
        return render_template('question.html', num=num, data=json.dumps(question_data))
    except Exception:
        raise ValueError


@app.route('/results')
def results():
    data = json.load(open('static/data/players.json', 'r', encoding='utf-8'))
    zero_data = data
    logging.info(data)
    for player in zero_data.keys():
        zero_data[player]['given'] = False
    open('static/data/players.json', 'w', encoding='utf-8').write(json.dumps(zero_data))
    return render_template('results.html', data=data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    app.run(debug=True, host='127.0.0.1', port=80)
