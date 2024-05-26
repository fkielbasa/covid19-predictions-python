import customtkinter
from CTkListbox import *
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import interp1d
import datetime

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()

root.title("Corona Rush")

root.iconbitmap("icon.ico")


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
    filename = f'data/CovidData{country}.json'
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

    # Interpolacja sześcienna dla wygładzenia danych
    interp_days = np.linspace(min(days), max(days), 500)  # Więcej punktów dla gładkości
    cubic_interp = interp1d(days, values, kind='cubic')
    smooth_values = cubic_interp(interp_days)

    fig, ax = plt.subplots(figsize=(10, 7))  # Zwiększamy rozmiar figury
    ax.plot(days, values, marker='o')

    # Dodajemy wykres liniowy wygładzony
    ax.plot(interp_days, smooth_values, label='Smooth Line Chart', color='red')

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
    if data:
        plot_data(data, right_frame, selected_country)
    else:
        show_waiting_message()

def load_countries():
    with open('data/Countries.json', 'r') as file:
        data = json.load(file)
    return data['countries']

def show_waiting_message():
    for widget in right_frame.winfo_children():
        widget.destroy()
    waiting_label = customtkinter.CTkLabel(right_frame, text="Waiting for data...", font=("Arial", 20))
    waiting_label.place(relx=0.5, rely=0.5, anchor="center")


# Obliczenie i ustawienie rozmiaru okna na podstawie rozmiaru ekranu
window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
root.geometry(f"{window_width}x{window_height}")
center_window(root, window_width, window_height)

# Prawy panel
right_frame = customtkinter.CTkFrame(root, width=800, height=window_height-100, border_width=5, border_color="#F9AA33")
right_frame.place(relx=0.62, rely=0.47, anchor="center")

# Początkowa wiadomość "Waiting for data..."
show_waiting_message()

# Lewy panel
left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
left_frame.place(relx=0.145, rely=0.33, anchor="center")

# Lista rozwijalna w ramce
listbox = CTkListbox(left_frame, command=on_country_selected, width=250, height=150)
listbox.pack(pady=10)

# Wczytaj listę krajów z pliku JSON i wypełnij listbox
countries = load_countries()
for i, country in enumerate(countries):
    listbox.insert(i, country)

# Pole do wpisania dat
date_label = customtkinter.CTkLabel(left_frame, text="Wprowadź trzy daty (DD-MM-YYYY):")
date_label.pack(pady=5)

# Ramka dla dat
date_frame = customtkinter.CTkFrame(left_frame)
date_frame.pack(pady=5)

# Pierwsza data
date_label1 = customtkinter.CTkLabel(date_frame, text="od:")
date_label1.grid(row=0, column=0, padx=5)
date_entry1 = customtkinter.CTkEntry(date_frame, width=150)
date_entry1.grid(row=0, column=1, padx=5)

# Druga data
date_label2 = customtkinter.CTkLabel(date_frame, text="do:")
date_label2.grid(row=1, column=0, padx=5)
date_entry2 = customtkinter.CTkEntry(date_frame, width=150)
date_entry2.grid(row=1, column=1, padx=5)

# Trzecia data
date_label3 = customtkinter.CTkLabel(date_frame, text="predykcja do:")
date_label3.grid(row=2, column=0, padx=5)
date_entry3 = customtkinter.CTkEntry(date_frame, width=150)
date_entry3.grid(row=2, column=1, padx=5)

# Przycisk do zatwierdzenia dat
submit_button = customtkinter.CTkButton(left_frame, text="Submit Dates", command=lambda: on_submit_dates([date_entry1.get(), date_entry2.get(), date_entry3.get()]))
submit_button.pack(pady=10)

def on_submit_dates(dates):
    try:
        # Konwersja dat na obiekt datetime
        date1 = datetime.datetime.strptime(dates[0], "%d-%m-%Y")
        date2 = datetime.datetime.strptime(dates[1], "%d-%m-%Y")
        date3 = datetime.datetime.strptime(dates[2], "%d-%m-%Y")

        # Sprawdzenie warunków
        if date2 <= date1 or (date2 - date1).days < 7:
            print("Druga data musi być co najmniej 7 dni późniejsza od pierwszej.")
            return
        if date3 <= date1 or date3 <= date2:
            print("Trzecia data musi być późniejsza niż pierwsza i druga.")
            return

        formatted_dates = [date1.strftime("%Y-%m-%d"), date2.strftime("%Y-%m-%d"), date3.strftime("%Y-%m-%d")]
        for date in formatted_dates:
            print(date)

        selected_country = listbox.get(listbox.curselection())
        data = load_data(selected_country)
        filtered_data = [entry for entry in data if entry['day'] in formatted_dates]
        if filtered_data:
            plot_data(filtered_data, right_frame, selected_country)
        else:
            show_waiting_message()

    except ValueError as e:
        print(f"Error parsing dates: {e}")

root.mainloop()
