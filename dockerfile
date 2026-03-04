FROM python:3.12

# Copy repo into container
COPY . . 

# Install any requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run Python program
CMD [ "python", "./main.py" ]