FROM astrocrpublic.azurecr.io/runtime:3.0-2

# Set working directory
WORKDIR /usr/local/airflow

# Copy essential project files for logging test
COPY src ./src
COPY config ./config
COPY params.yaml ./params.yaml
COPY schema.yaml ./schema.yaml

# Create logs directory (instead of copying to avoid Docker issues)
RUN mkdir -p logs

# Copy project requirements if it exists
COPY project_requirements.txt ./project_requirements.txt

# Install project-specific Python packages
RUN pip install --no-cache-dir -r project_requirements.txt || echo "No additional requirements to install"

# Set environment variables for the project
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/airflow"
ENV PROJECT_ROOT="/usr/local/airflow"
