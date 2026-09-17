import json
import os
import pymysql


def lambda_handler(event, context):

    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "content-type",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    }

    try:

        # Get HTTP method from API Gateway HTTP API
        method = event["requestContext"]["http"]["method"]

        # Handle CORS preflight request
        if method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "CORS OK"
                })
            }

        # Read request body
        body = json.loads(event["body"])

        # Connect to RDS MySQL
        connection = pymysql.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"]
        )

        # Create cursor
        cursor = connection.cursor()

        # Insert registration data
        query = """
        INSERT INTO users(name, email, password)
        VALUES (%s, %s, %s)
        """

        values = (
            body["name"],
            body["email"],
            body["password"]
        )

        cursor.execute(query, values)

        # Save changes
        connection.commit()

        # Close database resources
        cursor.close()
        connection.close()

        # Success response
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "message": "User registered successfully"
            })
        }

    except Exception as e:

        print("Error:", str(e))

        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "error": str(e)
            })
        }
