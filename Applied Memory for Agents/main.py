from openai import OpenAI
import os
import dotenv
from tinydb import TinyDB, Query
from enum import Enum

dotenv.load_dotenv()

CLIENT = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)


class ContextManager:
    def __init__(self):
        self.messages: list[dict] = []

    def add_user_message(self, message: str):
        self.messages.append({
            "role": "user", "content": message
        })

    def update_messages(self, messages: list[dict]):
        self.messages = messages

    def get_repr(self):
        """Function for showing context for easier solving of optional tasks"""
        msgs = []
        for elem in self.messages:
            if type(elem) is dict:
                if 'role' in elem:
                    msgs.append(elem['role'] + ': ' + elem['content'][:15] + '...')
                else:
                    msgs.append(elem['type'] + ': ' + elem['output'][:15] + '...')
            else:
                msgs.append(str(elem.type))
        return 'Context:\n\t' + "\n\t".join(msgs) + '\n-------'

    def get_context(self) -> list[dict]:
        return self.messages.copy()

    def compact(self):
        compacted = []
        for msg in self.messages:
            if isinstance(msg, dict) and msg.get("role") in {"user", "assistant"}:
                compacted.append(msg)
        self.messages = compacted

    def reset(self):
        self.messages = []


class MatchType(Enum):
    EQ = "eq"
    CONTAINS = "contains"


class TasksStore:
    VALID_STATUSES = {"to-do", "in-progress", "done"}

    def __init__(self):
        self.db = TinyDB('tasks.json')

    def create_task(self, name: str, status: str) -> str:
        if status not in self.VALID_STATUSES:
            return f"Invalid status '{status}'. Valid statuses: {', '.join(self.VALID_STATUSES)}"

        self.db.insert({
            "name": name,
            "status": status
        })
        return f"Task '{name}' created with status '{status}'."

    def find_task(self, key: str, value: str, match: MatchType = MatchType.EQ) -> str:
        Task = Query()

        if match == MatchType.EQ.value:
            results = self.db.search(Task[key] == value)
        elif match == MatchType.CONTAINS.value:
            results = self.db.search(Task[key].matches(value))
        else:
            return "Invalid match type."

        if not results:
            return "No matching tasks found."

        return "Found tasks:\n" + "\n".join(
            f"- {task['name']} [{task['status']}]" for task in results
        )

    def update_task_status(self, name: str, new_status: str) -> str:
        if new_status not in self.VALID_STATUSES:
            return f"Invalid status '{new_status}'. Valid statuses: {', '.join(self.VALID_STATUSES)}"

        Task = Query()
        updated = self.db.update(
            {"status": new_status},
            Task.name == name
        )

        if not updated:
            return f"No task found with name '{name}'."

        return f"Task '{name}' updated to status '{new_status}'."

    def flush(self):
        self.db.truncate()


class PersonalAssistant:
    def __init__(self):
        """
        TODO: fill tools list with correct tool descriptions. Match tool names to function names. And tool parameters to function parameters.

        As a hint, check how tool_result is obtained during tool call phase.
        """
        self.tools = [
            {
                "type": "function",
                "name": "find_task",
                "description": "Find tasks by a field value (exact or pattern match).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {"type": "string", "description": "Field name to search (name or status)."},
                        "value": {"type": "string", "description": "Field value to match."},
                        "match": {
                            "type": "string",
                            "enum": ["eq", "contains"],
                            "description": "Match type (exact or contains).",
                            "default": "eq"  # default makes it optional
                        }
                    },
                    "required": ["key", "value"],  # match is optional because it has a default
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "create_task",
                "description": "Create a new task with a name and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name"},
                        "status": {
                            "type": "string",
                            "enum": ["to-do", "in-progress", "done"],
                            "description": "Initial task status"
                        }
                    },
                    "required": ["name", "status"],
                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "update_task_status",
                "description": "Update the status of an existing task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Task name"},
                        "new_status": {
                            "type": "string",
                            "enum": ["to-do", "in-progress", "done"],
                            "description": "New task status"
                        }
                    },
                    "required": ["name", "new_status"],
                    "additionalProperties": False
                }
            }
        ]

        # to store data
        self.tasks_store = TasksStore()

        self.tool_map = {
            "find_task": self.tasks_store.find_task,
            "create_task": self.tasks_store.create_task,
            "update_task_status": self.tasks_store.update_task_status
        }
        # to manage context
        self.context_manager = ContextManager()

    def send_message(self, message: str) -> str:
        self.context_manager.add_user_message(message)
        context = self.context_manager.get_context()
        context = self._call_llm(context)
        self.context_manager.update_messages(context)
        return context[-1].content[0].text

    def _call_llm(self, messages: list[dict]) -> list[dict]:
        """
        Handles LLM calls and executes tools if requested.
        Appends tool results correctly in the format expected by OpenAI Responses API.
        """

        response = CLIENT.responses.create(
            model="gpt-4o-mini",
            input=messages,
            tools=self.tools
        )

        # Append the model output
        messages += response.output

        # Check if the last output is a tool call
        for item in response.output:
            if item.type == "function_call":
                # Execute the tool
                tool_result = self.tool_map[item.name](**eval(item.arguments))

                # Append the function call output in correct format
                messages.append({
                    "type": "function_call_output",
                    "call_id": item.id,  # link output to the original function call
                    "name": item.name,
                    "output": str(tool_result)
                })

                # Recursive call to let the model see the tool output and respond
                return self._call_llm(messages)

        # If there are no more function calls, return messages
        return messages

    def flush(self):
        self.tasks_store.flush()
        self.context_manager.reset()


def main():
    """Main conversation loop"""
    assistant = PersonalAssistant()
    while True:
        try:
            user_input = input("User: ").strip()
            if not user_input:
                continue

            # Process special commands
            if user_input == "/q":
                break
            elif user_input == "/flush":
                assistant.flush()
                print("[INFO] Flushed")
                continue

            # Process normal message
            response = assistant.send_message(user_input)
            print(f"Assistant: {response}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

