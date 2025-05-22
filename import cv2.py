import cv2
import numpy as np

# Constants
KNOWN_DISTANCE = 20  # meters (not used directly here, placeholder for future)
KNOWN_WIDTH = 2.5    # meters (placeholder for scale-based calculations)
FPS = 24             # frames per second of the video

# Function to calculate distance between two points (pixels)
def calculate_distance(point_a, point_b):
    return np.sqrt(((point_a[0] - point_b[0]) ** 2) + ((point_a[1] - point_b[1]) ** 2))

# Load video
video = cv2.VideoCapture('video.mp4')  # Replace with actual path

if not video.isOpened():
    print("Error: Could not open video file.")
    exit()

# Read the first frame
ret, frame = video.read()
if not ret:
    print("Error: Couldn't read the video.")
    video.release()
    exit()

height, width, _ = frame.shape
car_centroids = []

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    roi = frame[int(height/2):height, :]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    edges = cv2.Canny(blur_roi, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    current_centroids = []

    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            centroid_x = x + w / 2
            centroid_y = y + h / 2
            current_centroids.append((centroid_x, centroid_y))

            # Draw bounding box and centroid
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(roi, (int(centroid_x), int(centroid_y)), 4, (0, 0, 255), -1)

    # Speed / movement tracking logic (placeholder for future expansion)
    if car_centroids and current_centroids:
        for i, curr in enumerate(current_centroids):
            if i < len(car_centroids):
                prev = car_centroids[i]
                dist = calculate_distance(curr, prev)
                speed = dist * FPS  # speed in pixels/sec
                cv2.putText(
                    roi,
                    f"Speed: {speed:.2f}px/s",
                    (int(curr[0]), int(curr[1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                )

    car_centroids = current_centroids.copy()

    # Show result
    frame[int(height/2):height, :] = roi
    cv2.imshow("Car Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
