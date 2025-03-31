# syntax=docker/dockerfile:1
# based on
# https://docs.docker.com/compose/gettingstarted/
# and some housekeeping
ARG BASEIMAGE=python:3.9-slim
FROM ${BASEIMAGE}

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy everything inside refined_image into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Streamlit port
EXPOSE 8501

# Healthcheck for Docker
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "MyApp.py", "--server.port=8501", "--server.address=0.0.0.0"]
