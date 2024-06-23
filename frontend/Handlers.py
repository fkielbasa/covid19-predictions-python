import datetime
import customtkinter
from backend.DataManagement import load_data
from Plotting import plot_country_chart
from frontend.DataUtils import filter_data_by_dates
from frontend.UIComponents import show_waiting_message, create_right_frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

current_chart_index = 0
charts = []
current_data = []
selected_country = ""
date_entries = []


def handle_submit_dates(date_entries_param, listbox, right_frame, manual_entry=None):
    global current_chart_index, current_data, selected_country, date_entries
    date_entries = date_entries_param
    try:
        date1 = datetime.datetime.strptime(date_entries[0].get(), "%d-%m-%Y")
        date2 = datetime.datetime.strptime(date_entries[1].get(), "%d-%m-%Y")
        date3 = datetime.datetime.strptime(date_entries[2].get(), "%d-%m-%Y")

        if date2 <= date1 or (date2 - date1).days < 89:
            log_message("The second date must be at least 3 months later than the first.")
            return
        if date3 <= date1 or date3 <= date2:
            log_message("The third date must be later than the second and first.")
            return

        if manual_entry:
            selected_country = manual_entry
        else:
            selected_country = listbox.get(listbox.curselection())

        data = load_data(selected_country)
        if not data:
            log_message(f"No data found for {selected_country}")
            return

        current_data = data
        filtered_data = filter_data_by_dates(data, date1, date2)
        charts.clear()  # Clear existing charts
        charts.append(plot_country_chart(filtered_data, selected_country, 'total'))
        charts.append(plot_country_chart(filtered_data, selected_country, 'new'))
        current_chart_index = 0
        show_current_chart(right_frame)

    except ValueError as e:
        log_message(f"Error parsing dates: {e}")
    except KeyError as e:
        log_message(f"Key error: {e}")
    except Exception as e:
        log_message(f"Error: {e}")


def handle_prev(right_frame):
    global current_chart_index
    if current_chart_index > 0:
        current_chart_index -= 1
    show_current_chart(right_frame)


def handle_next(right_frame):
    global current_chart_index
    if current_chart_index < len(charts) - 1:
        current_chart_index += 1
    show_current_chart(right_frame)


def handle_details():
    if not current_data:
        log_message("No data available to show details.")
        return

    open_details_window(current_data, selected_country, date_entries)


def handle_listbox_select(event, listbox):
    global selected_country
    selected_country = listbox.get(listbox.curselection())
    log_message(f"Selected country: {selected_country}")


import customtkinter

def handle_manual_entry(date_entries, right_frame):
    manual_entry_window = customtkinter.CTkToplevel()
    manual_entry_window.title("Enter country manually")
    manual_entry_window.geometry("300x150")

    label = customtkinter.CTkLabel(manual_entry_window, text="Enter Country:", font=("Arial", 14))
    label.pack(pady=10)

    entry = customtkinter.CTkEntry(manual_entry_window, width=250)
    entry.pack(pady=10)

    button_frame = customtkinter.CTkFrame(manual_entry_window)
    button_frame.pack(pady=10)

    submit_button = customtkinter.CTkButton(button_frame, text="Submit",
                                            command=lambda: submit_manual_entry(entry, manual_entry_window, date_entries, right_frame))
    submit_button.pack(side="left", padx=10)

    cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", command=manual_entry_window.destroy)
    cancel_button.pack(side="right", padx=10)



def submit_manual_entry(entry, window, date_entries, right_frame):
    manual_entry_country = entry.get()
    window.destroy()
    # Call the handle_submit_dates function with manual entry
    handle_submit_dates(date_entries, None, right_frame, manual_entry_country)


def show_current_chart(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()

    if charts:
        charts[current_chart_index].set_size_inches(9, 7)
        canvas = FigureCanvasTkAgg(charts[current_chart_index], master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    else:
        show_waiting_message(right_frame)


def log_message(message):
    print(message)


def sum_new_cases(data, start_date, end_date):
    total_new_cases = 0
    for date, details in data[0]['cases'].items():
        current_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        if start_date <= current_date <= end_date:
            total_new_cases += details.get('new', 0)
    return total_new_cases


def open_details_window(data, selected_country, date_entries):
    details_window = customtkinter.CTkToplevel()
    details_window.title("Details")
    details_window.geometry("400x400")

    date1_str = date_entries[0].get()
    date2_str = date_entries[1].get()
    date3_str = date_entries[2].get()

    date1 = datetime.datetime.strptime(date1_str, "%d-%m-%Y")
    date2 = datetime.datetime.strptime(date2_str, "%d-%m-%Y")
    date3 = datetime.datetime.strptime(date3_str, "%d-%m-%Y")

    diff_from_to = (date2 - date1).days
    diff_to_prediction = (date3 - date2).days
    diff_from_prediction = (date3 - date1).days

    new_cases_from_to = sum_new_cases(data, date1, date2)
    new_cases_to_prediction = sum_new_cases(data, date2, date3)

    country_label = customtkinter.CTkLabel(details_window, text=f"Selected Country: {selected_country}")
    country_label.pack(pady=10)

    date1_label = customtkinter.CTkLabel(details_window, text=f"From: {date1_str}")
    date1_label.pack(pady=10)

    date2_label = customtkinter.CTkLabel(details_window, text=f"To: {date2_str}")
    date2_label.pack(pady=10)

    date3_label = customtkinter.CTkLabel(details_window, text=f"Prediction To: {date3_str}")
    date3_label.pack(pady=10)

    diff_from_to_label = customtkinter.CTkLabel(details_window, text=f"Difference (from - to): {diff_from_to} days")
    diff_from_to_label.pack(pady=10)

    diff_to_prediction_label = customtkinter.CTkLabel(details_window,
                                                      text=f"Difference (to - prediction to): {diff_to_prediction} days")
    diff_to_prediction_label.pack(pady=10)

    diff_from_prediction_label = customtkinter.CTkLabel(details_window,
                                                        text=f"Difference (from - prediction to): {diff_from_prediction} days")
    diff_from_prediction_label.pack(pady=10)

    new_cases_from_to_label = customtkinter.CTkLabel(details_window, text=f"New Cases (from - to): {new_cases_from_to}")
    new_cases_from_to_label.pack(pady=10)

    new_cases_to_prediction_label = customtkinter.CTkLabel(details_window,
                                                           text=f"New Cases (to - prediction to): {new_cases_to_prediction}")
    new_cases_to_prediction_label.pack(pady=10)

    details_window.attributes('-topmost', True)
