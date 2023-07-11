# Directory tree guide
* challenge_functions: Package that implements the logic for the functionality available in the UI.
* data: In this folder there's data from the reviews extracted in the mandatory excercise.
* load_database: Here you can find a full snapshot of the qdrant database, a file with the generic answers that the automated response system will use and a script that loads them and creates a full snapshot.
* pages: In this folder you'll find the implementation of the UIs.
* tests: notebooks that helped me develop some features.

# Installing dependencies
To create the conda environment used for this app use the following commands
``` bash
conda create -n nlp python=3
conda activate nlp
pip install -r requirements.txt
```
# Qdrant deployment in docker

``` bash
docker run --name qdrant -p 6333:6333 -p 6334:6334 -v "<__YOUR_PATH__>:/qdrant/storage" qdrant/qdrant
```
# Modify .env file
Just like in the template
```
QDRANT_HOST=localhost
QDRANT_PORT=6333
OPEN_AI_API_KEY=Your_api_key
```

# Running the program
```
streamlit run "./Sentiment Analisys.py"
```