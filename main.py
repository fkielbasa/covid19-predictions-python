import datetime
import warnings

from sklearn.linear_model import LinearRegression

from predictive import *


import pandas as pd
import numpy as np
import datetime as dt
import warnings
import os

from DataService import getData


def make_experiment_prediction(data):
    """Eksperyment predykcji"""
    warnings.filterwarnings("ignore")

    # Utworzenie ramki danych
    drow = []
    for i in data.cases:
        drow.append((i.date, i.total, i.new))
    df = pd.DataFrame(drow, columns=["date", "total", "new"])
    print(df, os.linesep)

    x_feature = "date"
    y_feature = "total"
    xlabel = "dejt"
    ylabel = "nowe przypadki"
    title = "covidowe chuje"

    # Wykres punktowy kompletnego zbioru pobranych danych
    visualize_plot_scatter(x_plot=None, y_plot=None, x_scatter=df.loc[:, x_feature], y_scatter=df.loc[:, y_feature],
                           title=title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")

    # Utworzenie i wyświetlenie początkowych danych ZBIÓR UCZĄCEGO
    df_train = df[pd.to_datetime(df.date) < pd.to_datetime("2022-01-01")]
    print(df_train.head, os.linesep)

    # Utworzenie i wyświetlenie początkowych danych ZBIÓR TESTOWEGO
    df_test = df[pd.to_datetime(df.date) >= pd.to_datetime("2022-01-01")]
    print(df_test.head, os.linesep)
    print(df_train)
    print(df_test)

    print("Rozmiar ZBIORU UCZĄCEGO: ", df_train.loc[:, y_feature].count() / df.loc[:, y_feature].count())
    print("Rozmiar ZBIORU TESTOWEGO: ", df_test.loc[:, y_feature].count() / df.loc[:, y_feature].count(), os.linesep)

    # Wykres punktowy z oznaczeniem lat ZBIÓR UCZĄCY
    visualize(df=df_train, x=x_feature, y=y_feature, title=title + "\n{Zbiór UCZĄCY}", grouping="date")

    # Wykres punktowy z oznaczeniem lat ZBIÓR TESTOWY
    visualize(df=df_test, x=x_feature, y=y_feature, title=title + "\n{Zbiór TESTOWY}", grouping="date")

    # Wykres punktowy ZBIÓR UCZĄCY
    visualize(df=df_train, x=x_feature, y=y_feature, title=title + "\n{Zbiór UCZĄCY}", regression=False)

    # Wykres punktowy z regresją liniową ZBIÓR UCZĄCY
    visualize(df=df_train, x=x_feature, y=y_feature, title=title + " & " + "Regresja" + "\n{Zbiór UCZĄCY}",
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
    x = np.linspace(np.min(x_train), max(x_train), 5000)
    y = model.coef_ * x + model.intercept_
    chart_title = "MODEL PREDYKCJI\n" + title + " & " + "Regresja"
    visualize_plot_scatter(x_plot=x, y_plot=y, x_scatter=x_train, y_scatter=y_train,
                           title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")

    # Predykcja
    x_test = np.array(df_test[x_feature]).reshape((-1, 1))
    y_test = np.array(df_test[y_feature])
    df_prediction, description = prediction(model, x_test, y_test)
    print("Rezultat predykcji:")
    print(df_prediction, os.linesep)

    # Ocena [modelu] predykcji
    print(description, os.linesep)

    # Wizualizacja predykcji
    chart_title = "PREDYKCJA\n" + title + " & " + "Regresja"
    visualize_plot_scatter(x_plot=x_test, y_plot=df_prediction["y_pred"], x_scatter=x_test, y_scatter=y_test,
                           title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")


def test(data):
    drow = []
    for i in data.cases:
        drow.append((i.date, i.total))
    df = pd.DataFrame(drow, columns=["date", "total"])

    # Podziel dane na zbiór uczący i testowy
    df['date'] = pd.to_datetime(df['date'])
    df_train = df[df['date'] < pd.to_datetime("2022-01-01")]
    df_test = df[df['date'] >= pd.to_datetime("2022-01-01")]

    # Przygotuj dane do modelu
    X_train = df_train[['total']]  # Zmienna objaśniająca
    y_train = df_train['date']  # Zmienna celu

    X_test = df_test[['total']]
    y_test = df_test['date']

    # Utwórz i dopasuj model regresji liniowej
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Wykonaj predykcję na zbiorze testowym
    y_pred = model.predict(X_test)

    # Wykresy
    plt.figure(figsize=(12, 6))

    # Wykres danych rzeczywistych
    plt.scatter(df_test['total'], df_test['date'], color='blue', label='Dane rzeczywiste')

    # Wykres predykcji
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predykcja')

    plt.title('Predykcja liczby nowych przypadków w zależności od sumy przypadków')
    plt.xlabel('Suma przypadków')
    plt.ylabel('Data')
    plt.legend()
    plt.show()

def nowy(data):
    """Eksperyment predykcji"""
    warnings.filterwarnings("ignore")

    # Utworzenie ramki danych
    drow = []
    for i in data.cases:
        drow.append((datetime.datetime.strptime(i.date, "%Y-%m-%d").timestamp(), i.total))
    df = pd.DataFrame(drow, columns=["date", "total"])
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

    x_feature = "date"
    y_feature = "total"
    xlabel = "dejt"
    title = "covidowe chuje"

    # Wykres punktowy kompletnego zbioru pobranych danych
    visualize_plot_scatter(x_plot=None, y_plot=None, x_scatter=df.loc[:, x_feature], y_scatter=df.loc[:, y_feature],
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
    print("Rozmiar ZBIORU TESTOWEGO: ", df_test.loc[:, y_feature].count() / df.loc[:, y_feature].count(), os.linesep)

    # Wykres punktowy z oznaczeniem lat ZBIÓR UCZĄCY
    visualize(df=df_train, x=x_feature, y=y_feature, title=title + "\n{Zbiór UCZĄCY}", grouping="date")

    # Wykres punktowy z oznaczeniem lat ZBIÓR TESTOWY
    visualize(df=df_test, x=x_feature, y=y_feature, title=title + "\n{Zbiór TESTOWY}", grouping="date")

    # Wykres punktowy ZBIÓR UCZĄCY
    visualize(df=df_train, x=x_feature, y=y_feature, title=title + "\n{Zbiór UCZĄCY}", regression=False)

    # Wykres punktowy z regresją liniową ZBIÓR UCZĄCY
    visualize(df=df_train, x=x_feature, y=y_feature, title=title + " & " + "Regresja" + "\n{Zbiór UCZĄCY}",
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
    x = np.linspace(np.min(x_train), max(x_train), 5000)
    y = model.coef_ * x + model.intercept_
    chart_title = "MODEL PREDYKCJI\n" + title + " & " + "Regresja"
    visualize_plot_scatter(x_plot=x, y_plot=y, x_scatter=x_train, y_scatter=y_train,
                           title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")

    # Predykcja
    x_test = np.array(df_test[x_feature]).reshape((-1, 1))
    y_test = np.array(df_test[y_feature])
    df_prediction, description = prediction(model, x_test, y_test)
    print("Rezultat predykcji:")
    print(df_prediction, os.linesep)

    # Ocena [modelu] predykcji
    print(description, os.linesep)

    # Wizualizacja predykcji
    chart_title = "PREDYKCJA\n" + title + " & " + "Regresja"
    visualize_plot_scatter(x_plot=x_test, y_plot=df_prediction["y_pred"], x_scatter=x_test, y_scatter=y_test,
                           title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")



def nowy2(data):
    """Eksperyment predykcji"""
    warnings.filterwarnings("ignore")

    # Utworzenie ramki danych z normalną datą
    drow = []
    for i in data.cases:
        date_obj = datetime.datetime.strptime(i.date, "%Y-%m-%d")
        drow.append((date_obj, date_obj.timestamp(), i.total))
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
    visualize_plot_scatter(x_plot=None, y_plot=None, x_scatter=df["date"], y_scatter=df.loc[:, y_feature],
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
    print("Rozmiar ZBIORU TESTOWEGO: ", df_test.loc[:, y_feature].count() / df.loc[:, y_feature].count(), os.linesep)

    # Wykres punktowy z oznaczeniem lat ZBIÓR UCZĄCEGO
    visualize(df=df_train, x="date", y=y_feature, title=title + "\n{Zbiór UCZĄCY}", grouping="date")

    # Wykres punktowy z oznaczeniem lat ZBIÓR TESTOWY
    visualize(df=df_test, x="date", y=y_feature, title=title + "\n{Zbiór TESTOWY}", grouping="date")

    # Wykres punktowy ZBIÓR UCZĄCEGO
    visualize(df=df_train, x="date", y=y_feature, title=title + "\n{Zbiór UCZĄCY}", regression=False)

    # Wykres punktowy z regresją liniową ZBIÓR UCZĄCEGO
    visualize(df=df_train, x="date", y=y_feature, title=title + " & " + "Regresja" + "\n{Zbiór UCZĄCY}",
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
    visualize_plot_scatter(x_plot=x_dates, y_plot=y, x_scatter=df_train["date"], y_scatter=y_train,
                           title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")

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
    visualize_plot_scatter(x_plot=x_test_dates, y_plot=df_prediction["y_pred"], x_scatter=x_test_dates, y_scatter=y_test,
                           title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green")

def main():
    data = getData()
    # for i in data.cases:
    #     print(i.date)

    # make_experiment_prediction(data)
    # test(data)
    nowy2(data)


if __name__ == '__main__':
    main()
