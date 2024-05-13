import boto3
import json
import psutil
import datetime
import time
import os
import pytz  # Import pytz for timezone information

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    # Collect other stats as needed
    # For application-specific metrics, use custom code or APIs
    return {
        'timestamp': str(datetime.datetime.now()),
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage_percent': psutil.disk_usage('/').percent,
        'network_bytes_sent': psutil.net_io_counters().bytes_sent,
        'network_bytes_recv': psutil.net_io_counters().bytes_recv
    }

def upload_to_s3(bucket_name, file_name, data):
    try:
        s3_client = boto3.client('s3', aws_access_key_id='<<Your aws ID here>>', aws_secret_access_key='<<Your Secret key here>>')
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))
        print(f"Uploaded {file_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def save_local_log(file_name, data):
    log_folder = 'logs'
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    with open(f'{log_folder}/{file_name}', 'a') as file:
        file.write(json.dumps(data) + '\n')


def main():
    bucket_name = 'demomad1'
    logs = []
    while True:
        current_time = datetime.datetime.now()
        timezone = pytz.timezone('Asia/Kolkata')  # To gte IST time
        current_time_tz = timezone.localize(current_time)
        formatted_date = current_time_tz.strftime("%Y-%m-%d_%H-%M_%Z")
        file_name = f'stats_{formatted_date}.json'

        stats_data = get_system_stats()
        save_local_log(f'stats_{formatted_date}.log', stats_data)  # Save each log locally
        logs.append(stats_data)
        upload_to_s3(bucket_name, file_name, stats_data)
        time.sleep(60)  # Wait for 60 seconds (1 minute) before collecting stats again

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
