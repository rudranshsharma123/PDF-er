from os import dup
from re import search
import tempfile
from pdf_segment import PDFSegmenter
from flask import Flask, request, jsonify, make_response
# from werkzeug.wrappers import request
# from werkzeug.wrappers import response
import os
from jina import Document,Client
from jina.types.request import Response 
from helper import image_del_workspace, image_run_index_flow, image_run_query_flow, text_run_index_flow, text_del_workspace, text_run_query
from tempfile import NamedTemporaryFile
app = Flask(__name__)



JINA_TEXT_PORT = 45678
JINA_IMAGE_PORT = 55555

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/pdf', methods = ["POST"])
def pdf_process():
    pdf = request.files['pdf']
    pdf_name = pdf.filename
    img_save_path = os.path.join(os.getcwd(), pdf_name)
    pdf.save(img_save_path)
    segmentor =PDFSegmenter(pdf_name)
    segmentor.text_crafter(save_file_name= "data")
    segmentor.image_crafter()
 
    return jsonify({'code':'succccc'})

@app.route('/index', methods =['GET', 'POST'])
def run_indexing():
    text_run_index_flow()
    image_run_index_flow()
    return jsonify({'code':'succcc'})

@app.route('/query', methods= ['GET', 'POST'])
def run_query():
    text_run_query()
    image_run_query_flow()
    return jsonify({'code':'succcc'})

@app.route('/reset', methods= ['GET', 'POST'])
def reset():
    text_del_workspace()
    image_del_workspace()
    return jsonify({'code':'succcc'})

@app.route('/searchText', methods = ["POST"])
def trying():
    requests = request.get_json(force= True, silent= True)
    search_text = requests['search']
    arr =[]
    def print_matches(resp: Response):  # the callback function invoked when task is done
        data = {}
        for idx, d in enumerate(resp.docs[0].matches): 
            data[str(d.scores['cosine'].value)] = d.text 
        for i in sorted(data.keys(), reverse= True, key= lambda x: float(x)):
            arr.append(data[i])
    c = Client(protocol='http', port=JINA_TEXT_PORT)
    c.post('/search', Document(text=search_text), on_done = print_matches)
    return jsonify({'data':arr})

@app.route('/searchImage', methods = ['POST'])
def image_search():
    import base64
    import cv2
    image = request.files['picture']
    image_name = image.filename
    img_save_path = os.path.join(os.getcwd(), image_name)
    image.save(img_save_path)
    retun_images = []
    def save_image(resp:Response):
        # print(resp.docs[0].matches[0])
    
        for i, v in enumerate(resp.docs[0].matches):
            print(v.tags['filename'])
            with open("jina-image/"+v.tags['filename'], 'rb') as img_file:
                encoded_string = base64.b64encode(img_file.read())
            retun_images.append(str(encoded_string))
            # img = cv2.imread(v.tags['filename'])
            # cv2.imwrite(f'{i}.png', img)
    c = Client(protocol='http', port=JINA_IMAGE_PORT)
    c.post('/search', Document(uri=img_save_path), on_done = save_image)
    
    
    return jsonify({'images':retun_images})
    



if __name__ == '__main__':
    app.run(debug=True)