from datetime import date, timedelta
from datetime import datetime as dt


def get_date_from_timestamp(timestamp):
    if not timestamp:
        return ''
    return dt.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def get_time_from_timestamp(start_ts):
    if not start_ts:
        return ''
    return dt.fromtimestamp(start_ts).strftime("%H:%M:%S")


def get_default_date(timestamp):
    if not timestamp:
        return ''
    return dt.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def time_delta_formatting(t_date):
    return f"{t_date.year}-{t_date.month}-{t_date.day}"


def get_today():
    return time_delta_formatting(date.today())


def get_yesterday_date():
    return time_delta_formatting(date.today() - timedelta(days=1))


def get_tomorrow_date():
    return time_delta_formatting(date.today() + timedelta(days=1))


def convert_time_12h_to_24h(str_time, input_time_format='%I:%M %p'):
    try:
        return dt.strptime(str_time, input_time_format).strftime("%H:%M:%S")
    except Exception as dt_err:
        print(dt_err)
        return str_time


def convert_date_to_mysql_format(str_date, input_date_formats=['%B %d, %Y', '%d-%m-%Y', '%m-%d-%Y', "%b %d, %Y"]):
    for date_format in input_date_formats:
        try:
            d = dt.strptime(str_date, date_format).strftime("%Y-%m-%d")
            return d
        except Exception as dt_err:
            pass

    return str_date
