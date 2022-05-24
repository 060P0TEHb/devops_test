FROM python:3.9.12-alpine
WORKDIR /app
COPY requirements.txt monitoring.py .
run pip3 install --no-cache-dir -r requirements.txt
CMD ["python3","/app/monitoring.py"]
