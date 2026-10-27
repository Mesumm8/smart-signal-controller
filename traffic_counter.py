import cv2
from ultralytics import YOLO

# 1. Loading YOLO model
model = YOLO("yolov8n.pt")

# 2. Open video stream (use 0 for webcam, or path to video file)
cap = cv2.VideoCapture("traffic.mp4")  # Replace with your video file path or use 0 for webcam

# Vehicle classes in YOLO (COCO dataset)
# 2: car, 3: motorcycle, 5: bus, 7: truck
VEHICLE_CLASSES = [2, 3, 5, 7]

print("Running with Region of Interest (ROI)... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("End of video stream.")
        break

    # Get frame dimensions to define our ROI box dynamically
    height, width, _ = frame.shape

    # Define a Waiting Zone (Region of Interest) coordinates: [xmin, ymin, xmax, ymax]
    # For example, a box occupying the lower-middle portion of the screen representing a lane approach.
    # You can tweak these numbers based on your camera angle!
    roi_xmin = int(width * 0.5)
    roi_ymin = int(height * 0.5)
    roi_xmax = int(width * 0.7)
    roi_ymax = int(height * 0.8)

    # 3. Run YOLO inference
    results = model(frame, classes=VEHICLE_CLASSES, verbose=False)

    waiting_vehicles_count = 0

    # 4. Loop through detected objects and check if they are inside our ROI
    for box in results[0].boxes:
        # Get coordinates of the vehicle bounding box
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        
        # Calculate the center point of the vehicle's bounding box
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Check if the center point is inside our defined waiting zone
        if roi_xmin <= center_x <= roi_xmax and roi_ymin <= center_y <= roi_ymax:
            waiting_vehicles_count += 1
            # Draw a special bounding box around waiting vehicles (e.g., Blue)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        else:
            # Draw standard boxes for passing traffic (e.g., Gray)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (128, 128, 128), 1)

    # 5. Draw the Waiting Zone (ROI) box on the screen (Green rectangle)
    cv2.rectangle(frame, (roi_xmin, roi_ymin), (roi_xmax, roi_ymax), (0, 255, 0), 2)
    cv2.putText(
        frame, 
        "Waiting Zone (Stop Line)", 
        (roi_xmin, roi_ymin - 10), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.6, 
        (0, 255, 0), 
        2
    )

    # 6. Display the waiting vehicle count on top
    cv2.putText(
        frame, 
        f"Cars Waiting at Light: {waiting_vehicles_count}", 
        (30, 50), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (0, 0, 255), # Red text
        2
    )

    # Show window
    frame = cv2.resize(frame, (960, 540))
    cv2.imshow("Smart Signal ROI Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()