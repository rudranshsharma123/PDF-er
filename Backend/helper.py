# subprocess.run('cd jina-text && python3 app.py -t index')
# subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe python3 jina-text/app.py -t del', shell= True,timeout=10000)

def text_run_index_flow():
    import subprocess
    subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe sh index.sh', shell= True )

def text_del_workspace():
    import subprocess
    subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe sh del_workspace.sh', shell= True )

def text_run_query():
    import subprocess
    subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe sh text_query.sh', shell= True )

def image_run_index_flow():
    import subprocess
    subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe sh index_image.sh', shell= True )

def image_run_query_flow():
    import subprocess
    subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe sh image_query.sh', shell= True )

def image_del_workspace():
    import subprocess
    subprocess.run('cmd.exe /c start cmd.exe /c wsl.exe sh image_del_workspace.sh', shell= True )

