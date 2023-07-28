import cv2
import math

# Global variables
points = []
mode = None

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def mouse_callback(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        if mode == 'L':
            points.append([x, y])
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # Draw a red circle at the clicked point
            print(f"Line point {len(points)}: ({x}, {y})")
            if len(points) == 2:
                cv2.line(frame, tuple(points[0]), tuple(points[1]), (0, 255, 0), 2)
                print(f"LINE = {points}")
                points = []

        elif mode == 'P':
            points.append([x, y])
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # Draw a red circle at the clicked point
            print(f"Polygon point {len(points)}: ({x}, {y})")
            if len(points) > 1:
                for i in range(len(points) - 1):
                    cv2.line(frame, tuple(points[i]), tuple(points[i + 1]), (0, 255, 0), 2)

        elif mode == 'C':
            points.append([x, y])
            cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)  # Draw a red circle at the clicked point
            print(f"Circle point {len(points)}: ({x}, {y})")
            if len(points) == 2:
                radius = int(calculate_distance(points[0], points[1]))
                cv2.circle(frame, tuple(points[0]), radius, (0, 255, 0), 2)
                print(f"CIRCLE = Center: {points[0]}, Radius: {radius}")
                points = []

    elif event == cv2.EVENT_RBUTTONDOWN:
        if mode == 'L':
            if len(points) == 2:
                print(f"LINE = {points}")
                points = []

        elif mode == 'P':
            # points.append(points[0])  # Connect the last point to the first to close the polygon
            print(f"POLY = {points}")
            points = []

        elif mode == 'C':
            if len(points) == 2:
                radius = int(calculate_distance(points[0], points[1]))
                cv2.circle(frame, tuple(points[0]), radius, (0, 255, 0), 2)
                print(f"CIRCLE = Center: {points[0]}, Radius: {radius}")
                points = []

def main():
    global frame, mode

    # Set the video file path as a variable
    video_path = "highway.mp4"  # Replace this with your desired video file path

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Read the 10th frame
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_count >= 10:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 9)

    ret, frame = cap.read()

    # Create a window and set the mouse callback
    cv2.namedWindow('Video Frame')
    cv2.setMouseCallback('Video Frame', mouse_callback)

    print("Press 'L' for lines, 'P' for polygons, 'C' for circles. Right-click to finish drawing.")

    while True:
        # Display the current frame
        cv2.imshow('Video Frame', frame)

        # Wait for user input (L, P, or C key)
        key = cv2.waitKey(1)
        if key == ord('l') or key == ord('L'):
            mode = 'L'
            points = []
            print("Line mode activated. Click two points to draw a line.")
        elif key == ord('p') or key == ord('P'):
            mode = 'P'
            points = []
            print("Polygon mode activated. Click points to draw a polygon.")
        elif key == ord('c') or key == ord('C'):
            mode = 'C'
            points = []
            print("Circle mode activated. Click two points to draw a circle.")
        elif key == 27:  # Press 'Esc' to exit the program
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
