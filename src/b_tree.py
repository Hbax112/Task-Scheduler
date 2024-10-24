class BTreeNode:
    def __init__(self, keys=None, children=None):
        """
        Inițializează un nod într-un arbore B cu cheile specificate și copiii asociați.
        - keys: Lista de chei stocate în nod.
        - children: Lista de copii ai nodului.
        """
        self.keys = keys or []
        self.children = children or []

    def is_leaf(self):
        """
        Verifică dacă nodul este frunză (nu are copii).
        """
        return len(self.children) == 0

class BTree:
    def __init__(self, t):
        """
        Inițializează un arbore B cu gradul specificat.
        - t: Gradul arborelui B, determinând numărul minim de chei într-un nod (t - 1).
        """
        self.root = BTreeNode()
        self.t = t

    def insert(self, task):
        """
        Inserează o cheie (o nouă sarcină) în arborele B.
        - task: Cheia (sarcina) ce urmează să fie inserată.
        """
        root = self.root

        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, task)

    def _insert_non_full(self, x, task):
        """
        Inserează o cheie într-un nod care nu este plin.
        - x: Nodul în care se realizează inserarea.
        - task: Cheia (sarcina) ce urmează să fie inserată.
        """
        i = len(x.keys) - 1

        if x.is_leaf():
            x.keys.append(task)
            x.keys.sort(key=lambda t: (t.priority, t.deadline))
        else:
            while i >= 0 and task.priority < x.keys[i].priority:
                i -= 1

            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if task.priority > x.keys[i].priority:
                    i += 1

            self._insert_non_full(x.children[i], task)

    def _split_child(self, x, i):
        """
        Realizează despărțirea unui copil al unui nod în două.
        - x: Nodul părinte.
        - i: Indexul copilului ce urmează să fie divizat.
        """
        t = self.t
        y = x.children[i]
        z = BTreeNode()
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.is_leaf():
            z.children = y.children[t:]
            y.children = y.children[:t]

    def save_completed_tasks_to_file(self, node=None):
        """
        Salvează cheile complete în fișierul "completed.txt".
        - node: Nodul de la care începe salvarea (implicit, rădăcina arborelui).
        """
        node = node or self.root
        if node.is_leaf():
            with open("completed.txt", "a") as file:
                for key in node.keys:
                    file.write(f"{key.priority},{key.description},{key.deadline.strftime('%Y-%m-%d')}\n")
        else:
            for i, child in enumerate(node.children):
                self.save_completed_tasks_to_file(child)
                if i < len(node.keys):
                    with open("completed.txt", "a") as file:
                        file.write(f"{node.keys[i].priority},{node.keys[i].description},{node.keys[i].deadline.strftime('%Y-%m-%d')}\n")

    def display(self, node=None, level=0):
        """
        Afișează structura arborelui în mod recursiv.
        - node: Nodul de la care începe afișarea (implicit, rădăcina arborelui).
        - level: Nivelul la care se află nodul în arbore.
        """
        node = node or self.root
        print("Level", level, ":", " ".join([str(key.priority) for key in node.keys]))
        if not node.is_leaf():
            for child in node.children:
                self.display(child, level + 1)

    def display_completed_tasks(self, node=None, level=0):
        """
        Afișează cheile complete în mod recursiv.
        - node: Nodul de la care începe afișarea (implicit, rădăcina arborelui).
        - level: Nivelul la care se află nodul în arbore.
        """
        node = node or self.root
        if not node.is_leaf():
            for i, child in enumerate(node.children):
                self.display_completed_tasks(child, level + 1)
                if i < len(node.keys):
                    print(f"Level {level}: {node.keys[i]}")
        else:
            for key in node.keys:
                print(f"Level {level}: {key}")

    def view_completed_tasks(self):
        """
        Afișează cheile complete în arborele B.
        """
        print("Completed tasks:")
        self.display_completed_tasks()
