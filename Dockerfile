# Use the AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.10

# Set the working directory in the container
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the Python script and requirements.txt into the container
COPY mood.py .
COPY best_model1.pkl .
COPY requirements.txt .
COPY images/ images/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run your Python script
CMD ["mood.main"]

