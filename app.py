from flask import Flask, render_template


app = Flask(__name__)
print(__name__)

@app.route('/')
def home():
    return render_template('index.html', title = 'Connect 4!')

