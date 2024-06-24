import datetime
import warnings
import numpy as np
from backend.predictive import *


def make_predicition(data):
    """Funkcja przeprowadzająca eksperyment predykcji."""
    warnings.filterwarnings("ignore")

    drow = []

    cases = data[0]['cases']
    for date, case_info in cases.items():
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        drow.append((date_obj, date_obj.timestamp(), case_info['total']))
    df = pd.DataFrame(drow, columns=["date", "timestamp", "total"])

    max_total = df['total'].max()
    if max_total > 1e9:
        df['total'] = df['total'] / 1e9
        ylabel = "nowe przypadki (w mld)"
    elif max_total > 1e6:
        df['total'] = df['total'] / 1e6
        ylabel = "nowe przypadki (w mln)"
    else:
        ylabel = "nowe przypadki"

    x_feature = "timestamp"
    y_feature = "total"
    xlabel = "data"
    title = "covidowe przypadki"


    df_train = df[pd.to_datetime(df.date) < pd.to_datetime("2022-01-01")]
    df_test = df[pd.to_datetime(df.date) >= pd.to_datetime("2022-01-01")]

    visualize3 = visualize(df=df_train, x="date", y=y_feature, title=title + "\n{Zbiór UCZĄCY}", regression=False)
    visualize4 = visualize(df=df_train, x="date", y=y_feature,
                           title=title + " & " + "Regresja" + "\n{Zbiór UCZĄCY}",
                           regression=True)

    x_train = np.array(df_train[x_feature]).reshape((-1, 1))
    y_train = np.array(df_train[y_feature])
    model, _ = predictor(x_train, y_train)

    x = np.linspace(np.min(x_train), np.max(x_train), 5000).flatten()
    y = model.coef_ * x + model.intercept_
    x_dates = [datetime.datetime.fromtimestamp(ts) for ts in x]
    chart_title = "MODEL PREDYKCJI\n" + title + " & " + "Regresja"
    visualize_plot_scatter2 = visualize_plot_scatter(
        x_plot=x_dates, y_plot=y, x_scatter=df_train["date"], y_scatter=y_train,
        title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green"
    )

    x_test = np.array(df_test[x_feature]).reshape((-1, 1))
    y_test = np.array(df_test[y_feature])
    df_prediction, _ = prediction(model, x_test, y_test)

    x_test_dates = df_test["date"]
    chart_title = "PREDYKCJA\n" + title + " & " + "Regresja"
    visualize_plot_scatter3 = visualize_plot_scatter(
        x_plot=x_test_dates, y_plot=df_prediction["y_pred"], x_scatter=x_test_dates,
        y_scatter=y_test,
        title=chart_title, xlabel=xlabel, ylabel=ylabel, plot_color="orange", scatter_color="green"
    )

    return [visualize_plot_scatter2, visualize_plot_scatter3, visualize3, visualize4]
