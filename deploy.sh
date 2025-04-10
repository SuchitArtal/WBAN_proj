#!/bin/bash

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "Elastic Beanstalk CLI is not installed. Please install it first."
    exit 1
fi

# Initialize EB application if not already done
if [ ! -f ".elasticbeanstalk/config.yml" ]; then
    echo "Initializing Elastic Beanstalk application..."
    eb init -p docker wban-auth
fi

# Create RDS instance if not exists
echo "Checking RDS instance..."
if ! aws rds describe-db-instances --db-instance-identifier wban-db &> /dev/null; then
    echo "Creating RDS instance..."
    aws rds create-db-instance \
        --db-instance-identifier wban-db \
        --db-instance-class db.t3.micro \
        --engine postgres \
        --master-username postgres \
        --master-user-password $DB_PASSWORD \
        --allocated-storage 20 \
        --vpc-security-group-ids $SECURITY_GROUP_ID
fi

# Wait for RDS to be available
echo "Waiting for RDS to be available..."
aws rds wait db-instance-available --db-instance-identifier wban-db

# Get RDS endpoint
RDS_ENDPOINT=$(aws rds describe-db-instances --db-instance-identifier wban-db --query 'DBInstances[0].Endpoint.Address' --output text)

# Update environment variables
sed -i "s|your_rds_endpoint|$RDS_ENDPOINT|g" .ebextensions/02_environment.config
sed -i "s|your_secure_password|$DB_PASSWORD|g" .ebextensions/02_environment.config

# Create EB environment if not exists
if ! eb status wban-auth-env &> /dev/null; then
    echo "Creating Elastic Beanstalk environment..."
    eb create wban-auth-env
fi

# Deploy application
echo "Deploying application..."
eb deploy

echo "Deployment complete! Your application is now live on AWS." 