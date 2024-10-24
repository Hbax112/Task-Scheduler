from datetime import datetime

class BTreeTaskCompleted:
    def __init__(self):
        """
        Inițializează o nouă instanță a clasei BTreeTaskCompleted.
        Atributul completed_tasks este o listă care va conține sarcinile completate.
        """
        self.completed_tasks = []

    def complete_task(self, task):
        """
        Marchează o sarcină ca fiind completată și adaugă la lista completed_tasks.
        - task: Sarcina de marcat ca fiind completată (o instanță a clasei Task).
        """
        timestamp = datetime.now()
        self.completed_tasks.append(task)

    def save_completed_tasks_to_file(self):
        """
        Salvează sarcinile completate într-un fișier "completed.txt".
        Sarcinile sunt sortate în funcție de prioritate înainte de salvare.
        """
        self.completed_tasks.sort(key=lambda x: x.priority)
        with open("completed.txt", "a") as file:
            for task in self.completed_tasks:
                file.write(f"{task.priority},{task.description},{task.deadline.strftime('%Y-%m-%d')}\n")
