# Use the official Alpine image
FROM alpine:latest

# Set working directory as code
WORKDIR /code

# Copy the application and dependencies to the container
COPY /code/gen_ml_data.py /code/
COPY requirements.txt /code/

# Install Python and venv
# DEBUG NOTE: Ensure the virtul environment is activate before beginning any installation operations. This 
RUN apk add --no-cache python3 py3-pip python3-dev && \
    python3 -m venv /venv && \
    source /venv/bin/activate && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    /venv/bin/pip install -r /code/requirements.txt
