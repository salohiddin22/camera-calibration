import cv2
import os
import numpy as np
import imageio
import argparse
import matplotlib.pyplot as plt

def calibration(image_path, pattern_size, square_size, criteria, gif_path=None):
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

    obj_points = []
    img_points = []
    gif_frames = []

    for file in sorted(os.listdir(image_path)):
        path = os.path.join(image_path, file)
        img = cv2.imread(path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            obj_points.append(objp)
            img_points.append(corners2)

            vis = cv2.drawChessboardCorners(img.copy(), pattern_size, corners2, ret)
            gif_frames.append(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
            cv2.imshow('Chessboard', vis)
            cv2.waitKey(200)
        else:
            print(f"Checkerboard not detected in {file}")

    cv2.destroyAllWindows()

    if gif_path and gif_frames:
        os.makedirs(os.path.dirname(gif_path), exist_ok=True)
        imageio.mimsave(gif_path, gif_frames, fps=2)
        print(f"GIF saved to {gif_path}")

    if len(obj_points) == 0:
        print("No valid detections.")
        return None

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    print("Calibration successful.")

    os.makedirs("info", exist_ok=True)
    np.savez("info/calibration.npz", camMatrix=mtx, distCoef=dist, rVector=rvecs, tVector=tvecs)
    with open("info/out_v1.txt", "w") as f:
        f.write(str(mtx) + '\n' + str(dist))

    return mtx, dist, rvecs, tvecs, obj_points, img_points

def check_calibration(img_path, camMatrix, distCoef):
    print("<<<<<<<<< \nStarting calibration check >>>>>>")
    img = cv2.imread(img_path)
    if img is None:
        print(f"Cannot load sample image: {img_path}")
        return

    h, w = img.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoef, (w, h), 1)
    undistorted_img = cv2.undistort(img, camMatrix, distCoef, None, new_camera_matrix)

    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y + h, x:x + w]

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.set_title('Original Image', fontsize=30)
    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax2.set_title('Undistorted Image', fontsize=30)
    ax2.imshow(cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2RGB))
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', default='images')
    parser.add_argument('--pattern_size', type=int, nargs=2, default=[7, 7])
    parser.add_argument('--square_size', type=float, default=24.0)
    parser.add_argument('--gif_path', type=str, default='output/calibration.gif')
    args = parser.parse_args()

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    calibration(args.images_dir, tuple(args.pattern_size), args.square_size, criteria, args.gif_path)
    
    # Call the checkerboard validation on a sample image
    sample_images = [f for f in os.listdir(args.images_dir) if f.endswith('.png')]
    if sample_images:
        sample_img_path = os.path.join(args.images_dir, sample_images[0])
        
    if not os.path.exists("info/calibration.npz"):
        
        print("Calibration file not found. Please run calibrate_camera.py first.")
        
    data = np.load("info/calibration.npz")
    mtx = data["camMatrix"]
    dist = data["distCoef"]
    check_calibration(sample_img_path, mtx, dist)
