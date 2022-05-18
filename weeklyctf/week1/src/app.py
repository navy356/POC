from flask import Flask, render_template, request, Markup
import sqlite3

app = Flask(__name__)
## getting output from the database ##


@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.form.get("query")
    if data:
        db = sqlite3.connect('test.db')
        cur = db.cursor()
        cur.execute(f"SELECT * FROM items WHERE item LIKE \'{data}\'")
        rows = cur.fetchall()
        if len(rows) == 0:
            return render_template('index.html', input="Sorry, but we don't have that item.")
        else:
            return render_template('index.html', input="Hell yeah we got some, come visit us.")
    else:
        return render_template('index.html', input="example: milk, eggs, etc")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
