import tkinter as tk

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

root = tk.Tk()
root.title("CoronaRush")

# Obliczanie wielkości okna na podstawie 80% powierzchni ekranu
window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())

# Ustawianie wielkości okna na środku ekranu
center_window(root, window_width, window_height)

root.mainloop()
