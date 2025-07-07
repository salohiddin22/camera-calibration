

# ## 📁 Directory Structure

# .
# ├── capture_images.py
# ├── calibrate_camera.py
# ├── test_live_camera.py
# ├── info/
# │   ├── calibration.npz
# │   └── out_v1.txt
# ├── images/
# │   └── imgXX.png
# ├── output/
# │   └── calibration.gif
# └── README.md
# ```

# ---

import cv2
import os
import argparse

def main(camera_id, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    num = len(os.listdir(save_dir))
    print(f"Press 's' to save, 'ESC' to quit")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Capture', frame)
        k = cv2.waitKey(5)
        if k == 27:
            break
        elif k == ord('s'):
            path = os.path.join(save_dir, f"img{num}.png")
            cv2.imwrite(path, frame)
            print(f"Saved: {path}")
            num += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--camera_id', type=int, default=2)
    parser.add_argument('--save_dir', type=str, default='images')
    args = parser.parse_args()
    main(args.camera_id, args.save_dir)


