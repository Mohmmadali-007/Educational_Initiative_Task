import re
from datetime import datetime

class Task:
    def __init__(self, description, completed, due_date):
        self.description = description
        self.completed = completed
        self.due_date = due_date

class TaskManager:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.due_date = ""

    def setCompleted(self, comp):
        self.completed = comp
        return self

    def setDueDate(self, date):
        if self.isValidDate(date):
            self.due_date = date
        else:
            print("\n----Invalid date format or past date. Please enter a future date in DD/MM/YYYY format.---\n")
        return self

    def build(self):
        return Task(self.description, self.completed, self.due_date)

    def isValidDate(self, date):
        date_pattern = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(date_pattern, date):
            return False  # Invalid format

        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
            if parsed_date <= datetime.now():
                return False  # Past date
        except ValueError:
            return False  # Invalid date

        return True  # Valid date

class TaskList:
    def __init__(self):
        self.tasks = []

    def addTask(self, task):
        self.tasks.append(task)

    def markTaskCompleted(self, task_number):
        pending_task_count = 0
        for task in self.tasks:
            if not task.completed:
                pending_task_count += 1
                if pending_task_count == task_number:
                    task.completed = True
                    return

    def deleteTask(self, task_number):
        if 1 <= task_number <= len(self.tasks):
            del self.tasks[task_number - 1]
            print("\n---------Task deleted successfully.---------\n")
        else:
            print("\n---------Invalid task number. No task deleted.---------\n")

    def viewTasks(self, filter):
        print()
        for task in self.tasks:
            if (
                filter == "Show all"
                or (filter == "Show completed" and task.completed)
                or (filter == "Show pending" and not task.completed)
            ):
                print("\n----------------------------------------------\n")
                print("Following are the list of tasks: \n")
                print(f" {task.description} - {'----Completed----' if task.completed else '----Pending----'}", end="")
                if task.due_date:
                    print(f", Due: {task.due_date}")
                else:
                    print()
        print("\n----------------------------------------------\n")

def markPendingTaskCompleted(task_list):
    task_number = 1
    print("Pending Tasks:")
    for task in task_list.tasks:
        if not task.completed:
            print(f"{task_number}. {task.description}", end="")
            if task.due_date:
                print(f", Due: {task.due_date}")
            else:
                print()
            task_number += 1

    selected_task = int(input("Enter the number of the task to mark as completed: "))
    if 1 <= selected_task <= task_number - 1:
        task_list.markTaskCompleted(selected_task)
        print("\n---------Task marked as completed.----------\n")
        print()
    else:
        print("\n---------Invalid task number. No task marked as completed.---------\n")

def deleteTaskByNumber(task_list):
    task_number = 1
    print("All Tasks:")
    for task in task_list.tasks:
        print(f"{task_number}. {task.description}", end="")
        if task.due_date:
            print(f", Due: {task.due_date}")
        else:
            print()
        task_number += 1

    selected_task = int(input("Enter the number of the task to delete: "))
    if 1 <= selected_task <= task_number - 1:
        task_list.deleteTask(selected_task)
        print()
    else:
        print("\n-----------Invalid task number. No task deleted.---------\n")

if __name__ == "__main__":
    task_list = TaskList()

    while True:
        print("Options:")
        print("1. Add Task")
        print("2. Mark Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Exit")
        choice_str = input("Enter your choice: ")

        try:
            choice = int(choice_str)
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        if choice < 1 or choice > 5:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            description = input("Enter task description: ")
            due_date = ""
            while True:
                print("Enter due date in DD/MM/YYYY format (optional): ")
                due_date = input()
                task_manager = TaskManager(description)
                if due_date:
                    task_manager.setDueDate(due_date)
                if task_manager.isValidDate(due_date):
                    break
            task = task_manager.build()
            task_list.addTask(task)
            print("Task added successfully.")
            print()
        elif choice == 2:
            markPendingTaskCompleted(task_list)
        elif choice == 3:
            deleteTaskByNumber(task_list)
        elif choice == 4:
            filter_choice = input("Options:\n1. Show all\n2. Show completed\n3. Show pending\nEnter your choice: ")
            if filter_choice == "1":
                filter = "Show all"
            elif filter_choice == "2":
                filter = "Show completed"
            elif filter_choice == "3":
                filter = "Show pending"
            else:
                filter = "Show all"
            task_list.viewTasks(filter)
        elif choice == 5:
            break
