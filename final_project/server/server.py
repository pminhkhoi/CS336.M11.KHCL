import os
from re import template
from flask import Flask, jsonify, redirect, request, render_template, make_response, send_from_directory
from image_retrieval import retrieval, retrieval_crop
import json


app = Flask(__name__, static_folder='static', template_folder='templates')
UPLOAD_FOLDER = './uploads'
MEDIA_FOLDER = './image_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MEDIA_FOLDER'] = MEDIA_FOLDER

@app.route("/")
def init():
    return render_template('./index.html')


@app.route('/test', methods=['GET', 'POST'])
def testfn():
    if 'file' not in request.files:
        print('no file')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        print('empty file name')
        return redirect(request.url)

    if file:    
        sorted_paths = None
        similarity = None

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f"upload.{file.filename.rsplit('.', 1)[1].lower()}"))

        if (request.headers['pos'] == 'none'):
            sorted_paths, similarity = retrieval('./uploads/upload.png')
        else:
            dict_obj = json.loads(request.headers['pos'])

            if (dict_obj['x'] > 0 and dict_obj['y'] > 0 and dict_obj['w'] > 0 and dict_obj['h'] > 0):
                sorted_paths, similarity = retrieval_crop(['./uploads/upload.png', dict_obj['x'], dict_obj['y'], dict_obj['w'], dict_obj['h']])
            else: 
                sorted_paths, similarity = retrieval('./uploads/upload.png')

        result = []

        for i in range(20): 
            result.append([sorted_paths[i], similarity[i]])

        
        return make_response(jsonify(result), 200)

    return 'Sucesss', 200  


@app.route('/image_data/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)