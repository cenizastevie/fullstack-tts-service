# Use AWS Amazon Linux 2 as the base image
FROM amazonlinux:2

# Install Python 3.8 and other required packages
RUN yum update -y && \
    yum install -y \
    python3 \
    python3-pip \
    tar \
    gzip \
    make \
    && yum clean all

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
