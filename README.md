## `README.md`

# Camera Calibration Suite

A complete camera calibration toolkit using OpenCV.

## Features
✅ Capture calibration images from webcam  
✅ Calibrate camera using checkerboard images  
✅ Visualize real-time undistorted output  
✅ Save detection GIF for documentation  

---

## 📁 Project Structure

```
camera-calibration/
│
├── capture_images.py
├── calibrate_camera.py
├── test_live_camera.py
├── info/
│   ├── calibration.npz
│   └── out_v1.txt
├── images/
│   └── imgXX.png
├── output/
│   └── calibration.gif
└── README.md

---

## 🧩 Setup
```bash
# Clone the repository
git clone --recursive https://github.com/salohiddin22/camera-calibration.git

# Navigate to the project folder.
cd camera-calibration

# Create the Conda environment.
conda create -n camera-calibration python==3.10.0

# Activate the new environment
conda activate camera-calibration

# Install the necessary requirements
pip install -r requirements.txt
```

---

## 🔸 Step 1: Capture Calibration Images
```bash
python capture_images.py --camera_id 0 --save_dir images
```
> Press 's' to save an image, 'ESC' to quit

---

## 🔸 Step 2: Calibrate Camera
```bash
python calibrate_camera.py --images_dir images --pattern_size 8 5 --square_size 24
```
> If your checkerboard has 9 squares wide × 6 squares high, use `8 5` for pattern_size.  
> Count inner corners, not squares. Include both black & white squares.

---

## 🔸 Step 3: Test Live Undistortion
```bash
python test_live_camera.py --camera_id 0
```

---

## 📷 Sample Output
![Calibration GIF](output/calibration.gif)

---

## 🧠 Notes
- `info/calibration.npz`: contains intrinsic matrix and distortion coefficients (NumPy file)
- `info/out_v1.txt`: human-readable copy

---

## 📜 License
MIT

---

## Credits

This project builds upon this excellent open source project:

[Camera Calibration](https://github.com/RakhmatovShohruh/Camera_Calibration#Overview) Original implementation of the calibration