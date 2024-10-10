# init a base image (Alpine is small Linux distro)
FROM python:3.9.6-alpine
# update pip to minimize dependency errors
WORKDIR /docker-flask
COPY . /docker-flask
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python","app.py"]
