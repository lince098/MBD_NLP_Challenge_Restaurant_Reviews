from qdrant_client import QdrantClient


qdrant = QdrantClient("localhost", port=6333)
qdrant.delete_collection("restaurant_review_answers")
