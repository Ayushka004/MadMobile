import boto3
import json
import psutil  # For system monitoring metrics (CPU, memory, disk, etc.)
import datetime
import time
import pytz  # Import pytz for timezone information


##Collect Stats and Format into JSON
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

s3_client = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')


def upload_to_s3(bucket_name, file_name, data):
    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(data))
        print(f"Uploaded {file_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")


def main():

    bucket_name = 'demomad1'
    file_name = 'stats_'+current_timestamp+'.json'
    while True:
        stats_data = get_system_stats()
        upload_to_s3(bucket_name, file_name, stats_data)
        time.sleep(60)  # Wait for 60 seconds (1 minute) before collecting stats again

if __name__ == "__main__":
    main()
