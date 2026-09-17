# Troubleshooting Guide

## Overview

This document contains common problems encountered while deploying and testing the Serverless Registration Application.

The main troubleshooting areas are:

* AWS Lambda dependencies
* Lambda execution
* API Gateway routes
* CORS
* S3 frontend
* RDS MySQL connectivity
* Browser Network errors

---

# 1. Lambda Import Error

## Error

```text
Unable to import module 'lambda_function':
No module named 'mysql.connector'
```

## Cause

The required MySQL Python dependency was not available in the Lambda deployment package.

The project originally used `mysql.connector`, but the final implementation uses PyMySQL.

## Solution

Install PyMySQL:

```cmd
pip install pymysql -t package
```

Package the dependency correctly and upload it with the Lambda deployment.

The Lambda source should use:

```python
import pymysql
```

---

# 2. Windows Dependency Compatibility

## Problem

Python dependencies installed on Windows can contain Windows-specific native files such as:

```text
*.pyd
```

These files may not work in the AWS Lambda Linux runtime.

## Solution

Build the Lambda dependency package for a Lambda-compatible environment.

For this project, PyMySQL is used to simplify the dependency packaging.

---

# 3. Lambda Test Works but S3 Does Not

## Problem

The Lambda test successfully inserts data into RDS MySQL, but registration from the S3 website fails.

## Diagnosis

This means the following components are working:

```text
Lambda
   ↓
RDS MySQL
```

The problem is likely between:

```text
S3
   ↓
API Gateway
```

Check:

* API Gateway URL
* API Gateway route
* CORS configuration
* Frontend `fetch()` URL
* Browser Network tab

---

# 4. Failed to Fetch Error

## Error

The frontend displays:

```text
Network Error: TypeError: Failed to fetch
```

## Possible Causes

* Incorrect API Gateway URL
* Incorrect API Gateway stage
* Incorrect route
* CORS configuration problem
* Missing `content-type` allowed header
* API Gateway changes not deployed

## Correct API Endpoint

The API Gateway route is:

```text
POST /register
```

Therefore the complete endpoint should be:

```text
https://<api-id>.execute-api.ap-south-1.amazonaws.com/regstage/register
```

Do not use only:

```text
https://<api-id>.execute-api.ap-south-1.amazonaws.com/regstage
```

---

# 5. CORS Configuration Problem

## Problem

The browser blocks the API request because the frontend and API are running on different origins.

## Solution

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

---

# 6. OPTIONS Request Problem

## Problem

The browser may send an `OPTIONS` request before the actual `POST` request.

The request flow is:

```text
Browser
   |
   | OPTIONS /register
   v
API Gateway
   |
   | CORS validation
   v
Browser
   |
   | POST /register
   v
API Gateway
   |
   v
Lambda
```

## Solution

Make sure API Gateway CORS allows:

```text
OPTIONS
POST
```

---

# 7. Check Browser Network Tab

Open the S3 website.

Press:

```text
F12
```

Select:

```text
Network
→ Fetch/XHR
```

Submit the registration form.

Look for:

```text
OPTIONS /register
POST /register
```

Check:

* Request URL
* Request Method
* Status Code
* Request Headers
* Response Headers

The POST request should use:

```text
https://<api-id>.execute-api.ap-south-1.amazonaws.com/regstage/register
```

---

# 8. API Gateway Route Error

## Problem

The API returns a route-related error.

## Check

Go to:

```text
API Gateway
→ regapi
→ Routes
```

The route should be:

```text
POST /register
```

Integration target:

```text
regUser
```

---

# 9. API Gateway Stage Problem

## Problem

The API URL is correct but the request still fails.

## Check

Go to:

```text
API Gateway
→ regapi
→ Stages
```

Verify:

```text
Stage:
regstage
```

After changing routes or CORS, deploy the latest configuration to this stage.

---

# 10. Lambda Environment Variable Problem

## Problem

Lambda cannot connect to the database.

## Check

Go to:

```text
Lambda
→ regUser
→ Configuration
→ Environment variables
```

Verify:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

Example:

```text
DB_HOST=your-rds-endpoint
DB_USER=admin
DB_PASSWORD=your-password
DB_NAME=regdb
```

Do not hard-code the password inside the Lambda source code.

---

# 11. RDS Connection Problem

## Problem

Lambda cannot connect to RDS MySQL.

## Check

### RDS Status

The RDS instance should be:

```text
Available
```

### Endpoint

Verify that `DB_HOST` contains the correct RDS endpoint.

### Port

MySQL normally uses:

```text
3306
```

### Security Group

Check whether the RDS security group allows the required MySQL connection.

For this learning project, the RDS instance was configured as publicly accessible.

> For production, use a private RDS instance and allow database access only from the required resources.

---

# 12. Database Table Problem

## Error

The Lambda function may return an error if the `users` table does not exist.

## Solution

Connect to RDS MySQL using MySQL Workbench:

```sql
USE regdb;

SHOW TABLES;
```

If required, create the table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);
```

Verify:

```sql
DESCRIBE users;
```

---

# 13. Database Verification

After a successful registration:

```sql
USE regdb;

SELECT * FROM users;
```

The new registration record should appear.

Example:

```text
+----+-------------+-------------------+----------+
| id | name        | email             | password |
+----+-------------+-------------------+----------+
|  1 | Test User   | test@example.com  | 123456   |
+----+-------------+-------------------+----------+
```

Do not use real user passwords in screenshots or GitHub documentation.

---

# 14. S3 Website Not Opening

## Problem

The S3 website does not open.

## Check

Verify:

```text
S3
→ Bucket
→ Properties
→ Static website hosting
```

Make sure static website hosting is enabled.

The index document should be:

```text
index.html
```

Also verify that `index.html` exists in the bucket.

---

# 15. Old `index.html` Being Loaded

## Problem

You updated the API URL in `index.html`, but the browser still uses the old URL.

## Solution

Upload the updated `index.html` to S3 again.

Then perform a hard refresh:

```text
Ctrl + Shift + R
```

---

# 16. Lambda Test Works

A successful Lambda test confirms that the backend logic and database connection are working.

Example test request:

```json
{
  "version": "2.0",
  "routeKey": "POST /register",
  "rawPath": "/register",
  "requestContext": {
    "http": {
      "method": "POST"
    }
  },
  "body": "{\"name\":\"Kunal\",\"email\":\"kunal@test.com\",\"password\":\"123456\"}",
  "isBase64Encoded": false
}
```

Expected response:

```json
{
  "message": "User registered successfully"
}
```

---

# 17. End-to-End Troubleshooting Flow

When the application does not work, check the components in this order:

```text
1. RDS MySQL
      ↓
2. Lambda
      ↓
3. API Gateway
      ↓
4. CORS
      ↓
5. S3 Frontend
      ↓
6. Browser Network
      ↓
7. Database Verification
```

---

# 18. Final Working Architecture

```text
                 User
                  |
                  v
        S3 Static Website
                  |
                  | HTTPS POST
                  v
          API Gateway
          POST /register
                  |
                  v
             Lambda
             regUser
                  |
                  | PyMySQL
                  v
            RDS MySQL
                  |
                  v
              regdb
                  |
                  v
              users
```

## Conclusion

The main troubleshooting areas for this project are Lambda dependency packaging, API Gateway routing, CORS configuration, S3 frontend configuration, and RDS connectivity.

Testing each layer independently makes it easier to identify where a request is failing.
