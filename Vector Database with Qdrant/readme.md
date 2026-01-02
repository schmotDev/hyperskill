##  Vector Database with Qdrant

fundamentals of Qdrant, a vector-first database, including data loading, similarity matching, natural language searching, and building a simple FastAPI interface.


### Summary

Solution for semantic search using Qdrant, using OpenAI's embeddings API to process data, perform similarity searches, and construct an interface that enables retrieval of data points through natural language queries and filtering techniques.


### To run the script
* You need to add a `.env` file with your OpenRouter API KEY  
`OPENROUTER_API_KEY=sk-xxxxx`

* You also need to have a Vector Store running.
Run the docker command: `docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z"   qdrant/qdrant`

As I don't want to install docker on my laptop, I used a VM with docker already installed.
Then on my laptop I create a SSH tunnel: ` ssh -L 6333:127.0.0.1:6333 <VM_user>@<VM-IP>`

Finally, to run the fastAPI app, execute `python -m uvicorn main:app --reload` in the terminal.


You can send request to the app, with commands such as:
` curl -Uri "http://localhost:8000/search" -Method POST -Headers @{ "Content-Type" = "application/json" }  -Body '{"query": "Papers on clustering by Andrew Ng", "top_n": 5}'`
