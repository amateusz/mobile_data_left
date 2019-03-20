FROM python:3-alpine

# install requirements
WORKDIR /install

COPY requirements/requirements.txt ./
ADD https://github.com/amateusz/plus-online-client/releases/download/1.3.1/plus-online-client-1.3.1.tar.gz ./
ADD https://github.com/amateusz/my-orange-client/releases/download/1.2.5/my_orange_client-1.2.5.tar.gz ./

RUN pip install *.tar.gz
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install gunicorn>=19

# webapp sources

WORKDIR /webapp
COPY static static/
COPY templates templates/
COPY *.py ./

EXPOSE 8000

CMD ["gunicorn", "-w 4", "app:app", "-b", "0.0.0.0:8000"]