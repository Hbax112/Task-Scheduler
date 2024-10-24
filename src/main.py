from task_scheduler import TaskScheduler, get_user_task

def main():
    """
    Funcția principală care inițializează și gestionează interacțiunea cu TaskScheduler.
    """
    scheduler = TaskScheduler()

    while True:
        print("\nSelect an option:")
        print("1. Add a task")
        print("2. Get the next task")
        print("3. View all tasks")
        print("4. Mark task as completed")
        # print("5. Get and complete next important task")
        print("5. View all completed tasks")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            user_task = get_user_task()
            scheduler.add_task(user_task)
            print("Task added successfully!")
        elif choice == '2':
            next_task = scheduler.get_next_task()
            if next_task is not None:
                print(f"Next task: {next_task}")
            else:
                print("No tasks in the scheduler.")
        elif choice == '3':
            scheduler.view_all_tasks()
        elif choice == '4':
            task_index = int(input("Enter the index of the task to mark as completed: ")) - 1
            if 0 <= task_index < len(scheduler.tasks):
                scheduler.complete_task(task_index)  # Pass the index, not the task object
            else:
                print("Invalid task index.")
        elif choice == '5':
            scheduler.view_completed_tasks()
        elif choice == '6':
            print("Exiting the task scheduler.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
