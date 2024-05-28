import json

import customtkinter
import matplotlib.dates as mdates
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.dates as mdates

def plot_data(data, frame, country):
    # Przypisanie wartości dla 'cases' do zmiennej dla łatwiejszego dostępu
    cases = data[0]['cases']

    # Konwersja kluczy słownika 'cases' na obiekty datetime
    days_datetime = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in cases.keys()]

    # Konwersja obiektów datetime na liczby reprezentujące dni (przed normalizacją)
    days2 = [mdates.date2num(day) for day in days_datetime]

    # Normalizacja dni, aby zaczynały się od zera
    min_day = min(days2)
    days = [day - min_day for day in days2]

    # Odczyt wartości 'new' dla każdej daty
    values = [details['new'] for date, details in cases.items()]

    # Interpolacja sześcienna dla wygładzenia danych
    interp_days = np.linspace(min(days), max(days), 1000)  # Więcej punktów dla gładkości
    cubic_interp = interp1d(days, values, kind='cubic')
    smooth_values = cubic_interp(interp_days)

    fig, ax = plt.subplots(figsize=(10, 7))  # Zwiększamy rozmiar figury
    ax.plot(days, values, marker='o')

    # Dodajemy wykres liniowy wygładzony
    ax.plot(interp_days, smooth_values, label='Smooth Line Chart', color='red')

    ax.set(xlabel='Day', ylabel='New', title=f'Covid Data for {country}')
    ax.grid()

    ax.title.set_size(20)  # Zwiększamy rozmiar tytułu
    ax.xaxis.label.set_size(14)  # Zwiększamy rozmiar etykiety osi X
    ax.yaxis.label.set_size(14)  # Zwiększamy rozmiar etykiety osi Y
    ax.tick_params(axis='both', which='major', labelsize=12)  # Zwiększamy rozmiar etykiet ticków

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

