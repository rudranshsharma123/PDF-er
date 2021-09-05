# PDF-er

# How to use guide


### Clone the Repository

```bash
     https://github.com/rudranshsharma123/PDF-er.git
```

### Install the Requirements

```bash
    pip install -r requirements.txt
```

### Running the backend

-   No need to index or query or run the flow like a traditional Jina app. All you need to do is run the flask server

```bash
    $ cd backend
    $ python3 server.py
```
-  Now all you need to do is run the frontend, made in electron and ensure that there server is serving

```bash
    $ cd frontend
    $ npm start
```
- Now that the frontend is ready all you need to do is to uplaod a PDF document and then click on the submit button

- You should see a message like "succc" on your page and that means the PDF is succesfully segmented and now you can run the Jina Flows

- Click on the Index button first to index your data. It will run both the Image and Text indexer Parallely (I have made the shell scripts such that it works well on WSL2 you might need to edit the shell scripts to fit into your OS but that's like editing around 4 lines)

- Then once the indexing is done, click the query button to tell Jina to start serving. Once both the server are serving all your Jina work is done

- Now, be sure to hit the reset button, (dont worry no data is being lost it is to circumvent an unresolved issue of Google Chrome)

- Now, just choose which type you want to search from the drop down and you should see your results 

- If you would like to change your PDF just click the reset pdf button which would delete any indexed data for a fresh start. Just follow these steps again  




