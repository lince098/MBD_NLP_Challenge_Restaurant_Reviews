import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import requests
from sentence_transformers import SentenceTransformer
import time

# Read and preprocess articles extracted
with open("generic_answers.txt", "r") as file:
    lines = file.readlines()

df = pd.DataFrame(lines, columns=["text"])

model = SentenceTransformer("all-MiniLM-L6-v2")

# Database Creation
qdrant = QdrantClient("localhost", port=6333)

collection_name = "restaurant_review_answers"


# Testing
# qdrant.delete_collection(collection_name)
# print(f"deleted collection: {collection_name}")
# end Testing

print(f"created collection: {collection_name}")
qdrant.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

# I didn't used batches because it only loads 30 answers
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

previous_number_of_snapshots = len(qdrant.list_full_snapshots())

try:
    description = qdrant.create_full_snapshot()
except Exception:
    print("Timeout Exception, getting all snapshots, ordering and taking the lastest.")
    time.sleep(10)
    while True:
        snapshot_list = qdrant.list_full_snapshots()
        if len(snapshot_list) > previous_number_of_snapshots:
            break

    f = lambda x: x.creation_time
    # Gets the latest snapshot uploaded
    description = list(sorted(snapshot_list, key=f, reverse=True))[0]

print("Snapshot description:", description, "\n")

url = f"http://localhost:6333/snapshots/{description.name}"

response = requests.get(url)

with open(description.name, "wb") as file:
    file.write(response.content)

print(f"Snapshot saved in: ./{description.name}")
