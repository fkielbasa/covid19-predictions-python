import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Corona Rush")
root.geometry("1200x800")

# Ramka dla selektora państw
country_frame = ttk.Frame(root, padding="10")
country_frame.grid(row=0, column=0, sticky="nsew")

# Ramka dla miejsca na wykres
chart_frame = ttk.Frame(root, padding="10")
chart_frame.grid(row=0, column=1, sticky="nsew")

# Ustawienie koloru tła ramki dla miejsca na wykres
chart_frame_style = ttk.Style()
chart_frame_style.configure("Chart.TFrame", background="lightblue")
chart_frame.configure(style="Chart.TFrame")

# Label
label = ttk.Label(country_frame, text="Corona Rush", font=("Helvetica", 16))
label.grid(row=0, column=0, pady=10)

# Selektor państw
countries = ["Polska", "Anglia", "Niemcy", "Rosja"]
country_var = tk.StringVar()
country_var.set(countries[0])  # Ustawiamy domyślnie pierwsze państwo

country_label = ttk.Label(country_frame, text="Wybierz państwo:")
country_label.grid(row=1, column=0, pady=(10, 5))

country_selector = ttk.OptionMenu(country_frame, country_var, *countries)
country_selector.grid(row=2, column=0, padx=10)

root.mainloop()
