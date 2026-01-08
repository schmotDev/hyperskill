## Applied Mmory for Agents

The goal of this project was to learn to how build an AI assistant with persistent memory and semantic recall by implementing conversation history strategies, structured key-value storage, vector search, and tool-based task management. 
The final version is a personal agent that remembers past interactions, retrieves information meaningfully, and updates tasks through autonomous tool calls.

<br>
### Summary

A full personal assistant agent that maintains conversation context, stores tasks persistently, and calls tools (create, search, update tasks) automatically.

<br>
### To run the script
* You need to add a `.env` file with your OpenRouter API KEY  and the Base URL of OpenRouter

```.env
OPENROUTER_API_KEY=sk-xxxxx
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

<br>
### Example of conversation with the agent

```
python main.py

User: hey, create task "do laundry"
Assistant: The task "do laundry" has been created and is marked as to-do.

User: ok. create task "call Lucy"
Assistant: The task "call Lucy" has been created and is marked as to-do.

User: I just started to do laundry
Assistant: The task "do laundry" is now marked as in-progress.

User: what are tasks in todo?
Assistant: The task in todo is "call Lucy."

User: what are tasks in progress?
Assistant: The task in progress is "do laundry."

User: /flush
[INFO] Flushed

User: what are tasks in progress?
Assistant: There are no tasks currently in progress.

User: /q
```
