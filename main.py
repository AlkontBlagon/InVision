import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from detal import run_paser 


def get_data(name):
    # Пример данных, которые могут зависеть от имени пользователя
    data = run_paser(name) 
    # Здесь можно добавить логику для изменения данных в зависимости от имени пользователя
    return data

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.selected_platform_data = None
        self.graph_type = "graph"  # Инициализация атрибута graph_type
        self.title("Data Visualization")
        self.geometry("800x600")

        self.name_label = tk.Label(self, text="Введите имя:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.get_data_button = tk.Button(self, text="Получить данные", command=self.load_data)
        self.get_data_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.platform_label = tk.Label(self, text="Выберите платформу:")
        self.platform_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        self.graph_type_label = tk.Label(self, text="Выберите тип отображения:")
        self.graph_type_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.graph_type_frame = tk.Frame(self)
        self.graph_type_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        self.graph_button = tk.Button(self.graph_type_frame, text="Графики", command=lambda: self.update_graph_type("graph"))
        self.graph_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.text_button = tk.Button(self.graph_type_frame, text="Текст", command=lambda: self.update_graph_type("text"))
        self.text_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.text_area = tk.Text(self, height=10)
        self.text_area.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.text_area.grid_remove()  # Скрыть текстовое поле по умолчанию

        self.figure, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 12))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def load_data(self):
        name = self.name_entry.get()
        self.data = get_data(name)
        self.get_data()
        # Отображение первой платформы и графиков по умолчанию
        self.select_platform(self.data[0])
        self.update_graph_type("graph")

    def get_data(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for i, d in enumerate(self.data):
            button = tk.Button(self.button_frame, text=d['platform'], command=lambda d=d: self.select_platform(d))
            button.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        compare_button = tk.Button(self.button_frame, text="Сравнить все", command=self.compare_all)
        compare_button.grid(row=0, column=len(self.data), padx=5, pady=5, sticky="ew")

    def select_platform(self, platform_data):
        self.selected_platform_data = platform_data
        self.update_graph()

    def update_graph_type(self, graph_type):
        self.graph_type = graph_type
        self.update_graph()

    def update_graph(self):
        if self.graph_type == "text":
            self.text_area.grid()
            self.canvas.get_tk_widget().grid_remove()
            self.show_text()
        else:
            self.text_area.grid_remove()
            self.canvas.get_tk_widget().grid()
            if self.selected_platform_data:
                self.ax1.cla()  # Очистка текущей фигуры
                self.ax2.cla()
                self.ax3.cla()
                self.ax1.plot(self.selected_platform_data['views'], label='Линейный график')
                self.ax2.bar(range(len(self.selected_platform_data['views'])), self.selected_platform_data['views'], alpha=0.5, label='Столбчатый график')
                self.ax3.pie(self.selected_platform_data['views'], labels=range(len(self.selected_platform_data['views'])), autopct='%1.1f%%')
                self.ax1.set_title(f"Views for {self.selected_platform_data['platform']}")
                self.ax1.legend()
                self.ax2.legend()
                self.canvas.draw()

    def compare_all(self):
        self.ax1.cla()  # Очистка текущей фигуры
        self.ax2.cla()
        self.ax3.cla()
        if self.graph_type == "text":
            self.show_text()
        else:
            for d in self.data:
                self.ax1.plot(d['views'], label=f"{d['platform']} - Линейный график")
                self.ax2.bar(range(len(d['views'])), d['views'], alpha=0.5, label=f"{d['platform']} - Столбчатый график")
            total_views = [sum(d['views']) for d in self.data]
            platforms = [d['platform'] for d in self.data]
            self.ax3.pie(total_views, labels=platforms, autopct='%1.1f%%')
            self.ax1.set_title("Comparison of Views Across Platforms")
            self.ax1.legend()
            self.ax2.legend()
            self.canvas.draw()

    def show_text(self):
        self.text_area.delete(1.0, tk.END)
        if self.selected_platform_data:
            self.text_area.insert(tk.END, f"Platform: {self.selected_platform_data['platform']}\nSubscribers: {self.selected_platform_data['subscrube']}\nViews: {self.selected_platform_data['views']}\n\n")
        else:
            for d in self.data:
                self.text_area.insert(tk.END, f"Platform: {d['platform']}\nSubscribers: {d['subscrube']}\nViews: {d['views']}\n\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
