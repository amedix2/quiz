from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/question/<int:num>')
def questions(num):
    return render_template('question.html', num=num)


@app.route("/results")
def results():
    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=80)
