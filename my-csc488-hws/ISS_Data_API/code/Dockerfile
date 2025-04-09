FROM python:3.9 
 
RUN mkdir /app 
WORKDIR /app 
COPY . /app 
RUN pip install -r /app/requirements.txt 
 
ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["python", "app.py"]