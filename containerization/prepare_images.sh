#!/bin/bash
# Define output directory
OUTPUT_DIR="D:/Operations/container_exports"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"
# Define image names and versions
GRAFANA_IMAGE="grafana/grafana:11.1.1"
PROMETHEUS_IMAGE="prom/prometheus:v2.53.2"

# Extract versions from the image names
GRAFANA_VERSION=$(echo $GRAFANA_IMAGE | awk -F':' '{print $2}')
PROMETHEUS_VERSION=$(echo $PROMETHEUS_IMAGE | awk -F':' '{print $2}')

# Define output tar file names
GRAFANA_TAR="$OUTPUT_DIR/grafana_image_$GRAFANA_VERSION.tar"
PROMETHEUS_TAR="$OUTPUT_DIR/prometheus_image_$PROMETHEUS_VERSION.tar"

# Pull the Docker images
docker pull $GRAFANA_IMAGE
docker pull $PROMETHEUS_IMAGE

# Save the images to tar files
docker save -o $GRAFANA_TAR $GRAFANA_IMAGE
docker save -o $PROMETHEUS_TAR $PROMETHEUS_IMAGE

# Transfer the files using a method suitable for your environment
# Example: Copy to a shared network folder, USB, etc.

echo "Images and files are ready for transfer."
