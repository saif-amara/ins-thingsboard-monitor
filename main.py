import requests
import threading
import time
from kalman_filter import KalmanFilter1D
from imu_simulator import IMUSimulator

# ============================================
# CONFIG — بدّل الـ TOKEN بتاعك
# ============================================
TOKEN    = "mgHdkWJqhWrbe9iVM03E"
BASE_URL = f"http://localhost:9090/api/v1/{TOKEN}"

# ============================================
# INIT
# ============================================
kf  = KalmanFilter1D()
imu = IMUSimulator()

running = True

def send_telemetry():
    """Send IMU + Kalman data to ThingsBoard every 0.5s"""
    while running:
        # Get raw IMU readings
        readings = imu.get_readings()

        # Kalman filter steps
        kf.predict(readings["true_accel"])
        filtered_position = kf.update(readings["raw_position"])

        # Drift error
        drift_error = abs(readings["raw_position"] - filtered_position)

        # Payload to ThingsBoard
        payload = {
            # Raw IMU
            "accel_x": readings["accel_x"],
            "accel_y": readings["accel_y"],
            "accel_z": readings["accel_z"],
            "gyro_x":  readings["gyro_x"],
            "gyro_y":  readings["gyro_y"],
            "gyro_z":  readings["gyro_z"],

            # Positions
            "position_true":     readings["true_position"],
            "position_raw":      readings["raw_position"],
            "position_filtered": round(filtered_position, 4),

            # Drift
            "drift_error": round(drift_error, 4),
        }

        r = requests.post(f"{BASE_URL}/telemetry", json=payload)
        print(f"✅ t={round(imu.time,1)}s | "
              f"raw={readings['raw_position']:.3f} | "
              f"filtered={filtered_position:.3f} | "
              f"drift={drift_error:.3f} | "
              f"status={r.status_code}")

        time.sleep(0.5)

def listen_rpc():
    """Listen for RPC commands from Dashboard"""
    print("👂 Listening for RPC commands...")
    while running:
        try:
            r = requests.get(f"{BASE_URL}/rpc", timeout=30)
            if r.status_code == 200:
                cmd = r.json()
                method = cmd.get("method", "")
                print(f"📨 RPC received: {method}")

                if method == "reset_filter":
                    kf.reset()
                    imu.reset()
                    requests.post(
                        f"{BASE_URL}/rpc/{cmd['id']}",
                        json={"status": "Filter reset OK"}
                    )
        except:
            time.sleep(1)

# ============================================
# MAIN
# ============================================
print("🛩️  INS Monitor starting...")
print(f"📡 Sending to: {BASE_URL}")
print("-" * 50)

t = threading.Thread(target=listen_rpc)
t.daemon = True
t.start()

try:
    send_telemetry()
except KeyboardInterrupt:
    running = False
    print("\n🛑 INS Monitor stopped.")