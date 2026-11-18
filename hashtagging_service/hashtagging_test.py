import os
os.environ.setdefault("GOOGLE_API_KEY", "test-key")  

from unittest.mock import patch, MagicMock
import hashtagging_service
from hashtagging_service import generate_hashtag


def test_generate_hashtag_extracts_hashtag_from_reply():
    with patch.object(hashtagging_service, "client") as fake_client:
        # Fake Gemini reply with extra words and punctuation
        fake_client.models.generate_content.return_value.text = "Here's one: #Mountains!"
        assert generate_hashtag("Hiked to the summit today") == "#Mountains"


def test_gemini_failure_returns_default():
    with patch.object(hashtagging_service, "client") as fake_client:
        # Fake Gemini raising an error, like the billing error you saw
        fake_client.models.generate_content.side_effect = Exception("402 credits depleted")
        assert generate_hashtag("Anything") == "#bskypost"

def test_gemini_refusal_returns_default():
    with patch.object(hashtagging_service, "client") as fake_client:
        # Fake Gemini reply with no hashtag in it
        fake_client.models.generate_content.return_value.text = "I can't help with that."
        assert generate_hashtag("Some post") == "#bskypost"