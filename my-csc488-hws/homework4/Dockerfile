FROM python:3.9
 
RUN mkdir /app 
WORKDIR /app 
COPY ml_data_analysis.py /app 
COPY Meteorite_Landings.json /app 

ENTRYPOINT ["python3", "ml_data_analysis.py"]
CMD ["Meteorite_Landings.json"]