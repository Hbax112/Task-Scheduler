from binomial_heap import BinomialHeap
from b_tree import BTree, BTreeNode
from task import Task
from b_tree_task_completed import BTreeTaskCompleted
from datetime import datetime

class TaskScheduler:
    def __init__(self):
        """
        Inițializează un program de planificare a sarcinilor.
        - task_heap: Heap binomial pentru gestionarea sarcinilor active.
        - tasks: Lista pentru stocarea sarcinilor active.
        - completed_tasks_btree: Arbore B pentru gestionarea sarcinilor finalizate.
        """
        self.task_heap = BinomialHeap()
        self.tasks = []
        self.completed_tasks_btree = BTree(t=2)  # Ajustați 't' după nevoie
        self.load_tasks_from_file()

    def add_task(self, task):
        """
        Adaugă o nouă sarcină în programul de planificare.
        - task: Obiect Task reprezentând sarcina ce urmează a fi adăugată.
        """
        self.task_heap.insert(task)
        self.tasks.append(task)
        self.save_tasks_to_file()  # Salvăm task-urile, inclusiv noul task

    def load_tasks_from_file(self):
        """
        Încarcă sarcinile din fișierul "tasks.txt" în lista de sarcini.
        """
        try:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    priority, description, deadline_str = map(str.strip, data)
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                    task = Task(int(priority), description, deadline)
                    if task not in self.tasks:
                        self.tasks.append(task)
        except FileNotFoundError:
            pass

    def _update_task_heap(self):
        """
        Actualizează heap-ul binomial cu sarcinile din lista de sarcini.
        """
        self.task_heap = BinomialHeap()
        tasks_from_file = self.load_tasks_from_file()
        sorted_tasks = sorted(tasks_from_file, key=lambda t: (t.priority, t.deadline))
        for task in sorted_tasks:
            self.task_heap.insert(task)

    def save_tasks_to_file(self):
        """
        Salvează sarcinile din lista de sarcini în fișierul "tasks.txt".
        """
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task.priority},{task.description},{task.deadline.strftime('%Y-%m-%d')}\n")

    def get_next_task(self):
        """
        Returnează următoarea sarcină din lista de sarcini (cea cu cea mai mare prioritate).
        """
        if not self.tasks:
            print("No tasks in the scheduler.")
            return None

        # Sortează task-urile în funcție de prioritate și deadline
        sorted_tasks = sorted(self.tasks, key=lambda task: (task.priority, task.deadline))

        # Returnează primul task din lista sortată (cel mai important)
        return sorted_tasks[0]

    def view_all_tasks(self):
        """
        Afișează toate sarcinile din lista de sarcini.
        """
        if not self.tasks:
            print("No tasks in the scheduler.")
        else:
            print("All tasks:")
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. Priority: {task.priority}, Description: {task.description}, Deadline: {task.deadline}")

    def complete_task(self, task_index):
        """
        Marchează o sarcină ca fiind completată și o mută în lista de sarcini finalizate.
        - task_index: Indexul sarcinii care trebuie marcată ca fiind completată.
        """
        all_tasks = self.tasks + self.completed_tasks_btree.root.keys

        if not all_tasks:
            print("No tasks to complete.")
            return

        if 0 <= task_index < len(all_tasks):
            task_to_complete = all_tasks[task_index]

            if task_to_complete in self.tasks:
                self.tasks.remove(task_to_complete)
            elif task_to_complete in self.completed_tasks_btree.root.keys:
                self.completed_tasks_btree.root.keys.remove(task_to_complete)

            print(f"Task completed: {task_to_complete}")
            self.completed_tasks_btree.insert(task_to_complete)
            self.save_tasks_to_file()
            self.completed_tasks_btree.save_completed_tasks_to_file()
        else:
            print("Invalid task index.")

    def get_and_complete_next_important_task(self):
        """
        Obține și completează următoarea sarcină importantă.
        """
        next_important_task = self.get_next_important_task()
        if next_important_task:
            self.complete_task(next_important_task)
        else:
            print("No important tasks remaining.")

    def get_next_important_task(self):
        """
        Returnează următoarea sarcină importantă din lista de sarcini.
        """
        if not self.tasks:
            return None

        # Ajustează ponderile în funcție de preferințe
        priority_weight = 0.7
        deadline_weight = 0.3

        # Calculează metrica combinată
        combined_metric = lambda t: (priority_weight * t.priority) + (
                    deadline_weight / (t.deadline - datetime.now().date()).days)

        sorted_tasks = sorted(self.tasks, key=combined_metric, reverse=True)
        return sorted_tasks[0] if sorted_tasks else None

    def save_completed_tasks_to_file(self):
        """
        Salvează sarcinile finalizate în fișierul "completed.txt".
        """
        with open("completed.txt", "w") as file:
            for task in self.completed_tasks:
                file.write(f"{task.priority},{task.description},{task.deadline.strftime('%Y-%m-%d')}\n")

    def view_completed_tasks(self):
        """
        Afișează toate sarcinile finalizate din lista de sarcini finalizate și din fișierul "completed.txt".
        """
        print("Completed tasks:")
        completed_tasks_btree = self.completed_tasks_btree
        completed_tasks_file = []

        # Citeste task-urile complete din fisierul "completed.txt"
        try:
            with open("completed.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    priority, description, deadline_str = map(str.strip, data)
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                    task = Task(int(priority), description, deadline)
                    completed_tasks_file.append(task)
        except FileNotFoundError:
            pass

        # Afișează task-urile din BTree și cele din fișier
        all_completed_tasks = completed_tasks_btree.root.keys + completed_tasks_file
        if not all_completed_tasks:
            print("No completed tasks.")
        else:
            sorted_completed_tasks = sorted(all_completed_tasks, key=lambda t: (t.priority, t.deadline))
            for task in sorted_completed_tasks:
                print(task.description)


def get_user_task():
    """
    Solicită utilizatorului datele pentru o nouă sarcină și returnează un obiect Task corespunzător.
    """
    print("Add a new task:")
    priority = int(input("Enter priority for the task (1 - highest, 10 - lowest): "))
    description = input("Enter task description: ")
    deadline_str = input("Enter task deadline (YYYY-MM-DD): ")
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
    return Task(priority, description, deadline)
