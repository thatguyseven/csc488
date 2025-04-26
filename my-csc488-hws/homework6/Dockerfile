FROM python:3.9 
 
RUN mkdir /app 
COPY . /app 
WORKDIR /app/src  
RUN pip install -r /app/requirements.txt 

ENV FLASK_APP=app.py
EXPOSE 5000
CMD ["python", "app.py"]