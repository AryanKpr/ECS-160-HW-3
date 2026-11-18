from unittest.mock import patch, MagicMock
import grpc

import moderation_service
from moderation_service import moderate, ModerateRequest, check_moderation
import hashtagging_pb2


def test_banned_post_returns_failed_without_grpc():
    # Replace the stub with a fake, so we can check it's never called
    with patch.object(moderation_service, "stub") as fake_stub:
        response = moderate(ModerateRequest(post_content="This crypto scheme is terrible"))
        assert response.result == "FAILED"
        fake_stub.GetHashtag.assert_not_called()      # blocked before gRPC


def test_clean_post_returns_hashtag_from_service():
    with patch.object(moderation_service, "stub") as fake_stub:
        # Tell the fake stub what to "return over gRPC"
        fake_stub.GetHashtag.return_value = hashtagging_pb2.HashtagResponse(hashtag="#Hiking")
        response = moderate(ModerateRequest(post_content="Just hiked to the top of a mountain!"))
        assert response.result == "#Hiking"
        fake_stub.GetHashtag.assert_called_once()