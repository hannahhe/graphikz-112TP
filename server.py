from flask import Flask, render_template, request, jsonify
from main import ScatterPlot, GraphTheory
import io
import numpy as np
import cv2
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB # Remember to set a max content length

@app.route("/")
def root():
    # root directory, just send index.html
    return render_template('./public/index.html')

@app.route("/graph", methods=['PUT']) #need to retun LaTex file and detected points and lines picture (put in dict)
def graph(): #files are different from other things: if you wanted to send the file name (which is a string), use form
    print(request.form) #request.form, request.files
    print(request.files)
    if(request.form["GraphType"] == "Scatter Plot"):
        graph1 = ScatterPlot()
    if(request.form["GraphType"] == "Graph Theory"):
        graph1 = GraphTheory()
        numEdges = int(request.form["NumEdges"])
        # Here is the code to convert the post request to an OpenCV object via https://gist.github.com/mjul/32d697b734e7e9171cdb
        if request.method == 'PUT' and 'GraphImage' in request.files:
            photo = request.files['GraphImage']
            in_memory_file = io.BytesIO()
            photo.save(in_memory_file)
            data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
            color_image_flag = 1
            img = cv2.imdecode(data, color_image_flag)
        if(isinstance(graph1, GraphTheory)):
            laTexCode = graph1.detectPointsAndAxes(img, numEdges)
        if(isinstance(graph1, ScatterPlot)):
            laTexCode = graph1.detectPointsAndAxes(img)


    return jsonify({'latex': laTexCode}) #jsonify: turns python dictionaries into json

# @app.route("/get_tikz", methods=['GET'])
# def get_tikz(params):
#     tikz = tikz_stuff()
#     return tikz
