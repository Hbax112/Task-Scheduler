class BinomialTreeNode:
    def __init__(self, key):
        """
        Inițializează un nod în arborele binomial cu o cheie specificată.
        - key: Cheia asociată nodului, în acest context, reprezentând o sarcină.
        """
        self.key = key
        self.degree = 0
        self.children = []
        self.parent = None

class BinomialHeap:
    def __init__(self, head=None):
        """
        Inițializează un heap binomial cu o listă de arbori binomiali opțională.
        - head: Lista de arbori binomiali reprezentând structura heap-ului.
        """
        if head is None:
            self.head = []
        else:
            self.head = head

    def merge(self, other_heap):
        """
        Îmbină heap-ul binomial curent cu un alt heap binomial.
        - other_heap: Alt heap binomial cu care se face îmbinarea.
        """
        self.head.extend(other_heap.head)
        self.head.sort(key=lambda tree: tree.degree)
        self._consolidate()

    def _consolidate(self):
        """
        Consolidează heap-ul binomial prin combinarea arborilor cu aceleași grade.
        """
        if not self.head:
            return

        new_head = []
        max_degree = max(tree.degree for tree in self.head) + 1
        degree_table = [None] * max_degree

        for tree in self.head:
            while degree_table[tree.degree]:
                other_tree = degree_table[tree.degree]
                if (tree.key.priority, tree.key.deadline) < (other_tree.key.priority, other_tree.key.deadline):
                    tree, other_tree = other_tree, tree
                self._link(tree, other_tree)
                degree_table[tree.degree - 1] = None

            degree_table[tree.degree] = tree

        self.head = [tree for tree in degree_table if tree]

    def _link(self, tree1, tree2):
        """
        Realizează legătura între doi arbori binomiali.
        - tree1: Primul arbore binomial.
        - tree2: Al doilea arbore binomial.
        """
        tree1.parent = tree2
        tree1.sibling = tree2.children
        tree2.children = tree1
        tree2.degree += 1

    def insert(self, key):
        """
        Inserează o cheie (o nouă sarcină) în heap-ul binomial.
        - key: Cheia (sarcina) ce urmează să fie inserată.
        """
        new_tree = BinomialTreeNode(key)
        new_heap = BinomialHeap(head=[new_tree])
        self.merge(new_heap)

    def extract_min(self):
        """
        Extrage cheia minimă (cea cu cea mai mare prioritate) din binomial heap.
        """
        if not self.head:
            return None

        min_tree = min(self.head, key=lambda tree: tree.key)
        self.head.remove(min_tree)

        children_heap = BinomialHeap(head=min_tree.children)
        self.merge(children_heap)

        return min_tree.key
