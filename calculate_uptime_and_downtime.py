import pandas as pd
from datetime import datetime, timedelta

store_status_csv = "/Users/gauravkumar/store status.csv"

business_hours_csv = "/Users/gauravkumar/Downloads/Menu hours.csv"

store_timezone_csv = "/Users/gauravkumar/Downloads/bq-results-20230125-202210-1674678181880.csv"

store_status_df = pd.read_csv(store_status_csv)

business_hours_df = pd.read_csv(business_hours_csv)

store_timezone_df = pd.read_csv(store_timezone_csv)

def calculate_downtime_and_uptime(store_id):
    store_data = store_status_df[store_status_df['store_id'] == store_id]
    business_hours_data = business_hours_df[business_hours_df['store_id'] == store_id]

    store_timezone = store_timezone_df[store_timezone_df['store_id'] == store_id]['timezone_str'].values[0]

    uptime_minutes = 0
    downtime_minutes = 0

    for _, business_hours_row in business_hours_data.iterrows():
        day_of_week = business_hours_row['day']
        start_time_local = business_hours_row['start_time_local']
        end_time_local = business_hours_row['end_time_local']

        store_data['timestamp_utc'] = pd.to_datetime(store_data['timestamp_utc'])
        max_timestamp_utc = store_data['timestamp_utc'].max()
        print(store_data['timestamp_utc'])
        store_data_day = store_data[store_data['timestamp_utc'].dt.dayofweek == day_of_week]

        current_time = datetime.strptime(start_time_local, '%H:%M:%S')
        end_time = datetime.strptime(end_time_local, '%H:%M:%S')
        
        while current_time <= end_time:
            if current_time.time() >= max_timestamp_utc.time():
                is_active = store_data_day['status'].eq('active').sum() > 0

                if is_active:
                    uptime_minutes += 1
                else:
                    downtime_minutes += 1

            # Increment current time by 1 minute
            current_time += timedelta(minutes=1)

    return {
        'store_id': store_id,
        'uptime_last_hour': uptime_minutes,
        'uptime_last_day': uptime_minutes / 60,
        'update_last_week': uptime_minutes / 60 / 24 * 7,
        'downtime_last_hour': downtime_minutes,
        'downtime_last_day': downtime_minutes / 60,
        'downtime_last_week': downtime_minutes / 60 / 24 * 7
    }

if __name__ == "__main__":
    store_id = 54515546588432327

    report = calculate_downtime_and_uptime(store_id)
    
    print(report)
