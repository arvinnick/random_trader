# Use elestio/metatrader5 as the base image
FROM elestio/metatrader5:latest

# Set the working directory
WORKDIR /home/developer/app

# Copy your Python files into the image
COPY ./app /home/developer/app

# Install additional Python packages if needed
RUN pip install --no-cache-dir -r reaqirements.txt

# Command to run your main Python script
CMD ["python3", "app.py"]
