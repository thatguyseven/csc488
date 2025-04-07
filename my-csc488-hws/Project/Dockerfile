# Use the official Alpine image
FROM alpine:latest

# Create app directory
RUN mkdir /app

# Set working directory to app
WORKDIR /app

# Copy the application and dependencies to the container
COPY . /app

# Install Python and venv
# DEBUG NOTE: Ensure the virtul environment is activate before beginning any installation operations. This 
RUN apk add --no-cache python3 py3-pip python3-dev && \
    python3 -m venv /venv && \
    source /venv/bin/activate && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    /venv/bin/pip install -r /code/requirements.txt


CMD ["flask run -p 5000"] 