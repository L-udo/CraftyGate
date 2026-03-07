FROM python:3.12

ADD main.py .
ADD requirements.txt .
# Install any requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN touch servers.json
RUN chmod 777 servers.json
RUN touch config.yml

# Run Python program
CMD [ "python", "./main.py" ]