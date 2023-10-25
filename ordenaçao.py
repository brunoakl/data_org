import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import time, random, string

class OrdenacaoApp:
    def __init__(self, root):
        self.data = []
        
        self.root = root
        self.root.title("App de Ordenação")
        self.root.geometry("400x320")  # Ajustei a altura novamente para acomodar as mudanças
        
        self.label = tk.Label(root, text="Insira números ou palavras")
        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.entry = tk.Entry(root)
        self.entry.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.entry.bind("<Return>", self.add_item)    
        
        self.addButton = tk.Button(root, text="Adicionar", command=self.add_item)
        self.addButton.grid(row=2, column=0, pady=10, padx=10, sticky="w")        
        # Combobox para seleção de método de ordenação
        self.comboBox = ttk.Combobox(root, values=["QuickSort", "MergeSort"], state="readonly")
        self.comboBox.set("QuickSort")  # Método padrão
        self.comboBox.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        
        # Frame para botões
        self.buttonFrame = tk.Frame(root)
        self.buttonFrame.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        
        self.sortButton = tk.Button(self.buttonFrame, text="Ordenar", command=self.sort_items)
        self.sortButton.grid(row=0, column=0, padx=5)        
        self.clearButton = tk.Button(self.buttonFrame, text="Limpar", command=self.clear_vector)
        self.clearButton.grid(row=0, column=1, padx=4)
        
        
        self.saveButton = tk.Button(self.buttonFrame, text="Salvar", command=self.save_items)
        self.saveButton.grid(row=0, column=2, padx=5)
        
        self.exportButton = tk.Button(self.buttonFrame, text="importar", command=self.import_items)
        self.exportButton.grid(row=1, column=0, padx=5)
        self.searchLabel = tk.Label(root, text="Pesquisar")
        self.searchLabel.grid(row=0, column=1, padx=5)
        
        self.searchEntry = tk.Entry(root)
        self.searchEntry.bind("<Return>", self.filter_items)
        self.searchEntry.grid(row=1, column=1, padx=3)
        
        self.listbox = tk.Listbox(root)
        self.listbox.grid(row=2, column=1, rowspan=5, pady=20, padx=4)
        
        
        # Label para mostrar o tempo de ordenação
        self.timeLabel = tk.Label(root, text="", fg="red")
        self.timeLabel.grid(row=8, column=0, pady=10, padx=10, sticky="w")

        self.generateRandomButton = tk.Button(self.buttonFrame, text="Gerar Aleatório", command=self.generate_random_window)
        self.generateRandomButton.grid(row=1, column=1, padx=5)
        
        # Redimensionar colunas e linhas conforme necessário
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(7, weight=1)
        
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
    
    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if self.custom_compare(x, pivot)]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if self.custom_compare(pivot, x)]
        return self.quick_sort(left) + middle + self.quick_sort(right)

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
            if self.custom_compare(left[left_index], right[right_index]):
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
        
    def generate_random_window(self):
        self.random_window = tk.Toplevel(self.root)
        self.random_window.title("Gerar Itens Aleatórios")
        
        self.label = tk.Label(self.random_window, text="Insira a quantidade de itens:")
        self.label.pack(pady=10)
        
        self.random_entry = tk.Entry(self.random_window)
        self.random_entry.pack(pady=10)
        
        self.generateButton = tk.Button(self.random_window, text="Gerar", command=self.generate_random_items)
        self.generateButton.pack(pady=10)
    
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

    def refresh_listbox(self, items=None):
        self.listbox.delete(0, tk.END)
        for item in (items if items is not None else self.data):
            self.listbox.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenacaoApp(root)

    root.mainloop()
