import pytest
import torch
from embedding.embedding_local import get_embedding


def test_get_embedding():
    # Test input
    test_text = "This is a test sentence."

    # Call the function
    embedding = get_embedding(test_text)

    # Assertions
    assert isinstance(embedding, list), "Embedding should be a list"
    assert len(embedding) > 0, "Embedding should not be empty"
    assert all(isinstance(x, float) for x in embedding), "All elements should be floats"

    # Check if the embedding is normalized (L2 norm should be close to 1)
    tensor_embedding = torch.tensor(embedding)
    norm = torch.norm(tensor_embedding)
    assert 0.99 <= norm.item() <= 1.01, "Embedding should be approximately normalized"

    # Test with empty string
    empty_embedding = get_embedding("")
    assert isinstance(empty_embedding, list), "Empty string should still return a list"

    # Test with very long text
    long_text = "This is a very long text. " * 1000
    long_embedding = get_embedding(long_text)
    assert isinstance(long_embedding, list), "Long text should still return a list"
    assert len(long_embedding) == len(embedding), "Embedding dimension should be consistent"


@pytest.mark.parametrize("input_text", [
    "Hello, world!",
    "Python is awesome",
    "Machine learning is fascinating",
    "1234567890",
    "!@#$%^&*()",
])
def test_get_embedding_various_inputs(input_text):
    embedding = get_embedding(input_text)
    assert isinstance(embedding, list), f"Embedding for '{input_text}' should be a list"
    assert len(embedding) > 0, f"Embedding for '{input_text}' should not be empty"
