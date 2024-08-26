
FROM python:3.9-slim


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
#CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]