from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest
from sentence_transformers import SentenceTransformer
import streamlit as st
import os
import logging
from itertools import chain


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

COLLECTION_NAME = "restaurant_review_answers"


@st.cache_resource
def get_qdrant_connection():
    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")
    return QdrantClient(host, port=port)


@st.cache_resource
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def search(selected_list, df):
    if not selected_list:
        return

    qdrant = get_qdrant_connection()
    model = get_embedding_model()

    # Take text
    selected_rows = df.iloc[selected_list, :]
    selected_rows_list = selected_rows["body"].to_list()

    # Transform text
    embeddings = model.encode(selected_rows_list)

    logger.debug(f"embeddings length: {len(embeddings)}")

    # Prepare and send requests
    requests = [
        SearchRequest(vector=vector.tolist(), limit=1, with_payload=True)
        for vector in embeddings
    ]

    hits_not_flattened = qdrant.search_batch(
        collection_name=COLLECTION_NAME,
        requests=requests,
    )

    # Hits flatten
    hits = list(chain.from_iterable(hits_not_flattened))

    if logger.level == logging.DEBUG:
        logger.debug("PRINTING HITS")
        for i, hit in enumerate(hits, 1):
            logger.debug(f"hit {i}: {hit}")

    result = [
        {"Message": text, "Score": hit.score, "Answer": hit.payload["answer"]}
        for text, hit in zip(selected_rows_list, hits)
    ]

    if logger.level == logging.DEBUG:
        logger.debug("PRINTING Result")
        for i, item in enumerate(result, 1):
            print("que paza")
            logger.debug(f"result {i}: {item}")

    return result
