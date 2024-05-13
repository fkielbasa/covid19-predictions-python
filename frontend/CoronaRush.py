import tkinter as tk

def calculate_window_size(screen_width, screen_height):
    # screen_width = 1700
    # screen_height = 900
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

def country_selected(selected_country):
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

# Tytuł aplikacji
# label = tk.Label(left_frame, text="Corona Rush", font=("Arial", 25, "bold"), fg="white", bg=background_color)
# label.place(relx=0.5, rely=0.06, anchor=tk.CENTER)

# Opis selectora
# label = tk.Label(left_frame, text="Wybierz państwo", font=("Arial", 13), fg="white", bg=background_color)
# label.place(relx=0.14, rely=0.15)

# Selektor
countries = ["Polska", "Anglia", "Niemcy", "Rosja"]
selected_country = tk.StringVar(left_frame)
selected_country.set(countries[0])  # Ustawienie domyślnego wyboru
country_menu = tk.OptionMenu(left_frame, selected_country, *countries, command=country_selected)
country_menu.config(width=40)
country_menu.place(relx=0.5, rely=0.07, anchor=tk.CENTER)

# Separator
canvas = tk.Canvas(root, width=8, height=window_height, bg=orange_color, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.Y)

# Prawy panel
right_frame = tk.Frame(root, bg=background_color, width=window_width-301, height=window_height)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Opis wykresu
label = tk.Label(right_frame, text="Wykres", font=("Arial", 14), fg="white", bg=background_color)
label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

# Ramka dla wykresu
chart_frame = tk.Frame(right_frame, bg=chart_color, width=window_width-501, height=window_height-150, highlightthickness=5, highlightbackground=orange_color)
chart_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()