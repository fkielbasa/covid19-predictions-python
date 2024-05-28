import customtkinter


from data_management import load_countries
from plotting import plot_data, show_waiting_message
from data_management import load_data


def create_left_frame(root, window_height, right_frame):
    left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
    left_frame.place(relx=0.145, rely=0.33, anchor="center")
    setup_listbox(left_frame, right_frame)
    return left_frame

def setup_listbox(frame, right_frame):
    listbox = customtkinter.CTkListbox(frame, command=lambda event: on_country_selected(event, listbox, right_frame), width=250, height=150)
    listbox.pack(pady=10)
    countries = load_countries()
    for i, country in enumerate(countries):
        listbox.insert(i, country)

def create_right_frame(root, window_height):
    right_frame = customtkinter.CTkFrame(root, width=800, height=window_height-100, border_width=5, border_color="#F9AA33")
    right_frame.place(relx=0.62, rely=0.47, anchor="center")
    show_waiting_message(right_frame)
    return right_frame

