# AWS IAM Role for Lambda

## Overview

AWS IAM is used to provide permissions to the Lambda function.

In this project, an IAM execution role named `reg-role` is created and assigned to the Lambda function `regUser`.

## Step 1: Open IAM

Go to:

```text
AWS Console
→ IAM
→ Roles
→ Create role
```

## Step 2: Select Trusted Entity

Select:

```text
Trusted entity type:
AWS service
```

Select the service:

```text
Use case:
Lambda
```

This allows AWS Lambda to assume the IAM role.

## Step 3: Configure Permissions

Attach the permissions required by the Lambda function.

For the learning project, the Lambda execution role is:

```text
Role Name:
reg-role
```

> For production environments, use least-privilege permissions instead of Administrator-level permissions.

## Step 4: Create the Role

Review the configuration and create the role.

The final role should be:

```text
IAM Role
   |
   └── reg-role
          |
          └── Trusted Service: Lambda
```

## Step 5: Assign Role to Lambda

Go to:

```text
AWS Console
→ Lambda
→ Functions
→ regUser
→ Configuration
→ Permissions
```

Under the execution role, verify that:

```text
reg-role
```

is attached to the Lambda function.

## Role Purpose

The IAM role provides the Lambda function with permission to interact with AWS resources required during execution.

The Lambda function also requires network/database connectivity to communicate with the RDS MySQL database.

## Security Best Practices

For production environments:

* Follow the principle of least privilege.
* Do not use AdministratorAccess unnecessarily.
* Grant only the permissions required by the Lambda function.
* Review IAM policies regularly.
* Avoid using long-term AWS access keys inside Lambda.
* Use IAM roles for AWS service-to-service access.

## Verification

After assigning the role:

```text
Lambda
   |
   └── regUser
          |
          └── Execution Role
                 |
                 └── reg-role
```

The Lambda function can now execute using the permissions provided by its IAM execution role.
