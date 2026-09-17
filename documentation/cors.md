# CORS Configuration

## Overview

Cross-Origin Resource Sharing (CORS) allows the frontend hosted on Amazon S3 to communicate with the HTTP API hosted by Amazon API Gateway.

Without the correct CORS configuration, the browser may block requests from the S3 website to API Gateway.

## Architecture

```text id="3n5h4x"
Amazon S3
   |
   | Cross-Origin HTTP Request
   v
Amazon API Gateway
   |
   v
AWS Lambda
```

## Why CORS Is Required

The frontend and API are hosted on different origins.

Example:

```text id="f1qk8c"
Frontend:
S3 Static Website

API:
API Gateway
```

When JavaScript sends a request from the S3 website to API Gateway, the browser applies CORS security rules.

Therefore, API Gateway must allow the frontend origin and required HTTP methods and headers.

## Step 1: Open API Gateway

Go to:

```text id="n7z0hp"
AWS Console
→ API Gateway
→ regapi
→ CORS
```

## Step 2: Configure Allowed Origin

For this learning project:

```text id="j7f8s2"
Access-Control-Allow-Origin:
*
```

The `*` allows requests from any origin.

> For production, use the specific frontend domain instead of `*`.

## Step 3: Configure Allowed Headers

Add:

```text id="2s1n0c"
content-type
```

The frontend sends JSON using:

```http
Content-Type: application/json
```

Therefore, `content-type` must be allowed by the API.

## Step 4: Configure Allowed Methods

Allow:

```text id="3w9z7k"
POST
OPTIONS
```

`POST` is used to submit registration data.

`OPTIONS` is used by the browser for the CORS preflight request.

## Final CORS Configuration

```text id="u8f0p4"
Access-Control-Allow-Origin:
*

Access-Control-Allow-Headers:
content-type

Access-Control-Allow-Methods:
POST
OPTIONS
```

## Step 5: Save Configuration

Click:

```text id="4z9b2v"
Save
```

After modifying CORS, deploy the API changes to:

```text id="x3r6mv"
regstage
```

## CORS Request Flow

When the browser needs a preflight request:

```text id="c8n2py"
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

## Frontend Request

The frontend sends:

```javascript id="4ps2fj"
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

The API Gateway CORS configuration allows this request.

## Troubleshooting

### Error: Failed to Fetch

If the frontend displays:

```text id="9w5n4j"
TypeError: Failed to fetch
```

check the following:

```text id="hr9x1k"
1. CORS configuration
2. API Gateway URL
3. POST /register route
4. OPTIONS request
5. content-type allowed header
6. API deployment
7. Browser Network tab
```

## Browser Network Test

Open the S3 website and press:

```text id="0h1l5j"
F12
```

Then select:

```text id="5q7m9d"
Network
→ Fetch/XHR
```

Submit the registration form.

Look for:

```text id="1v7b8q"
OPTIONS /register
POST /register
```

The `OPTIONS` request should be successful before the browser sends the POST request.

## Common Mistakes

### Mistake 1: Missing `content-type`

Incorrect:

```text id="w3p7h2"
Access-Control-Allow-Headers:
```

Correct:

```text id="f6q1mz"
Access-Control-Allow-Headers:
content-type
```

### Mistake 2: Wrong API URL

Incorrect:

```text id="6b8m3n"
/regstage
```

Correct:

```text id="c2x9qa"
/regstage/register
```

### Mistake 3: CORS Changes Not Deployed

After changing CORS, deploy the API to:

```text id="9t2x7v"
regstage
```

## Production Recommendations

For production applications:

* Do not use `*` for allowed origins.
* Allow only the trusted frontend domain.
* Allow only required HTTP methods.
* Allow only required headers.
* Use HTTPS.
* Review CORS settings regularly.

## Result

Correct CORS configuration allows the S3-hosted frontend to communicate with API Gateway successfully.

Final communication flow:

```text id="j7m2vc"
S3 Frontend
     |
     | CORS-enabled HTTPS request
     v
API Gateway
     |
     v
Lambda
     |
     v
RDS MySQL
```
