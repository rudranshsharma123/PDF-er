import os
import sys
import click
import random
from jina import Flow, Document, DocumentArray
from jina.logging.predefined import default_logger as logger

MAX_DOCS = int(os.environ.get('JINA_MAX_DOCS', 10000))
JINA_PORT = str(45678)
cur_dir = os.path.dirname(os.path.abspath(__file__))
JINA_WORKSPACE = os.path.join(cur_dir, 'workspace')
def config():
    os.environ['JINA_DATA_FILE'] = os.environ.get('JINA_DATA_FILE', 'data.txt')
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', JINA_PORT)
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ.setdefault('JINA_WORKSPACE', os.path.join(os.path.join(cur_dir, 'jina-text'), 'workspace'))
    os.environ.setdefault('JINA_WORKSPACE_MOUNT',
                          f'{os.environ.get("JINA_WORKSPACE")}:/workspace/workspace')



def input_generator(num_docs: int, file_path: str):
    with open(file_path) as file:
        lines = file.readlines()
    num_lines = len(lines)
    random.shuffle(lines)
    for i in range(min(num_docs, num_lines)):
        yield Document(text=lines[i])


def index(num_docs):
    flow = Flow().load_config('flows/flow.yml')
    data_path = os.path.join(os.path.dirname(__file__), os.environ.get('JINA_DATA_FILE', None))
    with flow:
        flow.post(on='/index', inputs=input_generator(num_docs, data_path),
                  show_progress=True)
def query_restful():
    flow = Flow.load_config('flows/flow.yml')
    flow.protocol = 'http'
    flow.port_expose = JINA_PORT        
    with flow:
        flow.block()

# def remove_workspace():
#     import subprocess
#     subprocess.run(f'cmd.exe /c start cmd.exe /c wsl.exe rm -R {JINA_WORKSPACE}', shell= True,timeout=10000)


@click.command()
@click.option(
    '--task',
    '-t',
    type=click.Choice(['index', 'query'], case_sensitive=False),
)
@click.option('--num_docs', '-n', default=MAX_DOCS)
@click.option('--top_k', '-k', default=5)
def main(task, num_docs, top_k):
    config()
    if task == 'index':
        if os.path.exists(os.environ.get("JINA_WORKSPACE")):
            logger.error(f'\n +---------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                        | \
                    \n | The directory {os.environ.get("JINA_WORKSPACE")} already exists. Please remove it before indexing again. | \
                    \n |                                   🤖🤖🤖                                        | \
                    \n +---------------------------------------------------------------------------------+')
            sys.exit(1)
        index(num_docs)
    if task == 'query':
        query_restful()
    # if task == 'del':
    #     remove_workspace()




if __name__ == '__main__':
    main()
