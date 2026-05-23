# 🛩️ AI-Augmented INS Monitor

Real-time Inertial Navigation System monitoring with Kalman Filter,
built on ThingsBoard IoT platform.

## 📋 Project Overview

This project simulates a 6-DOF IMU sensor and applies a 1D Kalman Filter
to correct drift in real-time. Data is visualized on a ThingsBoard dashboard.

## 🏗️ Architecture

```
IMU Simulator → Kalman Filter → ThingsBoard (MQTT/HTTP) → Dashboard
```

## 📁 Project Structure

```
ins_thingsboard/
├── kalman_filter.py   # 1D Kalman Filter implementation
├── imu_simulator.py   # 6-DOF IMU sensor simulator
├── main.py            # Main entry point + ThingsBoard integration
├── requirements.txt   # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- ThingsBoard (Docker)

### Installation

```bash
# Clone the repository
git clone https://github.com/saif-amara/ins-thingsboard-monitor.git
cd ins-thingsboard-monitor

# Install dependencies
pip install -r requirements.txt

# Start ThingsBoard
docker run -it -p 9090:9090 -p 1883:1883 --name mytb --restart always thingsboard/tb-postgres
```

### Configuration

Edit `main.py` and replace the TOKEN:
```python
TOKEN = "your_device_token_here"
```

### Run

```bash
python main.py
```

## 📊 Dashboard Features

| Widget | Description |
|--------|-------------|
| Time Series Chart | Raw vs Filtered vs True position |
| Drift Error Gauge | Real-time drift magnitude |
| Reset Filter Button | RPC command to reset Kalman filter |
| Alarm | Triggered when drift > threshold |

## 🔧 Technical Details

### Kalman Filter
- **State vector**: [position, velocity]
- **Process noise (Q)**: 0.001
- **Measurement noise (R)**: 0.5

### IMU Simulator
- **Accelerometer noise**: σ = 0.1 m/s²
- **Gyroscope noise**: σ = 0.05 rad/s
- **Drift rate**: 0.002 m/step

## 🎯 Applications

- UAV/Drone navigation systems
- Aerospace avionics prototyping
- Embedded systems education

## 👤 Author

Saif Eddine Amara
Embedded Systems Engineering Student — ISSAT Sousse, Tunisia
Teaching Assistant, Robotics Lab
