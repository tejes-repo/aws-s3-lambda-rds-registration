# AWS Lambda Backend Configuration

## Overview

AWS Lambda is used as the backend component of the Serverless Registration Application.

The Lambda function receives registration data from Amazon API Gateway, processes the request, connects to Amazon RDS MySQL using PyMySQL, and inserts the registration data into the `users` table.

## Lambda Function Details

```text
Function Name: regUser
Runtime: Python 3.12
Architecture: x86_64
Execution Role: reg-role
```

## Step 1: Create Lambda Function

Go to:

```text
AWS Console
→ Lambda
→ Functions
→ Create function
```

Select:

```text
Author from scratch
```

Configure:

```text
Function name:
regUser

Runtime:
Python 3.12

Architecture:
x86_64

Permissions:
Use existing role

Role:
reg-role
```

Click:

```text
Create function
```

## Step 2: Configure Environment Variables

Go to:

```text
Lambda
→ regUser
→ Configuration
→ Environment variables
→ Edit
```

Add:

```text
DB_HOST=your-rds-endpoint
DB_USER=admin
DB_PASSWORD=your-password
  =regdb
```

The database password should not be stored directly in the source code.

## Step 3: Install PyMySQL

The Lambda function uses PyMySQL to connect to the RDS MySQL database.

Create a local package directory:

```cmd
mkdir Lambda
cd Lambda
mkdir package
```

Install PyMySQL:

```cmd
pip install pymysql -t package
```

The dependency should be included with the Lambda deployment package.

> The dependency package must be compatible with the AWS Lambda runtime environment. Avoid uploading Windows-specific native libraries.

## Step 4: Lambda Source Code

The Lambda source file is:

```text
source/lambda/lambda_function.py
```

The main processing flow is:

```text
API Gateway Request
       |
       v
Lambda Function
       |
       v
Read JSON Request Body
       |
       v
Connect to RDS MySQL
       |
       v
INSERT registration data
       |
       v
Commit Transaction
       |
       v
Return HTTP Response
```

## Step 5: Database Connection

The Lambda function uses the following environment variables:

```python
connection = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"]
)
```

This keeps the database configuration separate from the application source code.

## Step 6: Insert Registration Data

The registration data is inserted into the `users` table.

Example SQL:

```sql
INSERT INTO users(name, email, password)
VALUES (%s, %s, %s);
```

The values are provided by the API request.

Example request body:

```json
{
  "name": "Kunal",
  "email": "kunal@test.com",
  "password": "123456"
}
```

## Step 7: CORS Response

The Lambda response includes CORS headers:

```python
headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "content-type",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
}
```

API Gateway CORS configuration is also required for browser-based requests.

## Step 8: Test Lambda

Create a Lambda test event using the HTTP API version 2.0 format.

Example:

```json
{
  "version": "2.0",
  "routeKey": "POST /register",
  "rawPath": "/register",
  "rawQueryString": "",
  "headers": {
    "content-type": "application/json"
  },
  "requestContext": {
    "http": {
      "method": "POST",
      "path": "/register"
    }
  },
  "body": "{\"name\":\"Kunal\",\"email\":\"kunal@test.com\",\"password\":\"123456\"}",
  "isBase64Encoded": false
}
```

Click:

```text
Test
```

Expected response:

```json
{
  "message": "User registered successfully"
}
```

## Step 9: Verify Database

After a successful Lambda test, connect to RDS MySQL using MySQL Workbench.

Run:

```sql
USE regdb;

SELECT * FROM users;
```

The newly registered user should be displayed.

## Lambda Integration

The Lambda function is integrated with API Gateway:

```text
Amazon API Gateway
        |
        | POST /register
        v
AWS Lambda
        |
        | PyMySQL
        v
Amazon RDS MySQL
```

## Troubleshooting

### Error: No module named 'pymysql'

Cause:

The PyMySQL dependency is not included correctly in the Lambda deployment package.

Solution:

```cmd
pip install pymysql -t package
```

Recreate the deployment package and upload it to Lambda.

### Error: Failed to fetch

If Lambda works from the AWS console but the S3 website cannot submit the form, check:

* API Gateway CORS configuration
* API Gateway route
* Frontend API URL
* `POST /register`
* `OPTIONS /register`
* Browser Network tab

## Security Best Practices

For production environments:

* Do not hard-code database credentials.
* Use AWS Secrets Manager or Systems Manager Parameter Store.
* Use least-privilege IAM permissions.
* Use a private RDS database.
* Restrict network access using security groups.
* Do not store real passwords in GitHub.
* Enable CloudWatch logging and monitoring.

## Result

The Lambda function acts as the serverless backend of the registration application.

The final backend flow is:

```text
S3
 ↓
API Gateway
 ↓
Lambda: regUser
 ↓
PyMySQL
 ↓
RDS MySQL
 ↓
regdb.users
```
