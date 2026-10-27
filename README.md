# 🚦 AI-Powered Adaptive Traffic Light Control System

An intelligent traffic light management prototype designed to move away from rigid, fixed-timer systems toward **adaptive priority scheduling**. Instead of rotating through signals blindly, this system uses computer vision to detect waiting vehicles, track arrival order, and **skip empty lanes** to clear traffic efficiently.

---

## 💡 The Core Concept
* **Vehicle Detection:** Uses computer vision (YOLO) to monitor intersection approaches in real-time.
* **Dynamic Skipping:** If a major lane has waiting vehicles and the adjacent lanes are empty, the controller bypasses the empty signals.
* **Arrival Priority:** Prioritizes lanes based on how long vehicles have been waiting, ensuring fairness and reducing idle wait times.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`cv2`)
* **AI Model:** Ultralytics YOLOv8 (Nano model for fast edge inference)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/Mesumm8/ai-adaptive-traffic-light.git](https://github.com/Mesumm8/ai-adaptive-traffic-light.git)
cd ai-adaptive-traffic-light
2. Install Dependencies
Make sure you have Python installed, then run:

Bash
pip install opencv-python ultralytics
3. Run the Vehicle Counter Script
Place your script (e.g., traffic_counter.py) in the folder and run:

Bash
python traffic_counter.py
(Note: By default, the script looks at your webcam 0. You can replace 0 with a path to a traffic video file).

🗺️ Project Roadmap
[x] Phase 1: Basic vehicle detection and counting using YOLOv8 & OpenCV.

[ ] Phase 2: Implement Region of Interest (ROI) stop-lines to count only waiting vehicles.

[ ] Phase 3: Build the multi-lane state machine logic (arrival timestamps & lane skipping).

[ ] Phase 4: Simulate the system via a Python GUI or miniature hardware (Arduino/ESP32).

📄 License
This project is open-source and available under the MIT License.