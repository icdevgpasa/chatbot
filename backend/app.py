from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello():
    now = datetime.now().strftime("%H:%M:%S")
    return 'Hello World! I have been seen {} times.\n'.format(now)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
