import numpy as np

class KalmanFilter1D:
    """
    1D Kalman Filter for IMU drift correction
    State: [position, velocity]
    """
    def __init__(self):
        # State vector [position, velocity]
        self.x = np.array([[0.0],
                           [0.0]])

        # State covariance matrix
        self.P = np.array([[1.0, 0.0],
                           [0.0, 1.0]])

        # State transition matrix (dt=0.1s)
        self.dt = 0.1
        self.F = np.array([[1.0, self.dt],
                           [0.0, 1.0]])

        # Control input matrix
        self.B = np.array([[0.5 * self.dt**2],
                           [self.dt]])

        # Measurement matrix (we measure position only)
        self.H = np.array([[1.0, 0.0]])

        # Process noise covariance
        self.Q = np.array([[0.001, 0.0],
                           [0.0,   0.001]])

        # Measurement noise covariance
        self.R = np.array([[0.5]])

    def predict(self, acceleration):
        """Predict step"""
        u = np.array([[acceleration]])
        self.x = self.F @ self.x + self.B @ u
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x[0, 0]

    def update(self, measurement):
        """Update step"""
        z = np.array([[measurement]])
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ (z - self.H @ self.x)
        self.P = (np.eye(2) - K @ self.H) @ self.P
        return self.x[0, 0]

    def reset(self):
        """Reset filter to initial state"""
        self.__init__()
        print("🔄 Kalman Filter reset!")