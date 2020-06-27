FROM python:3.7-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install cython
#RUN apk del .build-deps gcc musl-dev

COPY blockchain app

WORKDIR app

RUN pip install -U setuptools

RUN pip install -r requirements.txt

EXPOSE 5000

RUN [ "/bin/rm" ,"-rf", "*.db" ]

RUN  [ "rm" ,"-rf", "*.ini"] 

RUN  [ "rm" ,"-rf", "*.json"]

ENTRYPOINT [ "python",  "main.py"]
