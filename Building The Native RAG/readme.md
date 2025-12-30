## Butler Agent


### Summary

PoC to learn how to build a complete Retrieval-Augmented Generation (RAG) system. 
Implement the RAG pipeline—from efficient data ingestion and processing, to context-aware generation.


### To run the script
* You need to add a `.env` file with your OpenRouter API KEY  
`OPENROUTER_API_KEY=sk-xxxxx`

* You also need to have a Vector Store running.
Run the docker command: `docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z"   qdrant/qdrant`

As I don't want to install docker on my laptop, I used a VM with docker already installed.
Then on my laptop I create a SSH tunnel: ` ssh -L 6333:127.0.0.1:6333 <VM_user>@<VM-IP>`
