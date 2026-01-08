## Applied Mmory for Agents

The goal of this project was to learn to how build an AI assistant with persistent memory and semantic recall by implementing conversation history strategies, structured key-value storage, vector search, and tool-based task management. 
The final version is a personal agent that remembers past interactions, retrieves information meaningfully, and updates tasks through autonomous tool calls.

### Summary

A full personal assistant agent that maintains conversation context, stores tasks persistently, and calls tools (create, search, update tasks) automatically.


### To run the script
* You need to add a `.env` file with your OpenRouter API KEY  and the Base URL of OpenRouter

```env
OPENROUTER_API_KEY=sk-xxxxx
OPENAI_BASE_URL=https://openrouter.ai/api/v1

* You also need to have a Vector Store running.
Run the docker command: `docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z"   qdrant/qdrant`

As I don't want to install docker on my laptop, I used a VM with docker already installed.
Then on my laptop I create a SSH tunnel: ` ssh -L 6333:127.0.0.1:6333 <VM_user>@<VM-IP>`
