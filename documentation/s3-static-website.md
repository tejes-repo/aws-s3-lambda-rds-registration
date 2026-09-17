# Amazon S3 Static Website Hosting

## Overview

Amazon S3 is used to host the frontend of the Serverless Registration Application as a static website.

The frontend contains the registration form built using HTML, CSS, and JavaScript.

When a user submits the form, JavaScript sends the registration data to the API Gateway endpoint.

## Architecture

```text
User Browser
     |
     v
Amazon S3
Static Website
     |
     | POST Request
     v
Amazon API Gateway
```

## Step 1: Create S3 Bucket

Go to:

```text
AWS Console
→ S3
→ Create bucket
```

Create a bucket with a unique name.

Example:

```text
registration-frontend-13
```

Bucket names must be globally unique.

## Step 2: Upload Frontend

The frontend file is:

```text
source/frontend/index.html
```

Upload it to the S3 bucket.

The bucket should contain:

```text
registration-frontend-13/
└── index.html
```

## Step 3: Configure Static Website Hosting

Open:

```text
S3
→ Bucket
→ Properties
```

Find:

```text
Static website hosting
```

Enable:

```text
Static website hosting
```

Configure the index document:

```text
index.html
```

Save the configuration.

## Step 4: Configure Public Access

For this learning project, the S3 bucket is configured to allow public access to the static website.

The purpose is to allow users to access the registration page through the S3 website endpoint.

> For production applications, consider using Amazon CloudFront with appropriate access controls instead of making the S3 bucket publicly accessible.

## Step 5: Access the Website

After enabling static website hosting, AWS provides a website endpoint.

Open the S3 website endpoint in a browser.

The registration page should be displayed.

Example:

```text
http://<bucket-name>.s3-website.ap-south-1.amazonaws.com
```

The exact endpoint is provided by AWS for the selected region.

## Step 6: Configure API Gateway URL

The frontend JavaScript must contain the API Gateway registration endpoint.

Example:

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

The URL must include the API Gateway stage and route:

```text
/regstage/register
```

## Step 7: Test the Registration Form

Open the S3 website.

Enter registration details:

```text
Name:
Email:
Password:
```

Click:

```text
Register Now
```

The frontend sends the request:

```text
S3 Website
     |
     | POST /register
     v
API Gateway
     |
     v
Lambda
     |
     v
RDS MySQL
```

## Step 8: Verify the Response

After successful processing, Lambda returns:

```json
{
    "message": "User registered successfully"
}
```

The frontend displays the success message.

## Step 9: Verify Database

Open MySQL Workbench and execute:

```sql
USE regdb;

SELECT * FROM users;
```

The newly registered user should appear in the result.

## Troubleshooting

### Website Does Not Open

Check:

* S3 static website hosting is enabled.
* `index.html` exists in the bucket.
* The correct S3 website endpoint is being used.
* Required public access configuration is available for the learning setup.

### Registration Form Opens but Registration Fails

Check:

* API Gateway URL in `index.html`.
* API Gateway `POST /register` route.
* API Gateway CORS configuration.
* Lambda function.
* RDS connectivity.

### Failed to Fetch

Open browser developer tools:

```text
F12
→ Network
→ Fetch/XHR
```

Check the API request.

The request URL should contain:

```text
/regstage/register
```

## Security Considerations

This project uses a public S3 website configuration for learning purposes.

For production:

* Use Amazon CloudFront for website delivery.
* Use HTTPS.
* Avoid exposing the S3 bucket unnecessarily.
* Use appropriate bucket policies.
* Keep the RDS database private.
* Configure API Gateway CORS for specific trusted origins.
* Use secure authentication mechanisms.

## Result

Amazon S3 provides the static frontend hosting layer for the application.

The complete frontend flow is:

```text
User
 ↓
S3 Static Website
 ↓
JavaScript Fetch API
 ↓
API Gateway
 ↓
Lambda
 ↓
RDS MySQL
```
