from flask import *
import requests


def getSite(url):
    site = requests.get(url)
    return site.text


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        search = request.form.get("url")
        site = getSite(search)
        template = '''
            <p>{}</p>
            
        '''.format(site)

        return render_template_string(template)
    return render_template("form.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

