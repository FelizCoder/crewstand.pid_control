# crewstand.pid_control

**Description:**  
This microservice implements a PID (Proportional-Integral-Derivative) controller for real-time process control. The service receives setpoints and sensor readings via WebSockets, calculates the PID output, and sends requests to control the actuator accordingly.

## Table of Contents

- [crewstand.pid\_control](#crewstandpid_control)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [Using Virtual Environment](#using-virtual-environment)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
  - [Usage](#usage)
    - [Quick start with Docker](#quick-start-with-docker)
      - [Pull the Docker images:](#pull-the-docker-images)

## Features

- **Real-time process control:** Uses PID algorithms to manage processes in real-time.
- **WebSocket Communication:** Efficiently handles asynchronous setpoints and sensor data.
- **Configurable Parameters:** Easily adjust PID parameters (Proportional, Integral, Derivative).

## Installation

### Using Virtual Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/FelizCoder/crewstand.pid_control.git
   cd crewstand.pid_control
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configuration

Configuration settings are defined in `app/utils/config.py` and can be customized via environment variables.

### Environment Variables

To configure the project, you need to set the following environment variables or create a `.env.local` file. Below is a table that describes each variable, its description, and its default value (if any).

| Variable Name           | Description                                 | Default Value              |
| ----------------------- | ------------------------------------------- | -------------------------- |
| `BACKEND_BASE`          | Base URL for the backend                    |                            |
| `PID_KP`                | Proportional gain for the PID controller    |                            |
| `PID_KI`                | Integral gain for the PID controller        |                            |
| `PID_KD`                | Derivative gain for the PID controller      |                            |
| `PID_OUTPUT_MIN`        | Minimum output value of the PID controller  |                            |
| `PID_OUTPUT_MAX`        | Maximum output value of the PID controller  |                            |
| `INFLUXDB_URL`          | URL for the InfluxDB instance               |                            |
| `INFLUXDB_BUCKET`       | InfluxDB bucket name                        |                            |
| `INFLUXDB_ORG`          | InfluxDB organization name                  |                            |
| `INFLUXDB_TOKEN`        | InfluxDB access token                       |                            |
| `PROJECT_NAME`          | Name of the project                         | `"swncrew pid controller"` |
| `PROPORTIONAL_VALVE_ID` | The id of the proportional valve to control | `0`                        |
| `SENSOR_ID`             | ID of the sensor                            | `0`                        |
| `DEBUG_LEVEL`           | Log level for debugging                     | `INFO`                     |

## Usage

### Quick start with Docker

The simplest way to set up and run both the crewstand.pid_control and crewstand.backend applications is to use Docker. This ensures that all dependencies and configurations are properly managed and isolated. Follow these steps to use Docker for both applications:

#### Pull the Docker images:

```bash
docker pull ghcr.io/felizcoder/crewstand.backend:latest
docker pull ghcr.io/felizcoder/crewstand.pid_control:latest
```

Set environment variables: Configure the required environment variables for both applications using the -e flag.

Run the Docker containers:

For crewstand.backend:

```bash
docker run -d -p 8000:8000 -e <environment variables> ghcr.io/felizcoder/crewstand.backend:latest
```

For crewstand.pid_control:

```bash
docker run -d -p 5000:5000 -e <environment variables> ghcr.io/felizcoder/crewstand.pid_control:latest
```
