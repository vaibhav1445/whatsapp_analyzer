import re
import pandas as pd


# Define the preprocess function
def preprocess(data):
    # Pattern to match date and time in the chat format
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} - '

    # Extract messages and dates using regex
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame with the extracted data
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    # Define a safe conversion function
    def safe_convert_date(date_str):
        try:
            # Attempt conversion to datetime
            return pd.to_datetime(date_str, format='%d/%m/%Y, %H:%M -', errors='raise')
        except Exception:
            # If conversion fails, return NaT (or you can return the original string if preferred)
            return pd.NaT

    # Apply safe conversion to 'message_date'
    df['date'] = df['message_date'].apply(safe_convert_date)

    df.drop(columns=['message_date'], inplace=True)

    # Separate users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # If a user is detected
            users.append(entry[1])
            messages.append(entry[2])
        else:  # If it's a group notification or system message
            users.append('group_notification')
            messages.append(entry[0])

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    # Extract additional date and time details for non-NaT values
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
