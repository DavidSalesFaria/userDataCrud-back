from flask import Flask

app_copy = Flask(__name__)
app_copy.config.from_pyfile("../app.py")