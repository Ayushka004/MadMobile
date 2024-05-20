import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
import csv
import os
import time
import matplotlib.pyplot as plt

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
def send_email(subject, body, attachment):
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
    msg.attach(MIMEText(body, 'html'))

    # Attach graph image
    with open(attachment, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
        msg.attach(img)

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

# Main function
def main():
    while True:
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

        # Send weekly summary email
        if now.weekday() == 6:  # Sunday (0-indexed)
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                cpu_data = []
                ram_data = []
                network_up_data = []
                network_down_data = []
                disk_data = []
                for row in reader:
                    cpu_data.append(float(row[1]))
                    ram_data.append(float(row[2]))
                    network_up_data.append(float(row[3]))
                    network_down_data.append(float(row[4]))
                    disk_data.append(float(row[5]))
            
            cpu_high, cpu_low, cpu_avg = calculate_statistics(cpu_data)
            ram_high, ram_low, ram_avg = calculate_statistics(ram_data)
            network_up_high, network_up_low, network_up_avg = calculate_statistics(network_up_data)
            network_down_high, network_down_low, network_down_avg = calculate_statistics(network_down_data)
            disk_high, disk_low, disk_avg = calculate_statistics(disk_data)

            # Create a line graph of averages
            metrics = ['CPU', 'RAM', 'Network Up', 'Network Down', 'Disk']
            averages = [cpu_avg, ram_avg, network_up_avg, network_down_avg, disk_avg]
            plt.figure(figsize=(10, 6))
            plt.plot(metrics, averages, marker='o')
            plt.xlabel('Metrics')
            plt.ylabel('Average (%)')
            plt.title('Average System Metrics')
            plt.grid(True)
            plt.savefig('metrics_graph.png')
            plt.close()

            # Prepare HTML content for email
            subject = "AWS Weekly System Stats Summary"
            body = f"""\
            <html>
            <body>
                <h2>Weekly System Stats Summary:</h2>
                <table border="1" cellspacing="0" cellpadding="10">
                    <tr>
                        <th>Metric</th>
                        <th>High</th>
                        <th>Low</th>
                        <th>Average</th>
                    </tr>
                    <tr>
                        <td>CPU Usage</td>
                        <td>{cpu_high}%</td>
                        <td>{cpu_low}%</td>
                        <td>{cpu_avg}%</td>
                    </tr>
                    <tr>
                        <td>RAM Usage</td>
                        <td>{ram_high}%</td>
                        <td>{ram_low}%</td>
                        <td>{ram_avg}%</td>
                    </tr>
                    <tr>
                        <td>Network Usage (Up)</td>
                        <td>{network_up_high} bytes</td>
                        <td>{network_up_low} bytes</td>
                        <td>{network_up_avg} bytes</td>
                    </tr>
                    <tr>
                        <td>Network Usage (Down)</td>
                        <td>{network_down_high} bytes</td>
                        <td>{network_down_low} bytes</td>
                        <td>{network_down_avg} bytes</td>
                    </tr>
                    <tr>
                        <td>Disk Usage</td>
                        <td>{disk_high}%</td>
                        <td>{disk_low}%</td>
                        <td>{disk_avg}%</td>
                    </tr>
                </table>
                <br>
                <img src="cid:metrics_graph.png" alt="Average Metrics Graph">
            </body>
            </html>
            """

            # Send email with HTML content and graph attachment
            send_email(subject, body, 'metrics_graph.png')

            # Delete CSV file after sending email
            os.remove(filename)

        # Wait for 60 seconds before running again
        time.sleep(60)

if __name__ == "__main__":
    main()
