import json
from datetime import date
from typing import Optional

DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday", "General"
]

class Task:
    """Represents a single task."""

    _id_counter = 0  # class-level counter for unique task IDs

    def __init__(
        self,
        day: str,
        description: str,
        priority: str = "medium",
        due_date: Optional[date] = None,
    ):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.day = day
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = "pending"  # default status

    def mark_done(self):
        self.status = "done"

    def __str__(self):
        return (
            f"[ID: {self.id}] "
            f"{self.description} | "
            f"Status: {self.status} | "
            f"Priority: {self.priority} | "
            f"Due: {self.due_date}"
        )


class TaskManager:
    """Manages tasks organized by day of the week."""

    def __init__(self):
        self.tasks_by_day = {}  # e.g. {"Monday": [Task, Task]}

    # --------------------------------------------------
    # Adding a New Task
    # --------------------------------------------------
    def add_task(
        self,
        day: str,
        description: str,
        priority: str = "medium",
        due_date: Optional[date] = None,
    ):
        task = Task(day, description, priority, due_date)

        if day not in self.tasks_by_day:
            self.tasks_by_day[day] = []

        self.tasks_by_day[day].append(task)
        return task

    # --------------------------------------------------
    # Marking a Task as Done
    # --------------------------------------------------
    def mark_task_done(self, day: str, task_index: int):
        try:
            task = self.tasks_by_day[day][task_index]
            task.mark_done()
            return task
        except (KeyError, IndexError):
            raise ValueError("Invalid day or task index")

    # --------------------------------------------------
    # Editing Existing Tasks
    # --------------------------------------------------
    def edit_task(
        self,
        day: str,
        task_index: int,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[date] = None,
    ):
        try:
            task = self.tasks_by_day[day][task_index]
        except (KeyError, IndexError):
            raise ValueError("Invalid day or task index")

        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date

        return task

    # --------------------------------------------------
    # Viewing Tasks
    # --------------------------------------------------
    def view_tasks(self, day: Optional[str] = None):
        if day:
            tasks = self.tasks_by_day.get(day, [])
            return {day: tasks}
        return self.tasks_by_day

    def display_tasks(self, day: Optional[str] = None):
        tasks_to_show = self.view_tasks(day)

        if not tasks_to_show:
            print("No tasks found.")
            return

        for day_name, tasks in tasks_to_show.items():
            print(f"\n{day_name}:")
            if not tasks:
                print("  No tasks.")
            for i, task in enumerate(tasks):
                print(f"  {i}. {task}")

    # --------------------------------------------------
    # Save tasks to a JSON file
    # --------------------------------------------------
    def save_to_file(self, filename: str):
        data = {}

        for day in DAYS:
            tasks = self.tasks_by_day.get(day, [])
            data[day] = []

            for task in tasks:
                data[day].append({
                    "task": task.description,
                    "status": task.status.capitalize()
                })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        #print(f"Tasks saved to {filename}")

    # --------------------------------------------------
    # Load tasks from JSON (expects all days + General)
    # --------------------------------------------------
    def load_from_file(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.tasks_by_day.clear()

        for day in DAYS:
            self.tasks_by_day[day] = []

            for task_data in data.get(day, []):
                task = Task(
                    day=day,
                    description=task_data["task"]
                )
                task.status = task_data["status"].lower()
                self.tasks_by_day[day].append(task)

        #print(f"Tasks loaded from {filename}")


def main():
    manager = TaskManager()

    while True:
        command = input(
            "Enter command (add/edit/done/view/save/load/quit): "
        ).strip().lower()

        if command == "quit":
            #print("Goodbye!")
            break

        elif command == "save":
            filename = input("Enter filename (default: tasks.json): ").strip()
            if filename == "":
                filename = "tasks.json"
            manager.save_to_file(filename)

        elif command == "load":
            filename = input("Enter filename (default: tasks.json): ").strip()
            if filename == "":
                filename = "tasks.json"
            manager.load_from_file(filename)

        elif command == "add":
            day = input("Enter day: ").strip()
            description = input("Enter task: ").strip()

            manager.add_task(day, description)
            #print("Task added.")

        elif command == "done":
            day = input("Enter day: ").strip()

            try:
                task_index = int(input("Enter task index: ").strip())
                task = manager.mark_task_done(day, task_index)
                #print(f"Task marked as done: {task.description}")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "edit":
            day = input("Enter day: ").strip()

            try:
                task_index = int(input("Enter task index: ").strip())
            except ValueError:
                print("Invalid task index.")
                continue

            #print("Leave input blank to keep current value.")
            new_description = input("Enter new description: ").strip()
            #new_priority = input("Enter new priority: ").strip()
            #new_due_date = input("Enter new due date: ").strip()

            manager.edit_task(
                day,
                task_index,
                description=new_description or None,
            )
            #print("Task updated.")

        elif command == "view":
            day = input("Enter day (or leave blank to view all): ").strip()

            tasks_by_day = manager.view_tasks(day if day else None)

            if not tasks_by_day:
                print("No tasks found.")
                continue

            for day_name, tasks in tasks_by_day.items():
                print(f"\n{day_name}:")
                #if not tasks:
                    #print("  No tasks.")
                for i, task in enumerate(tasks):
                    status = task.status.capitalize()
                    print(f"{i}: {task.description} - {status}")

        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    # Write your solution here
    main()
