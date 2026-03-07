FROM python:3.12
WORKDIR /app
COPY main.py .
COPY requirements.txt .
COPY ./config.yml /app/config.yml
COPY ./servers.json /app/servers.json
# Install any requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run Python program
CMD [ "python", "./main.py" ]