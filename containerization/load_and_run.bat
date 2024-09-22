@echo off

REM Set the paths for your Docker images
set GRAFANA_IMAGE_PATH=D:\Operations\container_exports\grafana_image_11.1.1.tar
set PROMETHEUS_IMAGE_PATH=D:\Operations\container_exports\prometheus_image_v2.53.2.tar

REM Load the Grafana image
echo Loading Grafana image...
docker load -i %GRAFANA_IMAGE_PATH%
if %ERRORLEVEL% neq 0 (
    echo Failed to load Grafana image.
    exit /b %ERRORLEVEL%
)

REM Load the Prometheus image
echo Loading Prometheus image...
docker load -i %PROMETHEUS_IMAGE_PATH%
if %ERRORLEVEL% neq 0 (
    echo Failed to load Prometheus image.
    exit /b %ERRORLEVEL%
)

REM Change to the directory containing your docker-compose.yml file
cd /d %~dp0

REM Run docker-compose to start the services
echo Starting Docker Compose...
docker-compose up -d
if %ERRORLEVEL% neq 0 (
    echo Failed to start Docker Compose.
    exit /b %ERRORLEVEL%
)

echo Docker Compose services started successfully.

pause
