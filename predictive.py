
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def visualize_plot_scatter(x_plot: object, y_plot: object, x_scatter: object, y_scatter: object,
                           title=None, xlabel="x", ylabel="y", plot_color=None, scatter_color=None):
    """Tworzenie wykresów."""

    plt.figure(figsize=(15, 10))
    if x_plot is not None and y_plot is not None:
        plt.plot(x_plot, y_plot, color=plot_color, linewidth=1)
    if x_scatter is not None and y_scatter is not None:
        plt.scatter(x=x_scatter, y=y_scatter, color=scatter_color, marker="o")
    plt.xlabel(xlabel, fontsize="10", horizontalalignment="center")
    plt.ylabel(ylabel, fontsize="10", horizontalalignment="center")
    plt.title(title)
    plt.show()


def visualize(df, title, x, y, regression=False, grouping=None):
    # """Tworzenie wykresów.
    #    Parametr df to dane w formie ramki danych."""
    #
    # colors = ["blue", "orange", "red", "green", "magenta", "grey", "yellow",
    #           "black", "purple", "navy", "pink", "cyan", "white"]
    #
    # lm = sns.lmplot(x=x, y=y, data=df, fit_reg=regression, legend=True, height=10, aspect=1.55, hue=grouping,
    #                 palette=colors)
    # figure = lm.figure
    # figure.suptitle(title)
    """Tworzenie wykresów.
          Parametr df to dane w formie ramki danych."""

    colors = ["blue", "orange", "red", "green", "magenta", "grey", "yellow",
              "black", "purple", "navy", "pink", "cyan", "white"]

    # if regression:
    #     lm = sns.lmplot(x=x, y=y, data=df, fit_reg=True, legend=True, height=10, aspect=1.55, hue=grouping,
    #                     palette=colors)
    #     figure = lm.fig
    #     figure.suptitle(title)
    # else:
    plt.figure(figsize=(15, 10))
    plt.scatter(x=df[x], y=df[y], color=colors[0], marker="o")
    plt.xlabel(x, fontsize="10", horizontalalignment="center")
    plt.ylabel(y, fontsize="10", horizontalalignment="center")
    plt.title(title)
    plt.show()



def prediction(model, x_test, y_test):
    """Predykcja z wykorzystaniem REGRESJI LINIOWEJ"""

    # Predykcja
    y_pred = model.predict(x_test)
    df_prediction = pd.DataFrame({"x_test": x_test.ravel(), "y_test": y_test.ravel(), "y_pred": y_pred.ravel()})

    # Ocena [modelu] predykcji
    # mse = mean_squared_error(y_test, y_pred)
    # r_square_predict = r2_score(y_test, y_pred)
    # r_square_test = model.score(x_test, y_test)

    values = [["Metoda", model.__class__.__name__.upper()],
              ["Błąd średniokwadratowy (MSE):", mean_squared_error(y_test, y_pred)],
              ["Współczynnik determinacji (r^2) 'P':", r2_score(y_test, y_pred)],
              ["Współczynnik determinacji (r^2) 'T'':", model.score(x_test, y_test)]]
    description = pd.DataFrame(data=values, columns=["", ""])

    return df_prediction, description


def predictor(x_train, y_train):
    """Model predykcji tj. predyktor z wykorzystaniem REGRESJI LINIOWEJ"""

    # Utworzenie modelu predykcji tj. predyktora z wykorzystaniem REGRESJI LINIOWEJ
    model = linear_model.LinearRegression()
    model.fit(x_train, y_train)

    # Parametry modelu predykcji
    # r_square = model.score(x_train, y_train)
    # slope = model.coef_
    # intercept = model.intercept_

    values = [["Metoda", model.__class__.__name__.upper()],
              ["Współczynnik determinacji (r^2):", model.score(x_train, y_train)],
              ["Współczynnik a (slope):", model.coef_],
              ["Współczynnik b (intercept):", model.intercept_]]
    description = pd.DataFrame(data=values, columns=["", ""])

    return model, description