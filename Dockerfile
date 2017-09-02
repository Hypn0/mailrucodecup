FROM python:latest
ADD ./run.py /
ADD ./Models /Models
ADD ./Controllers /Controllers
ADD ./req.txt /

RUN pip install -r /req.txt
EXPOSE 80
CMD python run.py

