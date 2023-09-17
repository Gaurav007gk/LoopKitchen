from datetime import datetime, timedelta
import pytz

def convert_to_timezone(timestamp, timezone_str):
    try:
        
        dt = datetime.fromisoformat(timestamp)

       
        source_timezone = pytz.timezone(timezone_str)

        dt_utc = source_timezone.localize(dt).astimezone(pytz.UTC)

        return dt_utc
    except Exception as e:
        raise Exception("Error converting timestamp to timezone: " + str(e))


def is_business_hours(timestamp, business_hours):
    try:
       
        dt = datetime.fromisoformat(timestamp).time()

        return business_hours[0] <= dt <= business_hours[1]
    except Exception as e:
        raise Exception("Error checking business hours: " + str(e))

def calculate_metrics(store_data, business_hours):
    uptime_last_hour = downtime_last_hour = 0
    uptime_last_day = downtime_last_day = 0
    uptime_last_week = downtime_last_week = 0

    current_timestamp = '2023-09-17T15:00:00Z'

    last_hour_interval = timedelta(hours=1)
    last_day_interval = timedelta(days=1)
    last_week_interval = timedelta(weeks=1)

    for entry in store_data:
        timestamp = entry['timestamp_utc']
        status = entry['status']

        store_timezone = entry['timezone_str']
        timestamp_utc = convert_to_timezone(timestamp, store_timezone)

        if is_business_hours(timestamp_utc, business_hours):
            if timestamp_utc >= (current_timestamp - last_hour_interval):
                if status == 'active':
                    uptime_last_hour += 1
                else:
                    downtime_last_hour += 1

            if timestamp_utc >= (current_timestamp - last_day_interval):
                if status == 'active':
                    uptime_last_day += 1
                else:
                    downtime_last_day += 1

            if timestamp_utc >= (current_timestamp - last_week_interval):
                if status == 'active':
                    uptime_last_week += 1
                else:
                    downtime_last_week += 1

    return {
        'uptime_last_hour': uptime_last_hour,
        'uptime_last_day': uptime_last_day,
        'uptime_last_week': uptime_last_week,
        'downtime_last_hour': downtime_last_hour,
        'downtime_last_day': downtime_last_day,
        'downtime_last_week': downtime_last_week
    }    