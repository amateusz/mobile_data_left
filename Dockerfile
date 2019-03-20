FROM python:3-alpine

# install requirements
WORKDIR /install
COPY requirements/* ./

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