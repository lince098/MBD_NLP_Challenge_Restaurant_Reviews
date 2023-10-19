# Restaurant Review Intelligence Dashboard: Enhancing Customer Feedback Analysis with NLP
This project aims to develop a comprehensive dashboard for intelligent analysis of restaurant customer reviews using various natural language processing (NLP) techniques. The goal is to provide restaurant employees with a user-friendly tool to analyze customer feedback, particularly from sources like TripAdvisor, and gain valuable insights.

## Features
The dashboard comprises several modules, each serving a unique purpose:

1. Sentiment Analysis (Classification): This module assesses the sentiment of customer reviews, categorizing them as either positive or negative. It helps hotel staff quickly gauge customer sentiment at a glance.

2. Automated Responses (Vector Search): The Automated Responses module generates intelligent responses based on the analyzed reviews. This feature can assist hotel employees in crafting personalized and timely responses to customer feedback.

3. Content Summaries (OpenAI): The Content Summaries module provides a high-level overview of the content found within a set of reviews. It extracts key themes and highlights, helping hotel staff identify common issues or praise points.

4. Possible Improvements (OpenAI): This feature analyzes customer reviews and identifies potential areas for improvement. It uses advanced NLP techniques to extract suggestions, complaints, and recurring themes from the reviews. Restaurant management can use these insights to make data-driven decisions and enhance the overall guest experience

5. Stars Distribution Histogram (Visualization): Understanding the distribution of star ratings in customer reviews is crucial for evaluating restaurant performance. The Distribution of Stars Histogram provides a visual representation of how customers rate their experiences. This histogram helps hotel management identify trends and assess the overall satisfaction levels of guests.

6. Translations (OpenAI): The Translation feature allows hotel staff to translate customer reviews into multiple languages, making it easier to cater to a global audience. This multilingual capability ensures that no valuable feedback is missed, and it facilitates communication with international guests. It utilizes state-of-the-art translation models to provide accurate and context-aware translations.

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
