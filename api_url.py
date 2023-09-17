import random
import string
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_csv

app = Flask(__name__)

store_status_csv = "/Users/gauravkumar/store status.csv"

business_hours_csv = "/Users/gauravkumar/Downloads/Menu hours.csv"

store_timezone_csv = "/Users/gauravkumar/Downloads/bq-results-20230125-202210-1674678181880.csv"

store_status_df = pd.read_csv(store_status_csv)

business_hours_df = pd.read_csv(business_hours_csv)

store_timezone_df = pd.read_csv(store_timezone_csv)

reports = {}

def calculate_downtime_and_uptime(store_id, current_timestamp):
   
    return {
        'store_id': store_id,
        'uptime_last_hour': uptime_minutes,
        'uptime_last_day': uptime_minutes / 60,
        'update_last_week': uptime_minutes / 60 / 24 * 7,
        'downtime_last_hour': downtime_minutes,
        'downtime_last_day': downtime_minutes / 60,
        'downtime_last_week': downtime_minutes / 60 / 24 * 7
    }

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    report_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    max_timestamp_utc = store_status_df['timestamp_utc'].max()

    for store_id in store_status_df['store_id'].unique():
        report_data = calculate_downtime_and_uptime(store_id, max_timestamp_utc)
        reports[report_id] = report_data

    return jsonify({'report_id': report_id})

@app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')
    report_data = reports.get(report_id)

    if not report_data:
        return jsonify({'status': 'Report not found'}), 404

    if 'csv' in request.args:
        df = pd.DataFrame([report_data])
        csv_data = df.to_csv(index=False)
        return send_csv(csv_data, mimetype='text/csv', as_attachment=True, attachment_filename='report.csv')

    if 'status' in request.args:
        if request.args['status'] == 'complete':
            return jsonify({'status': 'Complete'})
        elif request.args['status'] == 'running':
            return jsonify({'status': 'Running'})

    return jsonify({'status': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(debug=True)
