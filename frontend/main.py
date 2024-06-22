import datetime
import json
import customtkinter
from CTkListbox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry

from backend.prediction import nowy3
from backend.DataManagement import load_countries, load_data
from plotting import plot_country_chart
from window_utils import calculate_window_size, center_window

current_chart_index = 0
charts = []
data_for_charts = None
manual_entry_result = None
search_query = ""


def search_country_in_file(country_name):
    try:
        with open("data/Countries.json", "r", encoding="utf-8") as f:
            countries_data = json.load(f)
            return country_name.lower() in [country.lower() for country in countries_data["countries"]]
    except FileNotFoundError:
        return False

def main():
    global current_chart_index, manual_entry_result, search_query

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


    def show_current_chart():
        for widget in right_frame.winfo_children():
            widget.destroy()

        if charts:
            charts[current_chart_index].set_size_inches(9, 7)

            canvas = FigureCanvasTkAgg(charts[current_chart_index], master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
        else:
            show_waiting_message()

    def on_prev():
        global current_chart_index
        if current_chart_index > 0:
            current_chart_index -= 1
        show_current_chart()

    def on_next():
        global current_chart_index
        if current_chart_index < len(charts) - 1:
            current_chart_index += 1
        show_current_chart()

    def on_submit_dates(dates):
        try:
            date1 = datetime.datetime.strptime(dates[0], "%d-%m-%Y")
            date2 = datetime.datetime.strptime(dates[1], "%d-%m-%Y")
            date3 = datetime.datetime.strptime(dates[2], "%d-%m-%Y")

            if date2 <= date1 or (date2 - date1).days < 89:
                log_message("The second date must be at least 3 months later than the first.")
                return
            if date3 <= date1 or date3 <= date2:
                log_message("The third date must be later than the second and first.")
                return
            global current_chart_index, charts

            if manual_entry_result:
                selected_country = search_query
            else:
                selected_country = listbox.get(listbox.curselection())
            log_message(f"Selected country: {selected_country}")
            data = load_data(selected_country)

            if not data:
                log_message(f"No data found for {selected_country}")
                return

            data_date1_to_date2 = [entry for entry in data if
                                   'day' in entry and date1.strftime("%Y-%m-%d") <= entry['day'] <= date2.strftime(
                                       "%Y-%m-%d")]

            data_date1_to_date3 = [entry for entry in data if
                                   'day' in entry and date1.strftime("%Y-%m-%d") <= entry['day'] <= date3.strftime(
                                       "%Y-%m-%d")]

            for entry in data_date1_to_date2:
                log_message(str(entry))

            if data_date1_to_date3:
                plot_country_chart(data_date1_to_date3, right_frame, selected_country)
            else:
                show_waiting_message()

            data = load_data(selected_country)

            filtered_data = filter_data_by_dates(data, date1, date2)
            # prediction_charts = nowy3(filtered_data, future_date)
            country_chart_total = plot_country_chart(filtered_data, selected_country, 'total')
            country_chart_new = plot_country_chart(filtered_data, selected_country, 'new')
            charts = [country_chart_total, country_chart_new]
            current_chart_index = 0
            show_current_chart()
        except ValueError as e:
            log_message(f"Error parsing dates: {e}")
        except KeyError as e:
            log_message(f"Key error: {e}")
            print(f"Key error: {e}")
            print(f"Data for {selected_country}: {data}")

            log_message(f"Incorrect date format: {e}")
        except Exception as e:
            log_message(f"Error: {e}")

    def filter_data_by_dates(data, start_date, end_date):
        """Filtruje dane na podstawie podanego zakresu dat."""
        filtered_cases = {date: details for date, details in data[0]['cases'].items() if
                          start_date <= datetime.datetime.strptime(date, '%Y-%m-%d') <= end_date}
        return [{'country': data[0]['country'], 'region': data[0]['region'], 'cases': filtered_cases}]

    def log_message(message):
        alert_label.configure(text=message, text_color="white", font=("Arial", 20))
        print(message)
        # Change color back after 3 seconds
        alert_label.after(3000, lambda: alert_label.configure(text_color="#242424"))

    def open_manual_entry_window():
        manual_entry_window = customtkinter.CTkToplevel(root)
        manual_entry_window.title("Enter country manually")

        entry_label = customtkinter.CTkLabel(manual_entry_window, text="Enter country:")
        entry_label.pack(pady=10)

        country_entry = customtkinter.CTkEntry(manual_entry_window, width=250)
        country_entry.pack(pady=10)

        def manual_entry_submit():
            global manual_entry_result
            global search_query

            search_query = country_entry.get().strip().capitalize()
            if search_country_in_file(search_query):
                log_message(f"Selected country: {search_query}")
                manual_entry_result = True
                manual_entry_window.destroy()
                # listbox.selection_clear(0, customtkinter.END)
            else:
                log_message("Incorrect country given!")

        button_frame = customtkinter.CTkFrame(manual_entry_window)
        button_frame.pack(pady=10)

        cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=manual_entry_window.destroy)
        cancel_button.pack(side="left", padx=10)

        submit_button = customtkinter.CTkButton(button_frame, text="Accept", command=manual_entry_submit)
        submit_button.pack(side="right", padx=10)

        # Set the position of the manual entry window
        manual_entry_button_pos = manual_entry_button.winfo_rootx(), manual_entry_button.winfo_rooty()
        manual_entry_window.geometry(f"+{manual_entry_button_pos[0]}+{manual_entry_button_pos[1] - 100}")

        manual_entry_window.transient(root)
        manual_entry_window.grab_set()
        manual_entry_window.focus_set()
        manual_entry_window.attributes('-topmost', True)

    def on_listbox_select(event):
        global manual_entry_result, search_query
        manual_entry_result = False
        search_query = listbox.get(listbox.curselection())
        log_message(f"Selected country: {search_query}")

    window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
    root.geometry(f"{window_width}x{window_height}")
    center_window(root, window_width, window_height)

    right_frame = customtkinter.CTkFrame(root, width=800, height=window_height - 100, border_width=5,
                                         border_color="#F9AA33")
    right_frame.place(relx=0.62, rely=0.47, anchor="center")

    show_waiting_message()

    left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
    left_frame.place(relx=0.145, rely=0.37, anchor="center")

    listbox = CTkListbox(left_frame, width=250, height=150)
    listbox.pack(pady=10)
    listbox.bind("<<ListboxSelect>>", on_listbox_select)

    manual_entry_button = customtkinter.CTkButton(left_frame, text="Enter manually", command=open_manual_entry_window)
    manual_entry_button.pack(pady=5)

    countries = load_countries()
    for i, country in enumerate(countries):
        listbox.insert(i, country)

    date_label = customtkinter.CTkLabel(left_frame, text="Select three dates (DD-MM-YYYY):")
    date_label.pack(pady=5)

    date_frame = customtkinter.CTkFrame(left_frame)
    date_frame.pack(pady=5)

    # Pierwsza data
    date_label1 = customtkinter.CTkLabel(date_frame, text="from:")
    date_label1.grid(row=0, column=0, padx=5)
    date_entry1 = DateEntry(date_frame, width=18, background="black", disabledbackground="black", bordercolor="white",
                            headersbackground="#242424", normalbackground="black", foreground='white',
                            normalforeground='white', headersforeground='white', borderwidth=2,
                            date_pattern='dd-mm-yyyy')
    date_entry1.grid(row=0, column=1, padx=5)

    # Druga data
    date_label2 = customtkinter.CTkLabel(date_frame, text="to:")
    date_label2.grid(row=1, column=0, padx=5)
    date_entry2 = DateEntry(date_frame, width=18, background="black", disabledbackground="black", bordercolor="white",
                            headersbackground="#242424", normalbackground="black", foreground='white',
                            normalforeground='white', headersforeground='white', borderwidth=2,
                            date_pattern='dd-mm-yyyy')
    date_entry2.grid(row=1, column=1, padx=5)

    # Trzecia data
    date_label3 = customtkinter.CTkLabel(date_frame, text="prediction to:")
    date_label3.grid(row=2, column=0, padx=5)
    date_entry3 = DateEntry(date_frame, width=18, background="black", disabledbackground="black", bordercolor="white",
                            headersbackground="#242424", normalbackground="black", foreground='white',
                            normalforeground='white', headersforeground='white', borderwidth=2,
                            date_pattern='dd-mm-yyyy')
    date_entry3.grid(row=2, column=1, padx=5)

    submit_button = customtkinter.CTkButton(left_frame, text="Start", command=lambda: on_submit_dates(
        [date_entry1.get(), date_entry2.get(), date_entry3.get()]))
    submit_button.pack(pady=10)

    # Ramka dla alertów
    alert_frame = customtkinter.CTkFrame(root, height=50, fg_color="#242424")
    alert_frame.pack(fill='x', side='bottom')

    # Etykieta dla wyświetlania alertów
    alert_label = customtkinter.CTkLabel(alert_frame, text="", font=("Arial", 20))
    alert_label.pack(pady=15)

    navigation_frame = customtkinter.CTkFrame(left_frame)
    navigation_frame.pack(pady=20)

    prev_button = customtkinter.CTkButton(navigation_frame, text="Previous", command=on_prev)
    prev_button.pack(side="left", padx=10)

    next_button = customtkinter.CTkButton(navigation_frame, text="Next", command=on_next)
    next_button.pack(side="right", padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()