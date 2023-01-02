FROM python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN adduser --disabled-password service-user 
WORKDIR /service

COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt
COPY service /service
EXPOSE 8000

