FROM python:3.12
RUN mkdir /app
RUN mkdir /app/db
WORKDIR /app
COPY ./main.py .
COPY ./requirements.txt .
COPY config.yml ./app/config.yml
# Install any requirements
RUN pip install --no-cache-dir -r requirements.txt
# Run Python program
CMD [ "python","-u","./main.py" ]