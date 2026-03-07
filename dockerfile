FROM python:3.12
WORKDIR /app
COPY main.py .
COPY requirements.txt .
COPY config.yml .
COPY servers.json .
# Install any requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run Python program
CMD [ "python", "./main.py" ]