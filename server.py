from flask import Flask, render_template
# from main import tikz_stuff
app = Flask(__name__)

@app.route("/")
def root():
    # root directory, just send index.html
    return render_template('./public/index.html')

@app.route("/tai")
def tai():
    return "Tai"

# @app.route("/get_tikz", methods=['GET'])
# def get_tikz(params):
#     tikz = tikz_stuff()
#     return tikz
