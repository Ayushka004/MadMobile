# L2 Technical support agent

# System Monitoring and Data Flow Using AWS

This repository contains scripts and configurations to set up system monitoring, data collection, and data flow using AWS services.

## Overview

The system setup involves monitoring critical stats of an EC2 instance, collecting data using a Python script, uploading JSON files to an S3 bucket, and storing data in DynamoDB. Additionally, it includes setting thresholds, sending notifications.

![Data Flow](images/Stats.png)

## Enterprise Architecture Diagram 
![System Overview](images/Enterprise%20Architecture%20Diagram%20.png)

--------------------------------------


## 1. monitor the Utilization of 5 Critical Environment/Host Stats in a EC2/Physical Unix Setup.
### Requirments
1. Launch a EC2 instance with Python and aws-cloud-watch installed.
2. Ensure the instance has necessary permissions for S3 and DynamoDB access.

### Step to take


-----------------------------------------

## Set Thresholds to Each of these 5 Critical stats at 60% - Amber and 80% Red
### Requirments
1. 

## 2. Setup a mechanism for each of the Critical Stat thresholds to be tested and upon each violation of the threshold an email to be sent out
### Requirments
1. Launch a EC2 instance with Python and aws-cloud-watch installed.
2. Ensure the instance has necessary permissions for S3 and DynamoDB access.

### Step to take

-----------------------------------------

## 3. Record the 5 Key stats every minute and record the data in a JSON Type Document which can be fed into a database
### Requirments
1. Write a Python script to collect system stats and upload JSON files to S3 
2. at the same time add them to a log folder and every 7 days remove them.
3. Use Boto3 to interact with AWS services in the script.
4. Collect logs in json and send it to the s3 bucket

### Step to take
1. Using SSH connect to the terminal 
2. Install the following dependencies
```
    pip3 install psutil
```
```
    pip3 install boto3
```
```
    pip3 install pytz
```

3. download the following Python script.
   
   <a href="/Python Scripts/Logs V2.py"> logsV2.py <a>
   

4. On the EC2 terminal create a new file in the root
    ``` Touch monitor.py ```
    
5. Edit the file and add the content from the logsV2py file using the following command 
    ```
    Vim monitor.py
    ```
    
6. Save and exit (press button esc and)
    ```
    :wq
    ```
    

7. Run the following command to make the app run indefinitely on the background
    ```
    nohup python monitor.py &
    ```

-----------------------------------------

## Send a Weekly Summary email to an email address with Weekly High, low and Average values in a tabular format.
### Requirments
1. Write a Python script to collect system stats and upload JSON files to S3 
2. at the same time add them to a log folder and every 7 days remove them.
3. Use Boto3 to interact with AWS services in the script.
4. Collect logs in json and send it to the s3 bucket

***Will be completed in a future iteration
-----------------------------------------

## Implement Error Logging to the Solution where any errors will be managed and notified to various stakeholders
### Requirments
1. Write a Python script to collect system stats and upload JSON files to S3 
2. at the same time add them to a log folder and every 7 days remove them.
3. Use Boto3 to interact with AWS services in the script.
4. Collect logs in json and send it to the s3 bucket

***Will be completed in a future iteration
-----------------------------------------