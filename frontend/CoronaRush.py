import customtkinter
from CTkListbox import *

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

def country_selected(event):
    selected_country = menu.get()
    print("Wybrano", selected_country)

root = customtkinter.CTk()

# Obliczenie i ustawienie rozmiaru okna na podstawie rozmiaru ekranu
window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
root.geometry(f"{window_width}x{window_height}")
center_window(root, window_width, window_height)

root.title("Corona Rush")

def show_value(selected_option):
    print(selected_option)

# Lewy panel
left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
left_frame.place(relx=0.12, rely=0.17, anchor="center")

# Lista rozwijalna w ramce
listbox = CTkListbox(left_frame, command=show_value, width=200, height=150)
listbox.pack(fill="both", expand=True)

listbox.insert(0, "Poland")
listbox.insert(1, "Spain")
listbox.insert(2, "France")
listbox.insert(3, "Canada")
listbox.insert(4, "Slovakia")
listbox.insert(5, "Russia")
listbox.insert("END", "Ukraine")

#Prawy panel
right_frame = customtkinter.CTkFrame(root, width=800, height=window_height-100, border_width=5, border_color="#F9AA33")
right_frame.place(relx=0.6, rely=0.47, anchor="center")

root.mainloop()
