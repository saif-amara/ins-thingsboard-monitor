import numpy as np
import random

class IMUSimulator:
    """
    Simulates a 6-DOF IMU sensor with realistic noise and drift
    """
    def __init__(self):
        self.time = 0.0
        self.dt = 0.1
        
        # True position (ground truth)
        self.true_position = 0.0
        self.true_velocity = 0.0
        
        # Raw position (with drift - no filter)
        self.raw_position = 0.0
        
        # Noise parameters
        self.accel_noise = 0.1      # Accelerometer noise
        self.gyro_noise  = 0.05     # Gyroscope noise
        self.drift_rate  = 0.002    # Drift per timestep

    def get_readings(self):
        """Generate one IMU reading"""
        self.time += self.dt

        # True acceleration (sinusoidal motion)
        true_accel = np.sin(self.time * 0.5) * 2.0

        # Update true state
        self.true_velocity += true_accel * self.dt
        self.true_position += self.true_velocity * self.dt

        # Noisy accelerometer reading
        accel_x = true_accel + random.gauss(0, self.accel_noise)
        accel_y = random.gauss(0, self.accel_noise * 0.5)
        accel_z = 9.81 + random.gauss(0, self.accel_noise * 0.3)

        # Noisy gyroscope reading
        gyro_x = random.gauss(0, self.gyro_noise)
        gyro_y = random.gauss(0, self.gyro_noise)
        gyro_z = np.cos(self.time * 0.3) + random.gauss(0, self.gyro_noise)

        # Raw position (cumulative drift)
        self.raw_position += (accel_x * self.dt) + (self.drift_rate * self.time)

        return {
            "accel_x": round(accel_x, 4),
            "accel_y": round(accel_y, 4),
            "accel_z": round(accel_z, 4),
            "gyro_x":  round(gyro_x, 4),
            "gyro_y":  round(gyro_y, 4),
            "gyro_z":  round(gyro_z, 4),
            "true_accel":    round(true_accel, 4),
            "true_position": round(self.true_position, 4),
            "raw_position":  round(self.raw_position, 4),
        }

    def reset(self):
        """Reset simulator"""
        self.__init__()
        print("🔄 IMU Simulator reset!")