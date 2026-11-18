import grpc
from concurrent import futures
import os

from google import genai

import hashtagging_pb2
import hashtagging_pb2_grpc

# Configure Gemini
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
MODEL = "gemini-2.0-flash"



def generate_hashtag(post_content):
    prompt = (
        "Generate exactly one hashtag that best describes this social media post. "
        "Reply with only the hashtag, starting with #, and nothing else.\n\n"
        f"Post: {post_content}"
    )
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        for word in response.text.split():          # e.g. "Here's one: #BeachVibes"
            if word.startswith("#") and len(word) > 1:
                return word.strip(".,!?\"'")
    except Exception as e:
        print(f"Gemini error: {e}")
    return "#bskypost"


class HashtagServiceServicer(hashtagging_pb2_grpc.HashtagServiceServicer):
    def GetHashtag(self, request, context):
        hashtag = generate_hashtag(request.post_content)
        return hashtagging_pb2.HashtagResponse(hashtag=hashtag)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hashtagging_pb2_grpc.add_HashtagServiceServicer_to_server(HashtagServiceServicer(), server)
    server.add_insecure_port("[::]:50051")   # adjust if test_pipeline.sh uses another port
    server.start()
    print("Hashtagging gRPC server listening on port 50051")
    server.wait_for_termination()
    


if __name__ == "__main__":
    serve()
