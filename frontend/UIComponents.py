import customtkinter
from CTkListbox import CTkListbox
from tkcalendar import DateEntry

def create_right_frame(root, window_height):
    right_frame = customtkinter.CTkFrame(root, width=800, height=window_height - 100, border_width=5, border_color="#F9AA33")
    right_frame.place(relx=0.62, rely=0.47, anchor="center")
    return right_frame

def create_left_frame(root, window_height):
    left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
    left_frame.place(relx=0.145, rely=0.37, anchor="center")

    listbox = CTkListbox(left_frame, width=250, height=150)
    listbox.pack(pady=10)

    manual_entry_button = customtkinter.CTkButton(left_frame, text="Enter manually")
    manual_entry_button.pack(pady=5)

    date_label = customtkinter.CTkLabel(left_frame, text="Select three dates (DD-MM-YYYY):")
    date_label.pack(pady=5)

    date_frame = customtkinter.CTkFrame(left_frame)
    date_frame.pack(pady=5)

    date_entries = []
    for i, label in enumerate(["from:", "to:", "prediction to:"]):
        date_label = customtkinter.CTkLabel(date_frame, text=label)
        date_label.grid(row=i, column=0, padx=5)
        date_entry = DateEntry(date_frame, width=18, background="black", disabledbackground="black", bordercolor="white",
                               headersbackground="#242424", normalbackground="black", foreground='white',
                               normalforeground='white', headersforeground='white', borderwidth=2,
                               date_pattern='dd-mm-yyyy')
        date_entry.grid(row=i, column=1, padx=5)
        date_entries.append(date_entry)

    submit_button = customtkinter.CTkButton(left_frame, text="Start")
    submit_button.pack(pady=10)

    alert_frame = customtkinter.CTkFrame(root, height=50, fg_color="#242424")
    alert_frame.pack(fill='x', side='bottom')

    alert_label = customtkinter.CTkLabel(alert_frame, text="", font=("Arial", 20))
    alert_label.pack(pady=15)

    navigation_frame = customtkinter.CTkFrame(left_frame)
    navigation_frame.pack(pady=20)

    prev_button = customtkinter.CTkButton(navigation_frame, text="Previous")
    prev_button.pack(side="left", padx=10)

    next_button = customtkinter.CTkButton(navigation_frame, text="Next")
    next_button.pack(side="right", padx=10)

    details_button = customtkinter.CTkButton(left_frame, text="Show Details", fg_color="#F9AA33", hover_color="#956720", text_color="#242424")
    details_button.pack(pady=10)

    return left_frame, listbox, manual_entry_button, date_entries, submit_button, details_button, prev_button, next_button

def show_waiting_message(right_frame):
    for widget in right_frame.winfo_children():
        widget.destroy()
    waiting_label = customtkinter.CTkLabel(right_frame, text="Waiting for data...", font=("Arial", 20))
    waiting_label.place(relx=0.5, rely=0.5, anchor="center")
