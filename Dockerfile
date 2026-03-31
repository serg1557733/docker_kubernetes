FROM python:3.9
WORKDIR /work_sbo
COPY ./src/main.py .
COPY ./src/requirements.txt  .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "main.py"]