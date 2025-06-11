FROM astrocrpublic.azurecr.io/runtime:3.0-2

# Set working directory
WORKDIR /usr/local/airflow

# Install Git (assuming Debian/Ubuntu-based base image)
USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy essential project files
COPY src ./src
COPY config ./config
COPY params.yaml ./params.yaml
COPY schema.yaml ./schema.yaml
COPY .env ./.env

# Create logs directory
RUN mkdir -p logs

# Copy and install project requirements
COPY project_requirements.txt ./project_requirements.txt
RUN pip install --no-cache-dir -r project_requirements.txt || echo "No additional requirements to install"

# Set environment variables
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/airflow"
ENV PROJECT_ROOT="/usr/local/airflow"

# Optional: suppress MLflow Git warnings
ENV GIT_PYTHON_REFRESH=quiet