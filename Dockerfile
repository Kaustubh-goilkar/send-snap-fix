FROM python:3.10.20-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

# Tell Flask where your app is
ENV FLASK_APP=App.py

# Run the Flask development server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]