import os
import sys
from shutil import rmtree
from glob import glob
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import imshow
from PIL import Image

from jina import Flow, DocumentArray, Document
# from jina.logging import logger as logger
from jinahub.image.normalizer import ImageNormalizer
from jinahub.image.encoder.big_transfer import BigTransferEncoder
from jinahub.image.encoder.torch_encoder import ImageTorchEncoder
import cv2
import click

from helper import JINA_PORT

def get_docs(image_src, num_docs):
    docs = DocumentArray()

    for file in image_src:
        # Uniform Resource Identifier
        doc = Document(uri=file)
        # this method loads the file into a np.ndarray 
        doc.convert_image_uri_to_blob()
        # tags can be used to store any other random data you'd need
        doc.tags['filename'] = file
        docs.append(doc)
        if len(docs) == num_docs:
            break
            
    return docs


def set_config():
    # num_docs = int(os.environ.get('JINA_MAX_DOCS', 100))
    # image_src = sorted(list(glob('data/*.*')))
    # print(image_src)
    workspace = './workspace'
    os.environ['JINA_WORKSPACE'] = workspace
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))

def index():
    num_docs = int(os.environ.get('JINA_MAX_DOCS', 100))
    image_src = sorted(list(glob('data/*.*'))) 
    f = Flow.load_config('flows/flow.yml')
    docs = get_docs(image_src, num_docs)
    with f:
        f.post(
                on='/index',
                inputs=docs,
                request_size=64
            )

def query_single(query_file_path:str):
    f = Flow.load_config('flows/flow.yml')
    outline = query_file_path
    query_docs = get_docs([outline], 1)
    with f:
        return_docs = f.post(
            on='/search',
            inputs=query_docs,
            parameters={'top_k': 5},
            return_results=True
        )
    for i, match in enumerate(return_docs[0].docs[0].matches):
        filename = match.tags['filename']
        img = cv2.imread(filename=filename)
        cv2.imwrite(f'{i}.png', img)

def query_restful():
    f = Flow.load_config('flows/flow.yml', override_with={'protocol':'http'})
    f.port_expose = JINA_PORT
    with f:
        f.block()









@click.command()
@click.option('--task', '-t', type=click.Choice(['index', 'query_restful', 'query']))
def main(task):
    set_config()
    if 'index' in task:
        # workspace = 'workspace'
        if os.path.exists(os.environ.get('JINA_WORKSPACE')):
            print(
                f'\n +------------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                           | \
                    \n | The directory  already exists. Please remove it before indexing again.  | \
                    \n |                                   🤖🤖🤖                                           | \
                    \n +------------------------------------------------------------------------------------+'
            )
            sys.exit(1)
    if 'query' in task:
        if not os.path.exists(os.environ.get('JINA_WORKSPACE')):
            print(f'The directory does not exist. Please index first via `python app.py -t index`')
            sys.exit(1)

    if task == 'index':
        index()
    elif task == 'query':
        query_single(query_file_path='data/1.png')
    elif task == 'query_restful':
        query_restful()


if __name__ == '__main__':
    
    main()




    
    # imshow(img)
    
    
    # plt.title(match.tags['filename'])
    # plt.show()