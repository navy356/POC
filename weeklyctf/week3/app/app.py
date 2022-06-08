import pickle
import base64
from flask import Flask, request
import os
from shlex import quote
app = Flask(__name__)

def exec(cmd):
    return os.popen(cmd).read()

class RCE:
    def __init__(self,file = ""):
        self.file = file
        self.output = ''

    def __reduce__(self):
        self.file = quote(self.file)
        if "file" in self.file:
            return
        cmd = ("curl -s "+self.file)
        return exec, (cmd,)

@app.route("/hackme", methods=["GET"])
def hackme():
    data = base64.urlsafe_b64decode(request.args['pickled'])
    deserialized = pickle.loads(data)
    return deserialized, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)