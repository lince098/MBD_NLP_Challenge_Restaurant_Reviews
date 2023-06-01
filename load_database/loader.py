import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import requests
from sentence_transformers import SentenceTransformer

# Read and preprocess articles extracted
with open("generic_answers.txt","r") as file:
    lines = file.readlines()

df = pd.DataFrame(lines, columns=["text"])

model = SentenceTransformer("all-MiniLM-L6-v2")

# Database Creation
qdrant = QdrantClient("localhost", port=6333)

collection_name = "restaurant_review_answers"

qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)


df["encoded"] = model.encode(df["text"].tolist()).tolist()

    
qdrant.upsert(
    collection_name=collection_name,
    points=[
        PointStruct(
            id=idx,
            vector=row["encoded"],
            payload={"answer": (row["text"])},
        )
        for idx, row in df.iterrows()
    ],
)


print("Number of answers", qdrant.count(collection_name=collection_name))

# Creation and download of the snapshot
print("\n\nCreating Full Snapshot")
description = qdrant.create_full_snapshot()
url = f"http://localhost:6333/snapshots/{description.name}"
response = requests.get(url)

with open("full_snapshot.snapshot", "wb") as file:
    file.write(response.content)

print("full_snapshot.snapshot")
