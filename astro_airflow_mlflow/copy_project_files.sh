#!/bin/bash

# Script to copy necessary project files into the Airflow project directory
# This ensures all dependencies are available in the container

echo "🚀 Copying project files into Airflow directory..."

# Define source and destination paths
SOURCE_DIR="/media/toni-birat/New Volume/English_Premier_League_Complete_Project"
AIRFLOW_DIR="/media/toni-birat/New Volume/English_Premier_League_Complete_Project/astro_airflow_mlflow"

# Copy src folder
echo "📂 Copying src/ folder..."
cp -r "$SOURCE_DIR/src" "$AIRFLOW_DIR/"

# Copy Datasets folder
echo "📊 Copying Datasets/ folder..."
cp -r "$SOURCE_DIR/Datasets" "$AIRFLOW_DIR/"

# Copy config folder
echo "⚙️  Copying config/ folder..."
cp -r "$SOURCE_DIR/config" "$AIRFLOW_DIR/"

# Copy logs folder
echo "📝 Copying logs/ folder..."
cp -r "$SOURCE_DIR/logs" "$AIRFLOW_DIR/"

# Copy individual files
echo "📄 Copying configuration files..."
cp "$SOURCE_DIR/params.yaml" "$AIRFLOW_DIR/"
cp "$SOURCE_DIR/schema.yaml" "$AIRFLOW_DIR/"
cp "$SOURCE_DIR/requirements.txt" "$AIRFLOW_DIR/project_requirements.txt"

# Create .gitignore to avoid committing copied files
echo "📝 Creating .gitignore for copied files..."
cat > "$AIRFLOW_DIR/.gitignore_copied" << EOL
# Copied project files - do not commit
src/
Datasets/
config/
logs/
params.yaml
schema.yaml
project_requirements.txt
EOL

echo "✅ All project files copied successfully!"
echo "🐳 You can now run 'astro dev start' to start the Airflow environment"
echo "📋 The copied files are listed in .gitignore_copied"
