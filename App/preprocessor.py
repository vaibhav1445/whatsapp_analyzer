import re
import pandas as pd

def preprocess(data):
    # Pattern with square brackets, seconds, and AM/PM
    pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM|am|pm))\]\s'
    
    messages = re.split(pattern, data)[::2][1:]  # Extract messages
    dates = re.findall(pattern, data)             # Extract dates

    if not messages or not dates:
        return pd.DataFrame()

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    def parse_date(date_str):
        formats = [
            '%d/%m/%y, %I:%M:%S %p',
            '%d/%m/%Y, %I:%M:%S %p',
            '%m/%d/%y, %I:%M:%S %p',
            '%m/%d/%Y, %I:%M:%S %p',
        ]
        for fmt in formats:
            try:
                return pd.to_datetime(date_str.strip(), format=fmt)
            except:
                continue
        return pd.NaT

    df['date'] = df['message_date'].apply(parse_date)
    df.drop(columns=['message_date'], inplace=True)
    df = df.dropna(subset=['date'])

    users = []
    messages_list = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df