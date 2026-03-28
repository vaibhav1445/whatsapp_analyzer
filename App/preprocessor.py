import re
import pandas as pd

def preprocess(data):
    # Pattern 1: [dd/mm/yy, hh:mm:ss AM/PM] (square brackets with seconds)
    pattern1 = r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM|am|pm))\]\s'
    
    # Pattern 2: dd/mm/yy, hh:mm AM/PM - (no brackets, no seconds, with am/pm)
    pattern2 = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm)\s-\s)'
    
    # Pattern 3: dd/mm/yyyy, HH:MM - (no brackets, no seconds, 24 hour)
    pattern3 = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s)'

    # Pattern 4: [dd/mm/yy, hh:mm:ss] (square brackets, no AM/PM)
    pattern4 = r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2})\]\s'

    # Detect which pattern matches
    def detect_pattern(data):
        if re.search(r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM|am|pm)\]', data):
            return pattern1, 'bracket_ampm_seconds'
        elif re.search(r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]', data):
            return pattern4, 'bracket_24h_seconds'
        elif re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM|am|pm)\s-', data):
            return pattern2, 'no_bracket_ampm'
        elif re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-', data):
            return pattern3, 'no_bracket_24h'
        return None, None

    pattern, fmt_type = detect_pattern(data)

    if pattern is None:
        return pd.DataFrame()

    # Extract dates and messages based on pattern type
    if fmt_type in ('bracket_ampm_seconds', 'bracket_24h_seconds'):
        dates = re.findall(pattern, data)
        messages = re.split(pattern, data)[2::2]
    else:
        dates = re.findall(pattern, data)
        dates = [d.strip() for d in dates]
        messages = re.split(pattern, data)[2::2]

    if not messages or not dates or len(messages) != len(dates):
        return pd.DataFrame()

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # All possible date formats
    def parse_date(date_str):
        date_str = date_str.strip().rstrip('-').strip()
        formats = [
            # 12-hour with seconds
            '%d/%m/%y, %I:%M:%S %p',
            '%d/%m/%Y, %I:%M:%S %p',
            '%m/%d/%y, %I:%M:%S %p',
            '%m/%d/%Y, %I:%M:%S %p',
            # 24-hour with seconds
            '%d/%m/%y, %H:%M:%S',
            '%d/%m/%Y, %H:%M:%S',
            '%m/%d/%y, %H:%M:%S',
            '%m/%d/%Y, %H:%M:%S',
            # 12-hour without seconds
            '%d/%m/%y, %I:%M %p',
            '%d/%m/%Y, %I:%M %p',
            '%m/%d/%y, %I:%M %p',
            '%m/%d/%Y, %I:%M %p',
            # 24-hour without seconds
            '%d/%m/%y, %H:%M',
            '%d/%m/%Y, %H:%M',
            '%m/%d/%y, %H:%M',
            '%m/%d/%Y, %H:%M',
        ]
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        return pd.NaT

    df['date'] = df['message_date'].apply(parse_date)
    df.drop(columns=['message_date'], inplace=True)
    df = df.dropna(subset=['date'])

    if df.empty:
        return pd.DataFrame()

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