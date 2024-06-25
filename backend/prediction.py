import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime


def prepare_data(cases, data_type='total'):
    '''Prepare data for training and prediction'''
    dates = sorted(cases.keys())
    X = np.array([datetime.datetime.strptime(date, '%Y-%m-%d').toordinal() for date in dates]).reshape(-1, 1)
    y = np.array([cases[date][data_type] for date in dates])
    return X, y


def make_prediction(filtered_data, prediction_to):
    '''Create predictions using linear regression for total and new cases'''
    train_data = filtered_data[0]['cases']

    X_train_total, y_train_total = prepare_data(train_data, 'total')
    X_train_new, y_train_new = prepare_data(train_data, 'new')

    # Train the model for total cases
    model_total = LinearRegression()
    model_total.fit(X_train_total, y_train_total)

    # Train the model for new cases
    model_new = LinearRegression()
    model_new.fit(X_train_new, y_train_new)

    # Define prediction range
    prediction_end_date = datetime.datetime.strptime(prediction_to, '%d-%m-%Y').toordinal()

    X_pred_total = np.arange(max(X_train_total), prediction_end_date + 1).reshape(-1, 1)
    y_pred_total = model_total.predict(X_pred_total)

    X_pred_new = np.arange(max(X_train_new), prediction_end_date + 1).reshape(-1, 1)
    y_pred_new = model_new.predict(X_pred_new)

    # Prepare plots for total cases
    plot_model_prediction(X_train_total, y_train_total, model_total, X_pred_total, y_pred_total,
                          'MODEL PREDYKCJI covidowe przypadki & regresja (Total)')
    plot_prediction(X_train_total, y_train_total, X_pred_total, y_pred_total,
                    'predykcja covidowe przypadki & regresja (Total)')
    plot_training_data(X_train_total, y_train_total, 'covidowe przypadki {zbiór UCZĄCY} (Total)')
    plot_training_with_regression(X_train_total, y_train_total, model_total,
                                  'covidowe przypadki & regresja {zbiór uczący} (Total)')

    # Prepare plots for new cases
    plot_model_prediction_new(X_train_new, y_train_new, model_new, X_pred_new, y_pred_new,
                              'MODEL PREDYKCJI covidowe przypadki & regresja (New)')
    plot_prediction_new(X_train_new, y_train_new, X_pred_new, y_pred_new,
                        'predykcja covidowe przypadki & regresja (New)')
    plot_training_data_new(X_train_new, y_train_new, 'covidowe przypadki {zbiór UCZĄCY} (New)')
    plot_training_with_regression_new(X_train_new, y_train_new, model_new,
                                      'covidowe przypadki & regresja {zbiór uczący} (New)')

    return [model_prediction_chart, prediction_chart, training_data_chart, training_with_regression_chart,
            model_prediction_chart_new, prediction_chart_new, training_data_chart_new,
            training_with_regression_chart_new]


def plot_model_prediction(X_train, y_train, model, X_pred, y_pred, title):
    '''Plot model prediction for total cases'''
    global model_prediction_chart
    plt.figure()
    plt.scatter(X_train, y_train, color='blue', label='Training data')
    plt.plot(X_pred, y_pred, color='red', label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('Total cases')
    plt.title(title)
    plt.legend()
    model_prediction_chart = plt.gcf()
    plt.close()


def plot_prediction(X_train, y_train, X_pred, y_pred, title):
    '''Plot prediction for total cases'''
    global prediction_chart
    plt.figure()
    plt.plot(X_pred, y_pred, color='red', label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('Total cases')
    plt.title(title)
    plt.legend()
    prediction_chart = plt.gcf()
    plt.close()


def plot_training_data(X_train, y_train, title):
    '''Plot training data for total cases'''
    global training_data_chart
    plt.figure()
    plt.scatter(X_train, y_train, color='blue', label='Training data')
    plt.xlabel('Date')
    plt.ylabel('Total cases')
    plt.title(title)
    plt.legend()
    training_data_chart = plt.gcf()
    plt.close()


def plot_training_with_regression(X_train, y_train, model, title):
    '''Plot training data with regression for total cases'''
    global training_with_regression_chart
    plt.figure()
    plt.scatter(X_train, y_train, color='blue', label='Training data')
    plt.plot(X_train, model.predict(X_train), color='red', label='Regression line')
    plt.xlabel('Date')
    plt.ylabel('Total cases')
    plt.title(title)
    plt.legend()
    training_with_regression_chart = plt.gcf()
    plt.close()


def plot_model_prediction_new(X_train, y_train, model, X_pred, y_pred, title):
    '''Plot model prediction for new cases'''
    global model_prediction_chart_new
    plt.figure()
    plt.scatter(X_train, y_train, color='blue', label='Training data')
    plt.plot(X_pred, y_pred, color='red', label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('New cases')
    plt.title(title)
    plt.legend()
    model_prediction_chart_new = plt.gcf()
    plt.close()


def plot_prediction_new(X_train, y_train, X_pred, y_pred, title):
    '''Plot prediction for new cases'''
    global prediction_chart_new
    plt.figure()
    plt.plot(X_pred, y_pred, color='red', label='Prediction')
    plt.xlabel('Date')
    plt.ylabel('New cases')
    plt.title(title)
    plt.legend()
    prediction_chart_new = plt.gcf()
    plt.close()


def plot_training_data_new(X_train, y_train, title):
    '''Plot training data for new cases'''
    global training_data_chart_new
    plt.figure()
    plt.scatter(X_train, y_train, color='blue', label='Training data')
    plt.xlabel('Date')
    plt.ylabel('New cases')
    plt.title(title)
    plt.legend()
    training_data_chart_new = plt.gcf()
    plt.close()


def plot_training_with_regression_new(X_train, y_train, model, title):
    '''Plot training data with regression for new cases'''
    global training_with_regression_chart_new
    plt.figure()
    plt.scatter(X_train, y_train, color='blue', label='Training data')
    plt.plot(X_train, model.predict(X_train), color='red', label='Regression line')
    plt.xlabel('Date')
    plt.ylabel('New cases')
    plt.title(title)
    plt.legend()
    training_with_regression_chart_new = plt.gcf()
    plt.close()
