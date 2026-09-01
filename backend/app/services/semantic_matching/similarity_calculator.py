import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

# Try importing sentence_transformers
_model = None
try:
    from sentence_transformers import SentenceTransformer
    try:
        # Load lightweight, fast model for semantic embedding
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("SentenceTransformer model 'all-MiniLM-L6-v2' loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load SentenceTransformer model: {e}")
        _model = None
except ImportError:
    _model = None


class SimilarityCalculator:
    """Computes semantic similarity between text strings using Sentence Transformers and vector Cosine Similarity."""

    # Taxonomy domain map for known skill relationships
    TAXONOMY_RELATIONS = {
        ("scikit-learn", "machine learning"): 0.88,
        ("sklearn", "machine learning"): 0.88,
        ("pytorch", "deep learning"): 0.90,
        ("pytorch", "machine learning"): 0.85,
        ("tensorflow", "deep learning"): 0.90,
        ("tensorflow", "machine learning"): 0.85,
        ("react", "frontend framework"): 0.92,
        ("react", "frontend"): 0.90,
        ("fastapi", "rest api"): 0.88,
        ("fastapi", "backend"): 0.85,
        ("postgresql", "relational database"): 0.90,
        ("postgresql", "database"): 0.85,
        ("docker", "containerization"): 0.92,
        ("kubernetes", "container orchestration"): 0.92,
        ("aws", "cloud platform"): 0.90,
        ("gcp", "cloud platform"): 0.90,
    }

    def compute_cosine_similarity(self, text1: str, text2: str) -> float:
        """Computes cosine similarity between two text snippets."""
        if not text1 or not text2:
            return 0.0

        t1_clean = text1.strip().lower()
        t2_clean = text2.strip().lower()

        # Exact match check
        if t1_clean == t2_clean:
            return 1.0

        # Substring contained check
        if t1_clean in t2_clean or t2_clean in t1_clean:
            return 0.95

        # Check domain taxonomy relation map
        key1 = (t1_clean, t2_clean)
        key2 = (t2_clean, t1_clean)
        if key1 in self.TAXONOMY_RELATIONS:
            return self.TAXONOMY_RELATIONS[key1]
        if key2 in self.TAXONOMY_RELATIONS:
            return self.TAXONOMY_RELATIONS[key2]

        # Sentence Transformers vector cosine similarity
        if _model is not None:
            try:
                embeddings = _model.encode([text1, text2])
                v1 = embeddings[0]
                v2 = embeddings[1]

                norm1 = np.linalg.norm(v1)
                norm2 = np.linalg.norm(v2)

                if norm1 > 0 and norm2 > 0:
                    sim = float(np.dot(v1, v2) / (norm1 * norm2))
                    return max(0.0, min(1.0, round(sim, 4)))
            except Exception as e:
                logger.debug(f"SentenceTransformer encoding fallback: {e}")

        # Fallback word overlap / Jaccard similarity
        words1 = set(t1_clean.split())
        words2 = set(t2_clean.split())
        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)
        jaccard = len(intersection) / len(union) if union else 0.0

        return max(0.0, min(1.0, round(jaccard, 4)))

    def compute_matrix_similarity(self, texts1: List[str], texts2: List[str]) -> np.ndarray:
        """Computes pairwise cosine similarity matrix between two lists of text strings."""
        if not texts1 or not texts2:
            return np.zeros((len(texts1), len(texts2)))

        matrix = np.zeros((len(texts1), len(texts2)))
        for i, t1 in enumerate(texts1):
            for j, t2 in enumerate(texts2):
                matrix[i, j] = self.compute_cosine_similarity(t1, t2)

        return matrix


similarity_calculator = SimilarityCalculator()
