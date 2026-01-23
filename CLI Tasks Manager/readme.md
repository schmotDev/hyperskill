## CLI Tasks Manager

# Python Task Manager

A simple command-line task manager written in Python that allows users to
organize tasks by day of the week and persist them using a JSON file.

---

## Summary

The Python Task Manager is a lightweight CLI application designed to help
users manage their daily tasks in a structured way. Tasks are grouped by
day (Monday through Sunday, plus a General category) and can be added,
edited, marked as completed, viewed, saved, and loaded from a JSON file.

This project was built as a learning exercise to demonstrate:
- Object-oriented programming in Python
- Interactive command-line interfaces
- Basic data persistence using JSON
- Clean project structure suitable for GitHub

---

## How to Run the Script

### Prerequisites
- Python 3.8 or higher

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/python-task-manager.git

    Navigate into the project directory:

    cd python-task-manager

    Run the script:

    python task_manager.py

You will be prompted with:

Enter command (add/edit/done/view/save/load/quit):

Examples of Usage
Adding a Task

Enter command (add/edit/done/view/save/load/quit): add
Enter day: Monday
Enter task: Buy groceries

Viewing Tasks for a Specific Day

Enter command (add/edit/done/view/save/load/quit): view
Enter day (or leave blank to view all): Monday
0: Buy groceries - Pending

Marking a Task as Done

Enter command (add/edit/done/view/save/load/quit): done
Enter day: Monday
Enter task index: 0

Saving Tasks to a File

Enter command (add/edit/done/view/save/load/quit): save
Enter filename: tasks.json

Loading Tasks from a File

Enter command (add/edit/done/view/save/load/quit): load
Enter filename: tasks.json

Exiting the Program

Enter command (add/edit/done/view/save/load/quit): quit

JSON Storage Format

Tasks are saved using the following structure:

{
  "Monday": [],
  "Tuesday": [],
  "Wednesday": [],
  "Thursday": [],
  "Friday": [],
  "Saturday": [],
  "Sunday": [],
  "General": []
}

Each task contains:

    task: task description

    status: Pending or Done

