import customtkinter
from WindowUtils import calculate_window_size, center_window
from UIComponents import create_right_frame, create_left_frame, show_waiting_message
from Handlers import handle_submit_dates, handle_prev, handle_next, handle_details, handle_listbox_select, handle_manual_entry
from DataUtils import load_countries

def main():
    root = customtkinter.CTk()
    root.title("Corona Rush")
    root.iconbitmap("icon.ico")

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
    root.geometry(f"{window_width}x{window_height}")
    center_window(root, window_width, window_height)

    right_frame = create_right_frame(root, window_height)
    left_frame, listbox, manual_entry_button, date_entries, submit_button, details_button, prev_button, next_button = create_left_frame(root, window_height)

    show_waiting_message(right_frame)

    countries = load_countries()
    for i, country in enumerate(countries):
        listbox.insert(i, country)

    submit_button.configure(command=lambda: handle_submit_dates(date_entries, listbox, right_frame))
    details_button.configure(command=handle_details)
    manual_entry_button.configure(command=lambda: handle_manual_entry(date_entries, right_frame))
    prev_button.configure(command=lambda: handle_prev(right_frame))
    next_button.configure(command=lambda: handle_next(right_frame))
    listbox.bind("<<ListboxSelect>>", lambda event: handle_listbox_select(event, listbox))

    root.mainloop()

if __name__ == "__main__":
    main()
