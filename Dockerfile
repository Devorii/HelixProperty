FROM python:3.11-slim

ARG AWS_SSM_USERNAME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AWS_SSM_USERNAME=${AWS_SSM_USERNAME}

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

