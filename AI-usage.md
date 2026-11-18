
# ECS 160 HW: Moderation and Hashtagging Microservices

A pipeline of two microservices that processes the top-10 most-liked posts in `input.csv`:

- **Moderation service** (`moderation_service/`, FastAPI, port 8001): checks each post
  against a list of banned words (case-insensitive). Returns `FAILED` for banned posts;
  otherwise forwards the post to the hashtagging service over gRPC and returns its hashtag.
- **Hashtagging service** (`hashtagging_service/`, gRPC, port 50051): generates a hashtag
  using Google Gemini, falling back to `#bskypost` if Gemini fails or returns no hashtag.
- **Client** (`client/main.py`): loads the posts, selects the 10 most-liked, sends each to
  the moderation service over HTTP, and prints each post with its hashtag, or `[DELETED]`.

## Running

    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    export GOOGLE_API_KEY="your-key"

    # Terminal 1
    cd hashtagging_service && python3 hashtagging_service.py
    # Terminal 2
    cd moderation_service && uvicorn moderation_service:app --port 8001
    # Terminal 3
    cd client && python3 main.py ../input.csv

Tests: `python3 -m pytest moderation_service/test_moderation.py hashtagging_service/test_hashtagging.py -v`

## AI Usage Disclosure

I used Claude (Anthropic) as a study aid and tutor while completing this assignment.

**How I used it:**
- To understand the lecture concepts this assignment depends on: gRPC, Protocol Buffers,
  stubs and servicers, and how they map onto the Java examples in the slides.
- To understand the handout's test script, so my output format and ports matched it.
- To debug errors as I worked (missing generated files, imports, environment variables,
  Gemini API setup), by explaining what each error meant.
- To review code I wrote. It pointed out bugs, which I then fixed, for example in
  `check_moderation`, `moderate`, `send_to_pipeline`, and `process_post`.

**Code that was largely AI-suggested:** the gRPC server setup in `serve()`, the gRPC client
call in `get_hashtag_from_service`, the corrected version of `generate_hashtag` (prompt,
hashtag extraction, and fallback), and most of the unit tests. I added one test myself.

**What I did:** I wrote the initial versions of the service and client functions, ran and
debugged every component, set up the Gemini API, ran the test script and fixed failures, and
reviewed every suggested line until I understood what it does and why it's needed. I did not
copy code I didn't understand.