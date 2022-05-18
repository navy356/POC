from flask import Flask, render_template
from flask import request, render_template_string
import os


# FLASK_APP = app.py

app = Flask(__name__, static_folder="static")
app.secret_key = "BugBase{rtx_3090_ssti}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        update = request.form['quote']
    else:
        update = "hemlo"
    
    template = '''
    %s''' % update
    quote = render_template_string(template)
    return render_template("index.html", quote = quote)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port="6942")
