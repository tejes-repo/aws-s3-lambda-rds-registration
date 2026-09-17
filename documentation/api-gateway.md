# Amazon API Gateway Configuration

## Overview

Amazon API Gateway provides the HTTP API endpoint for the Serverless Registration Application.

It receives registration requests from the S3-hosted frontend and invokes the AWS Lambda function `regUser`.

## Architecture

```text
S3 Static Website
       |
       | HTTP POST
       v
Amazon API Gateway
       |
       | Integration
       v
AWS Lambda
    regUser
       |
       v
Amazon RDS MySQL
```

## Step 1: Create HTTP API

Go to:

```text
AWS Console
→ API Gateway
→ Create API
```

Select:

```text
HTTP API
```

Create the API with:

```text
API Name:
regapi
```

## Step 2: Add Lambda Integration

Add an integration:

```text
Integration Type:
Lambda

Lambda Function:
regUser
```

The API Gateway integration connects the HTTP API with the Lambda backend.

## Step 3: Create API Route

Create the following route:

```text
Method:
POST

Resource Path:
/register

Integration Target:
regUser
```

The final route is:

```text
POST /register
```

This route receives the registration data from the frontend.

## Step 4: Create Stage

Create a stage:

```text
Stage Name:
regstage
```

For this project, automatic deployment can be disabled and deployments can be performed manually.

The stage URL will look like:

```text
https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/regstage
```

The complete registration endpoint is:

```text
https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/regstage/register
```

## Step 5: Configure CORS

Go to:

```text
API Gateway
→ regapi
→ CORS
```

Configure:

```text
Access-Control-Allow-Origin:
*

Access-Control-Allow-Headers:
content-type

Access-Control-Allow-Methods:
POST
OPTIONS
```

Save the configuration.

CORS allows the browser-based frontend hosted on S3 to communicate with API Gateway.

## Step 6: Deploy API

After creating the route and CORS configuration, deploy the API to:

```text
regstage
```

Verify that the deployment is active for the stage.

## Step 7: Configure Frontend API URL

Open:

```text
source/frontend/index.html
```

The JavaScript frontend should send the registration request to the complete API Gateway endpoint.

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

Replace the API ID with the actual API Gateway ID.

## Request Format

The frontend sends JSON data:

```json
{
  "name": "Kunal",
  "email": "kunal@test.com",
  "password": "123456"
}
```

The request is sent using:

```text
Method:
POST

Path:
/register

Content-Type:
application/json
```

## API Gateway Request Flow

```text
Browser
   |
   | POST /register
   | Content-Type: application/json
   v
API Gateway
   |
   | Lambda Integration
   v
regUser Lambda
   |
   | PyMySQL
   v
RDS MySQL
```

## Testing

The API can be tested through the frontend or by using tools such as Postman or cURL.

Example cURL request:

```bash
curl -X POST "https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/regstage/register" \
-H "Content-Type: application/json" \
-d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"password\":\"123456\"}"
```

Expected response:

```json
{
  "message": "User registered successfully"
}
```

## Browser Testing

Open the S3 static website and submit the registration form.

Use browser developer tools to troubleshoot API requests:

```text
F12
→ Network
→ Fetch/XHR
```

Check:

```text
OPTIONS /register
POST /register
```

The POST request should return a successful response.

## Troubleshooting

### Failed to fetch

If the S3 website shows:

```text
TypeError: Failed to fetch
```

check:

* API Gateway URL
* `/regstage/register` path
* `POST /register` route
* CORS configuration
* `content-type` allowed header
* `POST` and `OPTIONS` methods
* Browser Network tab

### CORS Error

Verify:

```text
Allow Origin:
*

Allow Headers:
content-type

Allow Methods:
POST, OPTIONS
```

After changing CORS, deploy the changes to `regstage`.

### 404 Not Found

Verify that the frontend uses:

```text
/regstage/register
```

and not only:

```text
/regstage
```

## Security Considerations

For production applications:

* Restrict allowed origins instead of using `*`.
* Use authentication and authorization.
* Apply API throttling where required.
* Use HTTPS.
* Keep the RDS database private.
* Use least-privilege IAM permissions.
* Monitor API Gateway and Lambda using CloudWatch.

## Result

API Gateway provides the communication layer between the S3 frontend and Lambda backend.

The final API flow is:

```text
S3
 ↓
API Gateway
 ↓
POST /register
 ↓
Lambda: regUser
 ↓
RDS MySQL
```
