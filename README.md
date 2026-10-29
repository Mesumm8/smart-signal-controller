# 🚦 AI-Powered Adaptive Traffic Light Control System

An intelligent traffic light management prototype that moves away from rigid, fixed-timer signals toward **adaptive priority scheduling**. Instead of rotating through signals blindly, the system uses computer vision to detect waiting vehicles in each approach, **skips empty lanes**, and gives green time to lanes that actually have traffic.

---

## 📸 Screenshots

> Add your screenshots to a `screenshots/` folder in the repo and update the file names below.

### Live Detection Dashboard
![Live detection dashboard](screenshots/dashboard.png)
*Four colour-coded lane zones (North, East, South, West) with live queue counts and the active green lane shown in the banner.*

### Active Lane Highlighting
![Active lane highlighting](screenshots/active-lane.png)
*The lane with the green light gets a thicker border and an "ACTIVE" tag.*

### Lane Zone Setup
![ROI lane zones](screenshots/roi-zones.png)
*Region-of-interest boxes placed over each approach so only waiting vehicles are counted.*

### Demo (optional)
![Demo GIF](screenshots/demo.gif)

---

## 💡 The Core Concept

* **Vehicle Detection:** YOLOv8 monitors the intersection in real time and detects cars, motorcycles, buses and trucks.
* **Queue Counting (ROI):** Each lane has its own region of interest. Only vehicles whose centre is inside a lane's zone are counted as waiting.
* **Dynamic Skipping:** If a lane has no waiting vehicles, the controller bypasses it and moves to the next lane that does.
* **Timed Green Phases:** Each lane stays green for a set time (default 8 seconds), or until it empties, then the signal moves clockwise to the next lane with waiting cars.
* **Arrival Priority (planned):** Prioritise lanes by how long vehicles have been waiting, for fairness and shorter idle times.

---

## 🧠 How It Works

```
Video frame ──► YOLOv8 detection ──► ROI check per lane ──► Queue counts
                                                                │
                                              Traffic controller (state machine)
                                                                │
                                         Active lane + on-screen dashboard
```

1. Each frame is resized and passed to YOLOv8 (confidence 0.20, vehicle classes only).
2. The centre point of every detection is tested against each lane's ROI box.
3. Counted vehicles are drawn in their lane's colour. Other traffic is drawn in grey.
4. The controller picks the active lane based on the counts and the green timer.

### Lane colours

| Lane | Colour |
|------|--------|
| North | Cyan |
| East | Orange |
| South | Magenta |
| West | Yellow |

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`cv2`)
* **AI Model:** Ultralytics YOLOv8 (Nano model for fast edge inference)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Mesumm8/ai-adaptive-traffic-light.git
cd ai-adaptive-traffic-light
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install opencv-python ultralytics
```

### 3. Add a Video
Place your intersection video in the project folder (the script expects `multi-lane.mp4` by default).

### 4. Run the Traffic Controller
```bash
python traffic_counter.py
```
Press **`q`** to quit.

> **Note:** To use a webcam instead of a video file, change this line in the script:
> ```python
> cap = cv2.VideoCapture(0)
> ```

---

## ⚙️ Configuration

| Setting | Where | What it does |
|---------|-------|--------------|
| `green_time` | `TrafficController(lanes, green_time=8)` | Seconds each lane stays green |
| `intersection_lanes` | top of the script | Order the signal cycles through the lanes |
| `active_rois` | inside the main loop | ROI box for each lane, as fractions of frame width and height |
| `conf` | `model(frame, conf=0.20, ...)` | YOLO detection confidence threshold |

To move a lane zone, edit its `xmin`, `ymin`, `xmax` and `ymax` values (fractions of the frame, `0.0` to `1.0`).

---

## 🗺️ Project Roadmap

- [x] **Phase 1:** Basic vehicle detection and counting using YOLOv8 & OpenCV.
- [x] **Phase 2:** Region of Interest (ROI) zones per lane to count only waiting vehicles.
- [ ] **Phase 3:** Multi-lane state machine logic
  - [x] Lane skipping for empty lanes
  - [x] Timed green phases with clockwise rotation
  - [ ] Arrival timestamps and wait-time priority
- [ ] **Phase 4:** Simulate the system via a Python GUI or miniature hardware (Arduino/ESP32).

---

## 📄 License

This project is open-source and available under the MIT License.