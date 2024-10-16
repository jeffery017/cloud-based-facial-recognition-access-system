# Step 1: Use an official Ubuntu runtime as a base image
FROM ubuntu:22.04

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install dependencies (Python, pip, and Git)
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip git cmake && \
    apt-get clean

# Step 5: Install virtual environment and dependencies
RUN pip install -r requirements.txt

# Step 6: Expose port 8000
EXPOSE 8000

CMD ["python3", "app.py"]