import boto3
import json
import psutil
import datetime
import time
import pytz
import os
from uuid import uuid4

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    # Collect other stats as needed
    # For application-specific metrics, use custom code or APIs
    return {
        'ID': str(uuid4()),  # Generate a unique ID for each log line
        'timestamp': str(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))),  # Use IST timezone
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        # Add other stats here
    }

def save_local_log(file_name, data):
    log_folder = 'logs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    with open(f'{log_folder}/{file_name}', 'a') as file:
        file.write(json.dumps(data) + '\n')

def upload_to_s3(bucket_name, local_file, s3_file):
    s3_client = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')
    try:
        s3_client.upload_file(f'logs/{local_file}', bucket_name, s3_file)
        print(f"Uploaded {s3_file} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def main():
    bucket_name = 'demomad1'
    logs = []
    for _ in range(5):  # Collect stats every minute for 5 minutes
        stats_data = get_system_stats()

        current_time = datetime.datetime.now()
        timezone = pytz.timezone('Asia/Kolkata')  # To get IST time
        current_time_tz = timezone.localize(current_time)
        formatted_date = current_time_tz.strftime("%Y-%m-%d_%H-%M_%Z")

        save_local_log(f'stats_{formatted_date}.log', stats_data)  # Save each log locally
        logs.append(stats_data)
        time.sleep(60)  # Wait for 60 seconds (1 minute) before collecting stats again

    # Upload logs as a single JSON file to S3
    current_time = datetime.datetime.now()
    timezone = pytz.timezone('Asia/Kolkata')  # To get IST time
    current_time_tz = timezone.localize(current_time)
    formatted_date = current_time_tz.strftime("%Y-%m-%d_%H-%M_%Z")
    file_name = f'stats_{formatted_date}.log'
    upload_to_s3(bucket_name, file_name, file_name)

    # Delete local logs after 24 hours
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    for log_file in os.listdir('logs'):
        file_path = os.path.join('logs', log_file)
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        if creation_time < yesterday:
            os.remove(file_path)
            print(f"Deleted {log_file} from local storage")

if __name__ == "__main__":
    main()
