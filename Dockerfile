# base image  
FROM python:3.8   

RUN --mount=type=secret,id=MW_DJANGO_SECRET_KEY \
  export MW_DJANGO_SECRET_KEY=$(cat /run/secrets/MW_DJANGO_SECRET_KEY)

ENV MW_DJANGO_SECRET_KEY=abc
# setup environment variable  
ENV APP_DIR=/sticks  

# set work directory  
RUN mkdir -p $APP_DIR  

COPY ./website $APP_DIR 

# where your code lives  
WORKDIR $APP_DIR

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
