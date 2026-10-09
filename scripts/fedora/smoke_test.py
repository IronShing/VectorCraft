"""Quick end-to-end check that VectorCraft works on this machine.

Run with the VectorCraft environment's Python, e.g.:
    vectorcraft-python scripts/fedora/smoke_test.py
"""
import platform

import numpy as np
from langchain_core.embeddings import FakeEmbeddings

from vectorcraft.utils.math import cosine_similarity
from vectorcraft.vectorstores import FAISS

print(f"Python {platform.python_version()} on {platform.platform()}")
print(f"numpy {np.__version__}")

sim = cosine_similarity([[1.0, 0.0]], [[1.0, 1.0]])
assert abs(sim[0][0] - 2**-0.5) < 1e-9, sim

db = FAISS.from_texts(["apple", "banana", "car"], FakeEmbeddings(size=8))
assert len(db.similarity_search("apple", k=2)) == 2
assert len(db.max_marginal_relevance_search("apple", k=2)) == 2

print("VectorCraft smoke test passed")
