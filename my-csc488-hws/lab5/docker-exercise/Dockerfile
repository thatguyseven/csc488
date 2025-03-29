# Use the official Alpine image
FROM alpine:latest

# Install Python (if needed for your app)
RUN apk add --no-cache python3 py3-pip

# Copy the application to the container
COPY /code/ml_data_analysis.py /code/ml_data_analysis.py

# Allow file to execute
RUN chmod +rx /code/ml_data_analysis.py

ENV PATH="/code:$PATH"