import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def plot_country_chart(data, country, type):
    cases = data[0]['cases']
    dates = list(cases.keys())
    values = [details[type] for date, details in cases.items()]

    dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(dates, values, label=type)
    ax.set_title(f'{type.capitalize()} Cases for {country}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Cases')
    ax.legend()

    num_days = (dates[-1] - dates[0]).days

    if num_days > 365:
        locator = mdates.MonthLocator(interval=3)
    elif num_days > 90:
        locator = mdates.MonthLocator(interval=1)
    elif num_days > 30:
        locator = mdates.WeekLocator()
    else:
        locator = mdates.DayLocator(interval=1)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
