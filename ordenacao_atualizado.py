import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk,filedialog
import time, random, string
import networkx as nx
import matplotlib.pyplot as plt

# Função para criar e visualizar o grafo com Network
def visualize_graph(data):
    # Cria um grafo direcionado com NetworkX
    G = nx.DiGraph()
    
    # Adiciona os nós com os dados inseridos
    for item in data:
        G.add_node(item)

    # Adiciona arestas sequenciais para representar a ordem dos dados inseridos
    for i in range(len(data) - 1):
        G.add_edge(data[i], data[i + 1])

    # Desenha o grafo com layout circular e mostra a visualização
    nx.draw_circular(G, with_labels=True, font_weight='bold')
    plt.show()

# Classe Hashtable para organizar os dados
class Hashtable:
    def __init__(self, size=256):
        self.size = size
        self.hashmap = [[] for _ in range(self.size)]

    def count_frequency(self):
        frequency = {}
        for bucket in self.hashmap:
            for key, value in bucket:
                if key in frequency:
                    frequency[key] += value
                else:
                    frequency[key] = 1  # Comece a contagem com 1 se o item ainda não estiver no dicionário
        return frequency
    
    def get_unique_items(self):
        unique_items = []
        for item in self.hashmap:
            for key, _ in item:
                unique_items.append(key)
        return unique_items
        
    def hash_func(self, key):
        hashed_key = hash(key) % self.size
        return hashed_key
        
    def insert(self, key, value):
        hash_key = self.hash_func(key)
        key_exists = False
        bucket = self.hashmap[hash_key]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                bucket[i] = (key, value)  # Atualize o valor aqui, não concatene
                break
        if not key_exists:
            bucket.append((key, value))
            
    def retrieve(self, key):
        hash_key = self.hash_func(key)
        bucket = self.hashmap[hash_key]
        for k, v in bucket:
            if k == key:
                return v
        return None

class OrdenacaoApp:
    def __init__(self, root):
        self.data = []
        self.hashtable = Hashtable()
        
        
        self.root = root
        self.root.title("App de Ordenação")
        self.root.geometry("400x650")  # Ajustei a altura novamente para acomodar as mudanças
        
        self.visualizeButton = tk.Button(self.root, text="Visualizar Grafo", command=self.visualize)
        self.visualizeButton.pack()

        self.label = tk.Label(root, text="Insira números ou palavras")
        self.label.pack(pady=10)
        # Botão para contar frequência dos itens
        self.countFreqButton = tk.Button(root, text="Contar Frequência", command=self.count_frequency)
        self.countFreqButton.pack()
        
        # Checkbox para adicionar apenas itens únicos
        self.uniqueItemsVar = tk.BooleanVar()
        self.uniqueItemsCheckbutton = tk.Checkbutton(root, text="Apenas Itens Únicos", variable=self.uniqueItemsVar)
        self.uniqueItemsCheckbutton.pack()

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.add_item)  
        
        self.addButton = tk.Button(root, text="Adicionar", command=self.add_item)
        self.addButton.pack(pady=10)
        
        # Combobox para seleção de método de ordenação
        self.comboBox = ttk.Combobox(root, values=["QuickSort", "MergeSort"], state="readonly")
        self.comboBox.set("QuickSort")  # Método padrão
        self.comboBox.pack(pady=10)
        
        # Frame para botões
        self.buttonFrame = tk.Frame(root)
        self.buttonFrame.pack(pady=10)
        
        self.sortButton = tk.Button(self.buttonFrame, text="Ordenar", command=self.sort_items)
        self.sortButton.pack(side=tk.LEFT, padx=5)
        
        self.clearButton = tk.Button(self.buttonFrame, text="Limpar", command=self.clear_vector)
        self.clearButton.pack(side=tk.LEFT, padx=5)
        
        self.saveButton = tk.Button(self.buttonFrame, text="Salvar", command=self.save_items)
        self.saveButton.pack(side=tk.LEFT, padx=5)
        
        self.exportButton = tk.Button(self.buttonFrame, text="importar", command=self.import_items)
        self.exportButton.pack(side=tk.LEFT, padx=5)

        self.searchLabel = tk.Label(root, text="Pesquisar")
        self.searchLabel.pack(pady=10)
        
        self.searchEntry = tk.Entry(root)
        self.searchEntry.pack(pady=10)
        self.searchEntry.bind("<Return>", self.filter_items)
        
        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=20, padx=20, expand=True, fill="both")
        
        self.generateRandomButton = tk.Button(self.buttonFrame, text="Gerar Aleatório", command=self.generate_random_window)
        self.generateRandomButton.pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar o tempo de ordenação
        self.timeLabel = tk.Label(root, text="", fg="red")
        self.timeLabel.pack(pady=10)

    def count_frequency(self):
        hashtable = Hashtable()
        for item in self.data:
            current_count = hashtable.retrieve(item)
            if current_count is None:  # Se o item não estiver na hashtable ainda
                hashtable.insert(item, 1)
            else:
                hashtable.insert(item, current_count + 1)  # Incrementar a contagem
        frequency = hashtable.count_frequency()
        # Agora você pode mostrar a frequência dos itens como desejar, por exemplo, em um messagebox ou atualizando a interface do usuário
        messagebox.showinfo("Frequência de Itens", '\n'.join(f"{item}: {count}" for item, count in frequency.items()))
    
    def add_item(self, event=None):
        item = self.entry.get()
        if not item:
            return

        # Insira ou atualize a contagem na hashtable ao adicionar um item
        current_count = self.hashtable.retrieve(item) or 0
        self.hashtable.insert(item, current_count + 1)

        # Adicione o item à lista de dados e atualize a exibição
        self.data.append(item)
        self.entry.delete(0, tk.END)
        self.refresh_listbox()

    def display_frequency(self):
        # Computar e exibir a frequência dos itens usando a hashtable existente
        frequency = self.hashtable.count_frequency()
        messagebox.showinfo("Frequência dos Itens", "\n".join(f"{item}: {freq}" for item, freq in frequency.items()))

    def timer(self):
        start_time = time.time()

        if self.comboBox.get() == "QuickSort":
            self.data = self.quick_sort(self.data)
        else:  # MergeSort
            self.data = self.merge_sort(self.data)

        elapsed_time = time.time() - start_time
        self.timeLabel.config(text=f"Tempo: {elapsed_time:.6f} segundos")
        
        self.refresh_listbox()

    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)
    def visualize(self):
        visualize_graph(self.data)
    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        return self.merge(self.merge_sort(left), self.merge_sort(right))

    def merge(self, left, right):
        result = []
        left_index, right_index = 0, 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

        result += left[left_index:]
        result += right[right_index:]

        return result

    def sort_items(self):
        start_time = time.time()

        if self.comboBox.get() == "QuickSort":
            self.data = self.quick_sort(self.data)
        else:  # MergeSort
            self.data = self.merge_sort(self.data)

        elapsed_time = time.time() - start_time
        self.timeLabel.config(text=f"Tempo: {elapsed_time:.6f} segundos")
        
        self.refresh_listbox()
    def add_item(self, event=None):  
        item = self.entry.get()
        if not item:
            return
        
        if item.isnumeric() or item.replace(".", "", 1).isdigit():  
            self.data.append(float(item))
        else:
            self.data.append(item)
        
        self.entry.delete(0, tk.END)  
        self.refresh_listbox()
        
    def sort_items(self):
        self.data.sort(key=lambda x: (isinstance(x, str), x))
        self.refresh_listbox()
    
    def filter_items(self, event=None):
        query = self.searchEntry.get().lower()
        filtered_data = [item for item in self.data if query in str(item).lower()]
        self.refresh_listbox(filtered_data)
    
    def clear_vector(self):
        self.data.clear()
        self.refresh_listbox()

    def save_items(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        with open(file_path, 'w') as f:
            for item in self.data:
                f.write(f"{item}\n")

    def import_items(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        with open(file_path, 'r') as f:
            lines = f.readlines()
            self.data = [float(line.strip()) if line.strip().replace(".", "", 1).isdigit() else line.strip() for line in lines]

        self.refresh_listbox()

    def generate_random_window(self):
        self.random_window = tk.Toplevel(self.root)
        self.random_window.title("Gerar Itens Aleatórios")
        
        self.label = tk.Label(self.random_window, text="Insira a quantidade de itens:")
        self.label.pack(pady=10)
        
        self.random_entry = tk.Entry(self.random_window)
        self.random_entry.pack(pady=10)
        
        self.generateButton = tk.Button(self.random_window, text="Gerar", command=self.generate_random_items)
        self.generateButton.pack(pady=10)
    
    def refresh_listbox(self, items=None):
        self.listbox.delete(0, tk.END)
        for item in (items if items is not None else self.data):
            self.listbox.insert(tk.END, item)
            
    def generate_random_items(self):
        try:
            count = int(self.random_entry.get())
            
            choices = ["word", "number"]
            choice = random.choice(choices)
            
            if choice == "word":
                self.data.extend(self.generate_random_words(count))
            else:
                self.data.extend(self.generate_random_numbers(count))
            
            self.random_window.destroy()
            self.refresh_listbox()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def generate_random_words(self, count):
        return [''.join(random.choice(string.ascii_lowercase) for _ in range(5)) for _ in range(count)]

    def generate_random_numbers(self, count):
        return [random.randint(1, 1000) for _ in range(count)]

    def custom_compare(self, x, y):
        if isinstance(x, str) and isinstance(y, str):
            return x < y
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            return x < y
        else:
            return isinstance(x, str)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenacaoApp(root)
    root.mainloop()