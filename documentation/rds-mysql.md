# Amazon RDS MySQL Database Setup

## Overview

Amazon RDS for MySQL is used as the persistent relational database for the Serverless Registration Application.

The Lambda function connects to the RDS MySQL database and stores user registration information in the `users` table.

## Architecture

```text
AWS Lambda
    |
    | PyMySQL
    v
Amazon RDS MySQL
    |
    v
regdb
    |
    v
users table
```

## Step 1: Create RDS MySQL Instance

Go to:

```text
AWS Console
→ RDS
→ Databases
→ Create database
```

Select:

```text
Engine: MySQL
```

Configure the required database settings.

For this project:

```text
Database: MySQL
Database Name: regdb
```

For the learning project, the RDS instance was configured as publicly accessible so that it could be accessed using MySQL Workbench.

> Publicly accessible RDS is suitable for this learning setup. For production, use a private RDS instance inside a VPC.

## Step 2: Configure Database

After the RDS instance is created and its status becomes:

```text
Available
```

Open the RDS instance and go to:

```text
Connectivity & security
```

Copy the RDS endpoint.

Example:

```text
database.xxxxxxxxx.ap-south-1.rds.amazonaws.com
```

The endpoint is required by the Lambda function to connect to the database.

## Step 3: Connect Using MySQL Workbench

Open MySQL Workbench.

Create a new MySQL connection using:

```text
Hostname: <RDS Endpoint>
Port: 3306
Username: admin
Password: <RDS Password>
```

Test the connection.

After successful connection, select the project database:

```sql
USE regdb;
```

## Step 4: Create Users Table

Create the registration table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);
```

## Step 5: Verify the Table

Check the tables:

```sql
SHOW TABLES;
```

Check the table structure:

```sql
DESCRIBE users;
```

Expected columns:

```text
id
name
email
password
```

## Step 6: Verify Registration Data

After a user registers through the application, run:

```sql
USE regdb;

SELECT * FROM users;
```

The registered user's information should appear in the table.

Example:

```text
+----+-------------+-------------------+----------+
| id | name        | email             | password |
+----+-------------+-------------------+----------+
|  1 | Test User   | test@example.com  | 123456   |
+----+-------------+-------------------+----------+
```

> Do not use real passwords or personal information in GitHub screenshots.

## Lambda Connection

The Lambda function connects to RDS using environment variables:

```text
DB_HOST=your-rds-endpoint
DB_USER=admin
DB_PASSWORD=your-password
DB_NAME=regdb
```

The Python backend uses PyMySQL to establish the database connection.

Example:

```python
connection = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"]
)
```

## Security Considerations

The RDS instance in this project was configured for learning and testing.

For a production environment:

* Keep RDS private.
* Do not expose MySQL port 3306 to the entire internet.
* Allow access only from required resources.
* Use security groups with least-privilege rules.
* Store database credentials securely.
* Use AWS Secrets Manager or Systems Manager Parameter Store.
* Avoid storing database passwords in source code or GitHub.

## Database Verification Flow

```text
User Registration
       |
       v
S3 Frontend
       |
       v
API Gateway
       |
       v
Lambda
       |
       | PyMySQL
       v
RDS MySQL
       |
       v
regdb.users
       |
       v
SELECT * FROM users;
```

## Result

Amazon RDS MySQL provides persistent storage for the registration application.

The complete database flow is:

```text
Frontend
   ↓
API Gateway
   ↓
Lambda
   ↓
PyMySQL
   ↓
RDS MySQL
   ↓
regdb.users
```
