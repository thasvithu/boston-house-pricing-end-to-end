FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir gunicorn

# Copy app
COPY . .

EXPOSE 8080

CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:8080", "app:app"]