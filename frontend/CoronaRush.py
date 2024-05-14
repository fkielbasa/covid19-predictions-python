import tkinter as tk
from tkinter import ttk

def calculate_window_size(screen_width, screen_height):
    screen_height = 720
    screen_width = 1280

    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    return window_width, window_height

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def country_selected(event):
    selected_country = menu.get()
    print("Wybrano", selected_country)


root = tk.Tk()
root.title("Corona Rush")

window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
center_window(root, window_width, window_height)

# Kolory
background_color = "#344955"
chart_color = "#4a6572"
orange_color = "#f9aa33"

# Lewy panel
left_frame = tk.Frame(root, bg=background_color, width=350, height=window_height)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Selektor
countries = ["Polska", "Anglia", "Niemcy", "Rosja"]
selected_country = tk.StringVar(left_frame)
selected_country.set(countries[0])  # Ustawienie domyślnego wyboru

# Combobox o szerokości 40
menu = ttk.Combobox(left_frame, textvariable=selected_country, values=countries, width=40)
menu.place(relx=0.5, rely=0.07, anchor=tk.CENTER)
menu.bind("<<ComboboxSelected>>", country_selected)

# Prawy panel
right_frame = tk.Frame(root, bg=background_color, width=window_width-300, height=window_height)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Wymiary wykresu
chart_width = 600
chart_height = 500

# Współrzędne wykresu
chart_x = (window_width - chart_width) / 2
chart_y = (window_height - chart_height) / 2

# Ramka dla wykresu
chart_frame = tk.Frame(right_frame, bg=chart_color, width=chart_width, height=chart_height)
chart_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
