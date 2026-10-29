import cv2
from ultralytics import YOLO

# 1. Loading YOLO model
model = YOLO("yolov8n.pt")

# 2. Open video stream (use 0 for webcam, or path to video file)
cap = cv2.VideoCapture("multi-lane.mp4")

# Vehicle classes in YOLO (COCO dataset)
# 2: car, 3: motorcycle, 5: bus, 7: truck
VEHICLE_CLASSES = [2, 3, 5, 7]

# Traffic controller logic
class TrafficController:
    def __init__(self, lanes):
        self.lanes = lanes
        self.current_index = 0

    def get_next_active_lane(self, lane_counts):
        """
        Evaluates lanes starting from the current index.
        Skips any lane that has 0 waiting vehicles.
        """
        num_lanes = len(self.lanes)
        for i in range(num_lanes):
            check_index = (self.current_index + i) % num_lanes
            lane_name = self.lanes[check_index]

            if lane_counts.get(lane_name, 0) > 0:
                self.current_index = check_index
                return lane_name, lane_counts[lane_name]

        # Fallback if all lanes are empty
        return self.lanes[self.current_index], 0

# Initialize controller for all 4 intersection lanes
intersection_lanes = ["Lane_West", "Lane_North", "Lane_East", "Lane_South"]
controller = TrafficController(intersection_lanes)

# Unique color per lane (BGR format)
LANE_COLORS = {
    "Lane_North": (255, 255, 0),   # Cyan
    "Lane_East":  (0, 140, 255),   # Orange
    "Lane_South": (255, 0, 255),   # Magenta
    "Lane_West":  (0, 255, 255)    # Yellow
}

print("Running Multi-Lane Traffic Controller... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("End of video stream.")
        break

    # Resize FIRST so ROI boxes and the banner share the same coordinate space
    frame = cv2.resize(frame, (960, 540))
    height, width, _ = frame.shape

    # --- ROI BOXES ---
    active_rois = {
        "Lane_North": [
            # Moved down onto the car queue, clear of the top banner
            {"xmin": int(width * 0.28), "ymin": int(height * 0.36), "xmax": int(width * 0.47), "ymax": int(height * 0.54)}
        ],
        "Lane_East": [
            {"xmin": int(width * 0.69), "ymin": int(height * 0.35), "xmax": int(width * 0.92), "ymax": int(height * 0.53)}
        ],
        "Lane_South": [
            {"xmin": int(width * 0.10), "ymin": int(height * 0.52), "xmax": int(width * 0.32), "ymax": int(height * 0.82)}
        ],
        "Lane_West": [
            {"xmin": int(width * 0.70), "ymin": int(height * 0.58), "xmax": int(width * 0.98), "ymax": int(height * 0.97)}
        ]
    }

    # 3. Run YOLO inference
    results = model(frame, conf=0.20, classes=VEHICLE_CLASSES, verbose=False)

    lane_counts = {lane: 0 for lane in intersection_lanes}

    # 4. Check each detection against the ROI boxes
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        counted_lane = None
        for lane_name, boxes in active_rois.items():
            for b in boxes:
                if b["xmin"] <= center_x <= b["xmax"] and b["ymin"] <= center_y <= b["ymax"]:
                    counted_lane = lane_name
                    break
            if counted_lane:
                break

        if counted_lane:
            lane_counts[counted_lane] += 1
            # Counted vehicle drawn in its lane's color
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), LANE_COLORS[counted_lane], 2)
        else:
            # Gray box for traffic outside the queue zones
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (128, 128, 128), 1)

    # 5. Feed counts into the controller
    active_lane, active_count = controller.get_next_active_lane(lane_counts)

    # --- 6. DRAW LANE BOXES + LABELS ---
    for lane_name, boxes in active_rois.items():
        color = LANE_COLORS[lane_name]
        is_active = (lane_name == active_lane)
        thickness = 4 if is_active else 2

        for c in boxes:
            cv2.rectangle(frame, (c["xmin"], c["ymin"]), (c["xmax"], c["ymax"]), color, thickness)

        # Label drawn INSIDE the box so it never hides behind the banner
        first = boxes[0]
        label = f"{lane_name}: {lane_counts[lane_name]}" + ("  ACTIVE" if is_active else "")
        cv2.putText(frame, label, (first["xmin"] + 5, first["ymin"] + 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Status banner
    cv2.rectangle(frame, (20, 15), (780, 95), (0, 0, 0), -1)

    cv2.putText(frame, f"Active Green Light: {active_lane} ({active_count} vehicles)", (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Queue -> N: {lane_counts['Lane_North']} | E: {lane_counts['Lane_East']} | S: {lane_counts['Lane_South']} | W: {lane_counts['Lane_West']}",
                (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Real Multi-Lane Smart Traffic System", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()