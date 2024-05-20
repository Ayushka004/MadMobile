import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import csv
import os
import schedule
import time

# Function to get system resource usage
def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    network_usage = psutil.net_io_counters()
    network_up = network_usage.bytes_sent
    network_down = network_usage.bytes_recv
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, ram_usage, network_up, network_down, disk_usage

# Function to send email
def send_email(subject, body):
    # Configure SMTP server details
    smtp_server = 'your_smtp_server'
    smtp_port = 587
    sender_email = 'your_email@example.com'
    sender_password = 'your_email_password'
    receiver_email = 'receiver_email@example.com'

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to calculate statistics
def calculate_statistics(data):
    high = max(data)
    low = min(data)
    average = sum(data) / len(data)
    return high, low, average

# Function to schedule sending email
def schedule_email():
    schedule.every(5).minutes.do(send_email_task)

# Function to send email task
def send_email_task():
    # Get current date and time
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get system resource stats
    cpu_usage, ram_usage, network_up, network_down, disk_usage = get_system_stats()

    # Save stats to a CSV file
    filename = 'system_stats.csv'
    with open(filename, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([current_date, cpu_usage, ram_usage, network_up, network_down, disk_usage])

    # Send email
    subject = "System Stats Summary"
    body = f"""\
    System Stats Summary:

    CPU Usage: {cpu_usage}%
    RAM Usage: {ram_usage}%
    Network Up: {network_up} bytes
    Network Down: {network_down} bytes
    Disk Usage: {disk_usage}%
    """

    send_email(subject, body)

# Main function
def main():
    # Schedule email task every 5 minutes
    schedule_email()

    # Keep the script running to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
