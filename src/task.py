from datetime import datetime

class Task:
    def __init__(self, priority, description, deadline):
        """
        Inițializează o nouă instanță a clasei Task.
        - priority: Prioritatea sarcinii (un număr întreg).
        - description: Descrierea sarcinii (un șir de caractere).
        - deadline: Termenul limită al sarcinii (un obiect datetime.date).
        """
        self.priority = priority
        self.description = description
        self.deadline = deadline

    def __str__(self):
        """
        Returnează o reprezentare sub formă de șir a instanței Task.
        """
        return f"Priority: {self.priority}, Description: {self.description}, Deadline: {self.deadline}"
