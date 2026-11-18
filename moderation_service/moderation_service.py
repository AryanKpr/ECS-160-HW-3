from fastapi import FastAPI
from pydantic import BaseModel
import grpc

import hashtagging_pb2
import hashtagging_pb2_grpc

app = FastAPI()

BANNED_WORDS = [
    "illegal", "fraud", "scam", "exploit", "dox", "swatting", "hack", "crypto", "bots"
]

class ModerateRequest(BaseModel):
    post_content: str


class ModerateResponse(BaseModel):
    result: str


def check_moderation(text):
    lowered = text.lower()
    for word in BANNED_WORDS:      
        if word in lowered:        
            return False         
    return True 
       
         

channel = grpc.insecure_channel("localhost:50051")
stub = hashtagging_pb2_grpc.HashtagServiceStub(channel)

def get_hashtag_from_service(post_content):
    try:
        request = hashtagging_pb2.HashtagRequest(post_content=post_content)
        response = stub.GetHashtag(request) #looks like a local call; the stub sends it over the network
        return response.hashtag
    except grpc.RpcError as e:
        print(f"gRPC error: {e}") # hashtagging service down or unreachable
        return "#bskypost"


@app.post("/moderate")
def moderate(request: ModerateRequest):
    if not check_moderation(request.post_content):
        return ModerateResponse(result="FAILED")
    hashtag = get_hashtag_from_service(request.post_content)
    return ModerateResponse(result=hashtag)
