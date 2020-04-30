import datetime


def get_dates(days_amount):
    now = datetime.datetime.now().date()
    past_date = now - datetime.timedelta(days=days_amount)

    while past_date.weekday() != 0:  # searching nearest monday
        past_date -= datetime.timedelta(days=1)

    next_monday = past_date + datetime.timedelta(days=7)
    while next_monday <= now:
        yield past_date.strftime('%m/%d/%y'), next_monday.strftime('%m/%d/%y')
        past_date = next_monday
        next_monday = past_date + datetime.timedelta(days=7)
