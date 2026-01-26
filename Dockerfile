FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /itcproject

# Copy the requirements file into the container
COPY itcproject/requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY itcproject .

# Expose the port the app runs on
EXPOSE 5500

# Command to run the application
CMD ["python", "main.py"]