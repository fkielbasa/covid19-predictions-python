import customtkinter
from CTkListbox import *
import datetime

from pandas.core import frame

from configuration import setup_appearance
from window_utils import calculate_window_size, center_window
import requests
from predictive import *
from plotting import plot_data
from data_management import  load_data,load_countries
import customtkinter
from CTkListbox import *
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import interp1d
import datetime
from main_backend import nowy2

from sklearn.linear_model import LinearRegression

from predictive import *
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.dates as mdates

import pandas as pd
import numpy as np
import datetime as dt
import warnings
import os

from DataService import getData


current_chart_index = 0  # indeks aktualnie wyświetlanego wykresu
charts = []  # lista funkcji, które generują wykresy
data_for_charts = None  # dane używane do generowania wykresów

def main():

    global  current_chart_index


    root = customtkinter.CTk()

    root.title("Corona Rush")

    root.iconbitmap("icon.ico")

    setup_appearance()











    def nowy3(data):
        global charts




        """Eksperyment predykcji"""
        warnings.filterwarnings("ignore")

        # Utworzenie ramki danych z normalną datą
        drow = []

        cases = data[0]['cases']
        # Utworzenie ramki danych z normalną datą
        drow = []

        for date, case_info in cases.items():
            date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
            drow.append((date_obj, date_obj.timestamp(), case_info['total']))
        df = pd.DataFrame(drow, columns=["date", "timestamp", "total"])

        print(df, os.linesep)

        # Przeskalowanie liczby całkowitej, jeśli jest to konieczne
        max_total = df['total'].max()
        if max_total > 1e9:
            df['total'] = df['total'] / 1e9  # Przeskalowanie przez miliard
            ylabel = "nowe przypadki (w mld)"
        elif max_total > 1e6:
            df['total'] = df['total'] / 1e6  # Przeskalowanie przez milion
            ylabel = "nowe przypadki (w mln)"
        else:
            ylabel = "nowe przypadki"

        x_feature = "timestamp"
        y_feature = "total"
        xlabel = "data"
        title = "covidowe przypadki"

        # Wykres punktowy kompletnego zbioru pobranych danych
        visualize_plot_scatter1=visualize_plot_scatter(x_plot=None, y_plot=None, x_scatter=df["date"], y_scatter=df.loc[:, y_feature],
                               title=title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")

        # Utworzenie i wyświetlenie początkowych danych ZBIÓR UCZĄCEGO
        df_train = df[pd.to_datetime(df.date) < pd.to_datetime("2022-01-01")]
        print(df_train.head(), os.linesep)

        # Utworzenie i wyświetlenie początkowych danych ZBIÓR TESTOWEGO
        df_test = df[pd.to_datetime(df.date) >= pd.to_datetime("2022-01-01")]
        print(df_test.head(), os.linesep)
        print(df_train)
        print(df_test)

        print("Rozmiar ZBIORU UCZĄCEGO: ", df_train.loc[:, y_feature].count() / df.loc[:, y_feature].count())
        print("Rozmiar ZBIORU TESTOWEGO: ", df_test.loc[:, y_feature].count() / df.loc[:, y_feature].count(),
              os.linesep)

        # Wykres punktowy z oznaczeniem lat ZBIÓR UCZĄCEGO
        visualize1=visualize(df=df_train, x="date", y=y_feature, title=title + "\n{Zbiór UCZĄCY}", grouping="date")

        # Wykres punktowy z oznaczeniem lat ZBIÓR TESTOWY
        visualize2=visualize(df=df_test, x="date", y=y_feature, title=title + "\n{Zbiór TESTOWY}", grouping="date")

        # Wykres punktowy ZBIÓR UCZĄCEGO
        visualize3=visualize(df=df_train, x="date", y=y_feature, title=title + "\n{Zbiór UCZĄCY}", regression=False)

        # Wykres punktowy z regresją liniową ZBIÓR UCZĄCEGO
        visualize4=visualize(df=df_train, x="date", y=y_feature, title=title + " & " + "Regresja" + "\n{Zbiór UCZĄCY}",
                  regression=True)

        # Współczynnik korelacji liniowej Pearsona
        pc = np.corrcoef(df_train[x_feature], df_train[y_feature])
        print("Współczynnik korelacji liniowej Pearsona:\n", pc, os.linesep)

        # Utworzenie modelu predykcji tj. predyktora z wykorzystaniem REGRESJI LINIOWEJ
        x_train = np.array(df_train[x_feature]).reshape((-1, 1))
        y_train = np.array(df_train[y_feature])
        model, description = predictor(x_train, y_train)
        print(description, os.linesep)

        # Wizualizacja modelu predykcji
        x = np.linspace(np.min(x_train), np.max(x_train), 5000).flatten()
        y = model.coef_ * x + model.intercept_

        # Przekształcenie wartości x z powrotem do dat
        x_dates = [datetime.datetime.fromtimestamp(ts) for ts in x]

        chart_title = "MODEL PREDYKCJI\n" + title + " & " + "Regresja"
        visualize_plot_scatter2=visualize_plot_scatter(x_plot=x_dates, y_plot=y, x_scatter=df_train["date"], y_scatter=y_train,
                               title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange",
                               scatter_color="green")

        # Predykcja
        x_test = np.array(df_test[x_feature]).reshape((-1, 1))
        y_test = np.array(df_test[y_feature])
        df_prediction, description = prediction(model, x_test, y_test)
        print("Rezultat predykcji:")
        print(df_prediction, os.linesep)

        # Ocena [modelu] predykcji
        print(description, os.linesep)

        # Wizualizacja predykcji
        x_test_dates = df_test["date"]
        chart_title = "PREDYKCJA\n" + title + " & " + "Regresja"
        visualize_plot_scatter(x_plot=x_test_dates, y_plot=df_prediction["y_pred"], x_scatter=x_test_dates,
                               y_scatter=y_test,
                               title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange",
                               scatter_color="green")

        charts.append(visualize_plot_scatter1)
        print("Added scatter1 to charts")
        charts.append(visualize_plot_scatter2)
        charts.append(visualize1)
        charts.append(visualize2)
        charts.append(visualize3)
        charts.append(visualize4)
        return charts



















        # Domyslnie pokaz pierwszy wykres

    def show_waiting_message():
        for widget in right_frame.winfo_children():
            widget.destroy()
        waiting_label = customtkinter.CTkLabel(right_frame, text="Waiting for data...", font=("Arial", 20))
        waiting_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_country_selected(events):
        global current_chart_index,charts
        selected_country = listbox.get(listbox.curselection())
        data = load_data(selected_country)
        nowy3(data)
        if data:
                plot_data(data, right_frame, selected_country)
        else:
            show_waiting_message()

    # Obliczenie i ustawienie rozmiaru okna na podstawie rozmiaru ekranu
    window_width, window_height = calculate_window_size(root.winfo_screenwidth(), root.winfo_screenheight())
    root.geometry(f"{window_width}x{window_height}")
    center_window(root, window_width, window_height)

    # Prawy panel
    right_frame = customtkinter.CTkFrame(root, width=800, height=window_height-100, border_width=5, border_color="#F9AA33")
    right_frame.place(relx=0.62, rely=0.47, anchor="center")

    # Początkowa wiadomość "Waiting for data..."
    show_waiting_message()

    # Lewy panel
    left_frame = customtkinter.CTkFrame(root, width=300, height=window_height)
    left_frame.place(relx=0.145, rely=0.33, anchor="center")

    # Lista rozwijalna w ramce
    listbox = CTkListbox(left_frame, command=on_country_selected, width=250, height=150)
    listbox.pack(pady=10)

    # Wczytaj listę krajów z pliku JSON i wypełnij listbox
    countries = load_countries()
    for i, country in enumerate(countries):
        listbox.insert(i, country)


######################################################################
    # Pole do wpisania dat
    date_label = customtkinter.CTkLabel(left_frame, text="Wprowadź trzy daty (DD-MM-YYYY):")
    date_label.pack(pady=5)

    # Ramka dla dat
    date_frame = customtkinter.CTkFrame(left_frame)
    date_frame.pack(pady=5)

    # Pierwsza data
    date_label1 = customtkinter.CTkLabel(date_frame, text="od:")
    date_label1.grid(row=0, column=0, padx=5)
    date_entry1 = customtkinter.CTkEntry(date_frame, width=150)
    date_entry1.grid(row=0, column=1, padx=5)

    # Druga data
    date_label2 = customtkinter.CTkLabel(date_frame, text="do:")
    date_label2.grid(row=1, column=0, padx=5)
    date_entry2 = customtkinter.CTkEntry(date_frame, width=150)
    date_entry2.grid(row=1, column=1, padx=5)

    # Trzecia data
    date_label3 = customtkinter.CTkLabel(date_frame, text="predykcja do:")
    date_label3.grid(row=2, column=0, padx=5)
    date_entry3 = customtkinter.CTkEntry(date_frame, width=150)
    date_entry3.grid(row=2, column=1, padx=5)

    # Przycisk do zatwierdzenia dat
    submit_button = customtkinter.CTkButton(left_frame, text="Submit Dates", command=lambda: on_submit_dates([date_entry1.get(), date_entry2.get(), date_entry3.get()]))
    submit_button.pack(pady=10)

#################################################################
    def on_prev():
        # Dodaj logikę do przewijania wykresów w lewo
        print("Przejście do poprzedniego wykresu")
        global current_chart_index
        if current_chart_index > 0:
            current_chart_index -= 1
        '''charts[current_chart_index]'''
        # Usuwanie istniejących widgetów z right_frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Tworzenie canvas dla wykresu matplotlib
        canvas = FigureCanvasTkAgg(charts[current_chart_index], master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


    def on_next():
        # Dodaj logikę do przewijania wykresów w prawo
        print("Przejście do następnego wykresu")
        global current_chart_index
        if current_chart_index < len(charts) - 1:
            current_chart_index += 1
        ''' charts[current_chart_index]'''
        # Usuwanie istniejących widgetów z right_frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Tworzenie canvas dla wykresu matplotlib
        canvas = FigureCanvasTkAgg(charts[current_chart_index], master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


    # Ramka dla przycisków nawigacyjnych
    navigation_frame = customtkinter.CTkFrame(left_frame)
    navigation_frame.pack(pady=20)

    # Przycisk do przewijania w lewo
    prev_button = customtkinter.CTkButton(navigation_frame, text="Poprzedni", command=on_prev)
    prev_button.pack(side="left", padx=10)

    # Przycisk do przewijania w prawo
    next_button = customtkinter.CTkButton(navigation_frame, text="Następny", command=on_next)





































    def on_submit_dates(dates):
        try:
            # Konwersja dat na obiekt datetime
            date1 = datetime.datetime.strptime(dates[0], "%d-%m-%Y")
            date2 = datetime.datetime.strptime(dates[1], "%d-%m-%Y")
            date3 = datetime.datetime.strptime(dates[2], "%d-%m-%Y")

            # Sprawdzenie warunków
            if date2 <= date1 or (date2 - date1).days < 7:
                print("Druga data musi być co najmniej 7 dni późniejsza od pierwszej.")
                return
            if date3 <= date1 or date3 <= date2:
                print("Trzecia data musi być późniejsza niż pierwsza i druga.")
                return

            formatted_dates = [date1.strftime("%Y-%m-%d"), date2.strftime("%Y-%m-%d"), date3.strftime("%Y-%m-%d")]
            for date in formatted_dates:
                print(date)

            selected_country = listbox.get(listbox.curselection())
            data = load_data(selected_country)
            filtered_data = [entry for entry in data if entry['day'] in formatted_dates]
            if filtered_data:
                plot_data(filtered_data, right_frame, selected_country)
            else:
                show_waiting_message()

        except ValueError as e:
            print(f"Error parsing dates: {e}")









    next_button.pack(side="right", padx=10)

    root.mainloop()


if __name__ == "__main__":
    main()