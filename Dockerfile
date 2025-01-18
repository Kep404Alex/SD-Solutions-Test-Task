FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY app /app/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
