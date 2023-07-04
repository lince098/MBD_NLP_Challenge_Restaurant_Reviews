from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import streamlit as st
import asyncio

@st.cache_resource  
def get_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def get_qdrant_client():
    QdrantClient("localhost", port=6333)

def search(df):
    model = get_embedding_model()
    text_column = df["body"].to_list()
    embeddings = model.encode(text_column)
    
