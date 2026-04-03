import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"
COMPLETE_FILE = "completeTasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return[]
    with open(TASKS_FILE, "r") as file:
        return json.load(file)
    
def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def load_completetasks():
    if not os.path.exists(COMPLETE_FILE):
        print("Nothing complete yet")
        return[]
    with open(COMPLETE_FILE, "r") as file:
        return json.load(file)
    
def save_completetask(tasks):
    with open(COMPLETE_FILE, "w") as file:
        json.dump(tasks, file, indent=2)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, nargs="?", help="Task to add")
    parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
    parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")

    parser.add_argument("-u", "--update", action="store_true", help="Move all complete tasks to a new list")
    parser.add_argument("-lc", "--listcomplete", action="store_true", help="List all finished tasks")
    parser.add_argument("-r", "--reset", action="store_true", help="Delete all completed and current tasks to start a new list")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    if args.list:
        tasks = load_tasks()
        if not tasks:
            print("No tasks to do!")
        else:
            for task in tasks:
                status = "x" if task["done"] else " "
                print(f"[{status}] {task['id']}: {task['task']}")
            sys.exit(0)
    elif args.complete:
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.complete:
                task["done"] = True
                save_task(tasks)
                print(f"Task {args.complete} marked as complete")
                break
    elif args.reset:
        print("Pick an option below via typing its number")
        print("option 1 delete all tasks")
        print("option 2 only delete finished tasks")
        print("option 3 only delete current tasks")
        print("option 4 cancel")

        choice = input("Enter 1, 2, 3, 4: ")

        if choice == "1":
            save_completetask([])
            save_task([])
            print("All tasks reset!")
        if choice == "2":
            save_completetask([])
            print("Finished tasks reset!")
        if choice == "3":
            save_task([])
            print("Current tasks reset!")
        if choice == "4":
            print("Canceled!")


    elif args.update:
        tasks = load_tasks()
        completed_tasks = []
        remaining_tasks = []

        for task in tasks:
            if task["done"]:
                completed_tasks.append(task)
            else:
                remaining_tasks.append(task)

        old_completed = load_completetasks()
        all_completed = old_completed + completed_tasks
        
        save_completetask(all_completed)
        save_task(remaining_tasks)

        print("Completed tasks moved to completed list")

    if args.listcomplete:
        tasks = load_completetasks()
        print(f"Complete tasks:")
        for task in tasks:
            status = "x" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['task']}")
        sys.exit(0)

    elif args.delete:
        tasks = load_tasks()
        new_tasks = []
        for task in tasks:
            if task["id"] != args.delete:
                new_tasks.append(task)
        tasks = new_tasks
        save_task(tasks)
        print(f"Task number {args.delete} was deleted")
    elif args.task:
        tasks = load_tasks()
        if len(tasks) == 0:
            new_id = 1
        else:
            new_id = tasks[-1]["id"] + 1
        tasks.append({"id": new_id, "task": args.task, "done": False})
        save_task(tasks)

        print(f"Task {args.task} added with ID of {new_id}")
if __name__ == "__main__":
    main()        

