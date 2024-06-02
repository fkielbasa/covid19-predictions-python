import datetime
import customtkinter
from CTkListbox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.prediction import nowy3
from data_management import load_countries, load_data
from plotting import plot_data
from window_utils import calculate_window_size, center_window

current_chart_index = 0
charts = []
data_for_charts = None

def main():
    global current_chart_index

    root = customtkinter.CTk()
    root.title("Corona Rush")
    root.iconbitmap("icon.ico")

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    def show_waiting_message():
        for widget in right_frame.winfo_children():
            widget.destroy()
        waiting_label = customtkinter.CTkLabel(right_frame, text="Waiting for data...", font=("Arial", 20))
        waiting_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_country_selected(events):
        global current_chart_index, charts
        selected_country = listbox.get(listbox.curselection())
        data = load_data(selected_country)
        future_date = '2025-05-20'
        charts = nowy3(data, future_date)
        if data:
            plot_data(data, right_frame, selected_country)
        else:
            show_waiting_message()

    def on_prev():
        global current_chart_index
        if current_chart_index > 0:
            current_chart_index -= 1

        for widget in right_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(charts[current_chart_index], master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def on_next():
        global current_chart_index
        if current_chart_index < len(charts) - 1:
            current_chart_index += 1

        for widget in right_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(charts[current_chart_index], master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def on_submit_dates(dates):
        try:
            date1 = datetime.datetime.strptime(dates[0], "%d-%m-%Y")
            date2 = datetime.datetime.strptime(dates[1], "%d-%m-%Y")
            date3 = datetime.datetime.strptime(dates[2], "%d-%m-%Y")

            if date2 <= date1 or (date2 - date1).days < 7:
                print("Druga data musi być co najmniej 7 dni późniejsza od pierwszej.")
                return
            if date3 <= date1 or date3 <= date2:
                print("Trzecia data musi być późniejsza niż pierwsza i druga.")
                return

            formatted_dates = [date1.strftime("%Y-%m-%d"), date2.strftime("%Y-%m-%d"), date3.strftime("%Y-%m-%d")]

            selected_country = listbox.get(listbox.curselection())
            data = load_data(selected_country)
            filtered_data = [entry for entry in data if entry['day'] in formatted_dates]
            if filtered_data:
                plot_data(filtered_data, right_frame, selected_country)
            else:
                show_waiting_message()

        except ValueError as e:
            print(f"Error parsing dates: {e}")

    window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
    root.geometry(f"{window_width}x{window_height}")
    center_window(root, window_width, window_height)

    right_frame = customtkinter.CTkFrame(root, width=800, height=window_height-100, border_width=5, border_color="#F9AA33")
    right_frame.place(relx=0.62, rely=0.47, anchor="center")

    show_waiting_message()

    left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
    left_frame.place(relx=0.145, rely=0.33, anchor="center")

    listbox = CTkListbox(left_frame, command=on_country_selected, width=250, height=150)
    listbox.pack(pady=10)

    countries = load_countries()
    for i, country in enumerate(countries):
        listbox.insert(i, country)

    date_label = customtkinter.CTkLabel(left_frame, text="Wprowadź trzy daty (DD-MM-YYYY):")
    date_label.pack(pady=5)

    date_frame = customtkinter.CTkFrame(left_frame)
    date_frame.pack(pady=5)

    date_label1 = customtkinter.CTkLabel(date_frame, text="od:")
    date_label1.grid(row=0, column=0, padx=5)
    date_entry1 = customtkinter.CTkEntry(date_frame, width=150)
    date_entry1.grid(row=0, column=1, padx=5)

    date_label2 = customtkinter.CTkLabel(date_frame, text="do:")
    date_label2.grid(row=1, column=0, padx=5)
    date_entry2 = customtkinter.CTkEntry(date_frame, width=150)
    date_entry2.grid(row=1, column=1, padx=5)

    date_label3 = customtkinter.CTkLabel(date_frame, text="predykcja do:")
    date_label3.grid(row=2, column=0, padx=5)
    date_entry3 = customtkinter.CTkEntry(date_frame, width=150)
    date_entry3.grid(row=2, column=1, padx=5)

    submit_button = customtkinter.CTkButton(left_frame, text="Submit Dates", command=lambda: on_submit_dates([date_entry1.get(), date_entry2.get(), date_entry3.get()]))
    submit_button.pack(pady=10)

    navigation_frame = customtkinter.CTkFrame(left_frame)
    navigation_frame.pack(pady=20)

    prev_button = customtkinter.CTkButton(navigation_frame, text="Poprzedni", command=on_prev)
    prev_button.pack(side="left", padx=10)

    next_button = customtkinter.CTkButton(navigation_frame, text="Następny", command=on_next)
    next_button.pack(side="right", padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()
