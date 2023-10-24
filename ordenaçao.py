import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk,filedialog
import time

class OrdenacaoApp:
    def __init__(self, root):
        self.data = []
        
        self.root = root
        self.root.title("App de Ordenação")
        self.root.geometry("400x650")  # Ajustei a altura novamente para acomodar as mudanças
        
        self.label = tk.Label(root, text="Insira números ou palavras")
        self.label.pack(pady=10)
        
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
        
        # Label para mostrar o tempo de ordenação
        self.timeLabel = tk.Label(root, text="", fg="red")
        self.timeLabel.pack(pady=10)

    def quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
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

    def refresh_listbox(self, items=None):
        self.listbox.delete(0, tk.END)
        for item in (items if items is not None else self.data):
            self.listbox.insert(tk.END, item)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenacaoApp(root)
    root.mainloop()