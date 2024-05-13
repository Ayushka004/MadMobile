# L2 Technical support agent

# System Monitoring and Data Flow Using AWS

This repository contains scripts and configurations to set up system monitoring, data collection, and data flow using AWS services.

## Overview

The system setup involves monitoring critical stats of an EC2 instance, collecting data using a Python script, uploading JSON files to an S3 bucket, and storing data in DynamoDB. Additionally, it includes setting thresholds, sending notifications.

![Data Flow](images/Stats.png)

![System Overview](images/system_overview.png)


## monitor the Utilization of 5 Critical Environment/Host Stats in a 3 EC2/Physical Unix Setup.
## Set Thresholds to Each of these 5 Critical stats at 60% - Amber and 80% Red
## Setup a mechanism for each of the Critical Stat thresholds to be tested and upon each violation of the threshold an email to be sent out
## Record the 5 Key stats every minute and record the data in a JSON Type Document which can be fed into a database
## Send a Weekly Summary email to an email address with Weekly High, low and Average values in a tabular format.
## Implement Error Logging to the Solution where any errors will be managed and notified to various stakeholders
##
##

Requirments
1. Launch 3 EC2 instance with Python and aws-cloud-watch installed.
2. Ensure the instance has necessary permissions for S3 and DynamoDB access.



### Step 2: Python Script and S3 Upload
1. Write a Python script to collect system stats and upload JSON files to S3.
2. Use Boto3 to interact with AWS services in the script.
3. Collect logs in json and send it to the s3 bucket

4. Using SSH connect to the terminal 
5. Install the following dependencies
```
    pip3 install psutil
```
```
    pip3 install boto3
```
```
    pip3 install pytz
```

7. download the following Python script.
   
   <a href="/Python Scripts/Logs V2.py"> logsV2.py <a>
   

9. On the EC2 terminal create a new file in the root
    ```
    Touch monitor.py
    ```
    
11. Edit the file and add the content from the logsV2py file using the following command 
    ```
    Vim monitor.py
    ```
    
12. Save and exit (press button esc and)
    ```
    :wq
    ```
    

14. Run the following command to make the app run indefinitely on the background
    ```
    nohup python monitor.py &
    ```

### Step 3: S3 Event Trigger and Lambda Function
1. Set up an S3 event trigger to invoke a Lambda function on file upload.
2. Create a Lambda function to read JSON files from S3 and store data in DynamoDB.

![Data Flow](images/image.png)

### Step 4: Thresholds, Alarms, and Notifications
1. Configure CloudWatch alarms for critical stats with thresholds.
2. Set actions for alarms to trigger Lambda functions for email notifications.

### Step 5: Weekly Summary Email
1. Create a Lambda function to calculate weekly high, low, and average values.
2. Use SES to send a weekly summary email with the calculated data.

### Step 6: Error Logging and Handling
1. Utilize CloudWatch Logs to capture errors from Lambda functions.
2. Set up alarms for critical errors and handle them appropriately.

![Error Handling](images/error_handling.png)

### Step 7: Configuration Flexibility
1. Store configurable parameters in AWS Parameter Store or Secrets Manager.
2. Ensure easy updates without code changes for thresholds, email addresses, etc.



## Credits
