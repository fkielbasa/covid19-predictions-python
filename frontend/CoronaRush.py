import customtkinter
from CTkListbox import *
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

def calculate_window_size(screen_width, screen_height):
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    return window_width, window_height

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def load_data(country):
    filename = f'CovidData{country}.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data['data']
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []

def plot_data(data, frame, country):
    days = [entry['day'] for entry in data]
    values = [entry['value'] for entry in data]

    fig, ax = plt.subplots(figsize=(10, 7))  # Zwiększamy rozmiar figury
    ax.plot(days, values, marker='o')

    ax.set(xlabel='Day', ylabel='Value', title=f'Covid Data for {country}')
    ax.grid()

    ax.title.set_size(20)  # Zwiększamy rozmiar tytułu
    ax.xaxis.label.set_size(14)  # Zwiększamy rozmiar etykiety osi X
    ax.yaxis.label.set_size(14)  # Zwiększamy rozmiar etykiety osi Y
    ax.tick_params(axis='both', which='major', labelsize=12)  # Zwiększamy rozmiar etykiet ticków

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def on_country_selected(event):
    selected_country = listbox.get(listbox.curselection())
    data = load_data(selected_country)
    plot_data(data, right_frame, selected_country)

def load_countries():
    with open('countries.json', 'r') as file:
        data = json.load(file)
    return data['countries']

root = customtkinter.CTk()

# Obliczenie i ustawienie rozmiaru okna na podstawie rozmiaru ekranu
window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
root.geometry(f"{window_width}x{window_height}")
center_window(root, window_width, window_height)

root.title("Corona Rush")

# Lewy panel
left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
left_frame.place(relx=0.12, rely=0.17, anchor="center")

# Lista rozwijalna w ramce
listbox = CTkListbox(left_frame, command=on_country_selected, width=200, height=150)
listbox.pack(fill="both", expand=True)

# Wczytaj listę krajów z pliku JSON i wypełnij listbox
countries = load_countries()
for i, country in enumerate(countries):
    listbox.insert(i, country)

# Prawy panel
right_frame = customtkinter.CTkFrame(root, width=800, height=window_height-100, border_width=5, border_color="#F9AA33")
right_frame.place(relx=0.62, rely=0.47, anchor="center")

root.mainloop()
