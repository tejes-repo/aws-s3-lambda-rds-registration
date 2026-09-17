# Serverless Registration Application Deployment

## 1. Project Overview

This project implements a serverless registration application using Amazon S3, API Gateway, AWS Lambda, and Amazon RDS MySQL.

The frontend is hosted as a static website on S3. Registration data is sent through API Gateway to Lambda, where it is processed and stored in the RDS MySQL database.

## 2. Architecture

```text
User
 |
 v
S3 Static Website
 |
 | HTTPS POST
 v
API Gateway
 |
 | POST /register
 v
AWS Lambda
 |
 | PyMySQL
 v
RDS MySQL
 |
 v
regdb.users
```

## 3. Deployment Components

The application consists of the following components:

```text
1. Amazon RDS MySQL
2. MySQL Database
3. IAM Role
4. AWS Lambda
5. PyMySQL Dependency
6. Amazon API Gateway
7. CORS Configuration
8. Amazon S3 Static Website
9. Frontend Registration Form
```

## 4. RDS MySQL Deployment

Create an Amazon RDS MySQL database.

Configuration:

```text
Engine:
MySQL

Database:
regdb

Username:
admin
```

For this learning project, the RDS instance is configured as publicly accessible for MySQL Workbench connectivity.

After the database becomes available, copy the RDS endpoint.

Example:

```text
database.xxxxxxxxx.ap-south-1.rds.amazonaws.com
```

## 5. Create Database Table

Connect to the RDS MySQL database using MySQL Workbench.

Run:

```sql
USE regdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);
```

Verify:

```sql
SHOW TABLES;

DESCRIBE users;
```

## 6. IAM Role Deployment

Create an IAM role for Lambda.

Configuration:

```text
Trusted Entity:
AWS Service

Service:
Lambda

Role Name:
reg-role
```

Attach the required permissions.

The Lambda function uses this role during execution.

> For production, use least-privilege permissions instead of administrator-level permissions.

## 7. Lambda Deployment

Create the Lambda function:

```text
Function Name:
regUser

Runtime:
Python 3.12

Architecture:
x86_64

Execution Role:
reg-role
```

The Lambda source code is stored in:

```text
source/lambda/lambda_function.py
```

## 8. Configure Lambda Environment Variables

Add:

```text
DB_HOST=your-rds-endpoint
DB_USER=admin
DB_PASSWORD=your-password
DB_NAME=regdb
```

Do not commit real credentials to GitHub.

## 9. Install PyMySQL

The Lambda backend uses PyMySQL to connect to MySQL.

Create a package directory:

```cmd
mkdir Lambda
cd Lambda
mkdir package
```

Install the dependency:

```cmd
pip install pymysql -t package
```

Package the dependency correctly for the AWS Lambda runtime and upload it with the Lambda deployment.

## 10. Test Lambda

Create an HTTP API version 2.0 test event:

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

Verify the database:

```sql
USE regdb;

SELECT * FROM users;
```

## 11. API Gateway Deployment

Create an HTTP API:

```text
API Name:
regapi
```

Add Lambda integration:

```text
Integration:
Lambda

Lambda Function:
regUser
```

Create the route:

```text
Method:
POST

Path:
/register
```

The final route is:

```text
POST /register
```

## 12. Create API Stage

Create:

```text
Stage Name:
regstage
```

After deployment, the API Gateway Invoke URL will look like:

```text
https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/regstage
```

The complete registration API endpoint is:

```text
https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/regstage/register
```

## 13. Configure CORS

Configure API Gateway CORS:

```text
Access-Control-Allow-Origin:
*

Access-Control-Allow-Headers:
content-type

Access-Control-Allow-Methods:
POST
OPTIONS
```

Save the configuration and deploy the changes to:

```text
regstage
```

## 14. Configure Frontend

The frontend is located at:

```text
source/frontend/index.html
```

Update the JavaScript API endpoint:

```javascript
fetch(
    "https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/regstage/register",
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
);
```

Replace the API ID with the actual API Gateway endpoint.

## 15. Create S3 Bucket

Create an S3 bucket:

```text
registration-frontend-13
```

Bucket names must be globally unique, so use a unique name if this name is already taken.

Upload:

```text
source/frontend/index.html
```

## 16. Enable Static Website Hosting

Go to:

```text
S3
→ Bucket
→ Properties
→ Static website hosting
```

Enable static website hosting.

Set:

```text
Index document:
index.html
```

Save the configuration.

## 17. Configure Website Access

For this learning project, configure the S3 bucket for public static website access as required by the S3 website hosting setup.

For production, use a more secure architecture such as CloudFront and appropriate S3 access controls.

## 18. Test the Application

Open the S3 static website endpoint.

Enter:

```text
Name
Email
Password
```

Click:

```text
Register Now
```

The request flow is:

```text
Browser
   |
   v
S3 Website
   |
   | POST /register
   v
API Gateway
   |
   v
Lambda
   |
   | PyMySQL
   v
RDS MySQL
```

## 19. Verify Registration

After successful registration, Lambda returns:

```json
{
    "message": "User registered successfully"
}
```

Open MySQL Workbench and run:

```sql
USE regdb;

SELECT * FROM users;
```

The newly registered user should appear in the result.

## 20. End-to-End Testing

Verify each layer individually:

```text
RDS MySQL
    ↓
Lambda Test
    ↓
API Gateway Test
    ↓
S3 Website Test
    ↓
MySQL Verification
```

### Expected Result

```text
S3 Website
     |
     | Registration Request
     v
API Gateway
     |
     | Lambda Integration
     v
AWS Lambda
     |
     | Database Connection
     v
RDS MySQL
     |
     v
User Record Stored
```

## 21. Troubleshooting

### Lambda Dependency Error

If Lambda returns:

```text
No module named 'pymysql'
```

verify that PyMySQL is included correctly in the Lambda deployment package.

### API Gateway Error

Verify:

```text
POST /register
```

and the Lambda integration:

```text
regUser
```

### CORS Error

Verify:

```text
Allow-Origin:
*

Allow-Headers:
content-type

Allow-Methods:
POST, OPTIONS
```

Then deploy the API changes.

### S3 Registration Error

If the S3 website loads but registration fails, check:

```text
1. Frontend API URL
2. API Gateway route
3. CORS
4. Lambda
5. RDS connectivity
6. Browser Network tab
```

## 22. Security Considerations

This is a learning/demo deployment.

For production:

* Use a private RDS database.
* Restrict security group rules.
* Do not expose MySQL port 3306 to everyone.
* Use least-privilege IAM permissions.
* Store database credentials in AWS Secrets Manager.
* Use HTTPS.
* Restrict CORS to trusted origins.
* Never commit passwords or AWS credentials to GitHub.
* Enable CloudWatch monitoring and logging.

## 23. Deployment Result

The final serverless registration application is deployed using:

```text
Amazon S3
      ↓
Amazon API Gateway
      ↓
AWS Lambda
      ↓
Amazon RDS MySQL
```

The application successfully allows users to submit registration information through the S3-hosted frontend and stores the registration data in the RDS MySQL database.
