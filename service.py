from random import randint
from time import sleep

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    delay = randint(0,10)
    sleep(delay)
    return "service response delay: " + str(delay) + "sec"


app.run()
