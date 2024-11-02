Overview

In this project, I set out to build and deploy a Flask application using Docker, while also preparing to manage the infrastructure on AWS using Terraform. This document outlines the steps I’ve taken so far, the challenges faced, and the solutions implemented.

Flask Application Setup

I began by creating a basic Flask application that would serve as the foundation for my project. I defined the necessary routes and ensured all required libraries were included in requirements.txt. This setup allowed me to create a functional application that could be easily containerized.

Docker Configuration

To containerize the application, I created a Dockerfile that established the environment for the Flask app. I configured it to install the necessary dependencies and set up Nginx as a reverse proxy to handle incoming requests.

Key Improvements:

I configured Nginx to handle both HTTP and HTTPS traffic, enabling secure communication.
By using Nginx as a reverse proxy, I improved the application’s performance and security. This setup allows Nginx to manage SSL termination while directing traffic to the Gunicorn server running the Flask application.

Nginx Configuration

I carefully crafted the Nginx configuration file to ensure proper request handling. I implemented redirection from HTTP to HTTPS, which enhances security by encrypting data in transit. Additionally, I set up SSL certificates to establish secure connections.

Terraform Infrastructure

Moving on to infrastructure management, I installed Terraform and securely configured my AWS credentials. I then began writing Terraform scripts to automate the provisioning of resources on AWS.

Key Steps Taken:

I defined AWS as the provider and set up remote state storage using S3 and DynamoDB for state locking. This approach ensures that the infrastructure state is managed reliably.
To control access, I created networking resources, including a VPC, public and private subnets, and security groups.
I launched EC2 instances to host my Jenkins server and application servers, ensuring they were properly configured for my application’s needs.

Next Steps

As I move forward with the project, my next steps include:

1. Implementing continuous integration and deployment (CI/CD) pipelines with Jenkins.
2. Setting up monitoring and logging to track the performance and health of my application and infrastructure.
3. Exploring scaling options for the application to handle varying loads effectively.
4. Enhancing security by reviewing IAM roles, policies, and security group settings to ensure adherence to best practices.
