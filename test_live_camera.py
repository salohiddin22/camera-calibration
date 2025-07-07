import os
import cv2
import numpy as np
import argparse

def main(camera_id):
    if not os.path.exists("info/calibration.npz"):
        print("Calibration file not found. Please run calibrate_camera.py first.")
        return

    data = np.load("info/calibration.npz")
    camMatrix = data["camMatrix"]
    distCoef = data["distCoef"]

    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        new_cam_mtx, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoef, (w, h), 1)
        undistorted = cv2.undistort(frame, camMatrix, distCoef, None, new_cam_mtx)

        cv2.imshow("Undistorted Live", undistorted)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera_id', type=int, default=2)
    args = parser.parse_args()
    main(args.camera_id)