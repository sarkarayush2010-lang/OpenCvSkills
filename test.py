import math
import time
import cv2
import numpy as np
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
)

cap = cv2.VideoCapture(0)
canvas = None
prev_x, prev_y = 0, 0


brush_thickness = 5
min_thickness = 2
max_thickness = 50

prev_pinch_y = None

print("Finger Painter Running!")
print(" - Raise INDEX finger: Draw")
print(" - Raise INDEX + MIDDLE fingers: Clear Canvas")
print(" - EMOJI PINCH (Thumb + Index pinched + 3 fingers OUT): Adjust Brush Size")
print(" - Press 'q' to quit")

with HandLandmarker.create_from_options(options) as landmarker:
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
      canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    frame_timestamp_ms = int(time.time() * 1000)
    results = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

    gesture_text = "NONE"

    if results.hand_landmarks:
      hand_landmarks = results.hand_landmarks[0]

      thumb_tip = hand_landmarks[4]
      index_tip = hand_landmarks[8]
      index_pip = hand_landmarks[6]

      middle_tip = hand_landmarks[12]
      middle_pip = hand_landmarks[10]

      ring_tip = hand_landmarks[16]
      ring_pip = hand_landmarks[14]

      pinky_tip = hand_landmarks[20]
      pinky_pip = hand_landmarks[18]

      tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)
      ix, iy = int(index_tip.x * w), int(index_tip.y * h)

      index_up = iy < int(index_pip.y * h)
      middle_up = int(middle_tip.y * h) < int(middle_pip.y * h)
      ring_up = int(ring_tip.y * h) < int(ring_pip.y * h)
      pinky_up = int(pinky_tip.y * h) < int(pinky_pip.y * h)

      pinch_distance = math.hypot(ix - tx, iy - ty)
      thumb_index_pinched = pinch_distance < 40 

      is_emoji_pinch = (
          thumb_index_pinched and middle_up and ring_up and pinky_up
      )


      if is_emoji_pinch:
        gesture_text = f"RESIZING ({brush_thickness}px)"
        pinch_cx, pinch_cy = int((tx + ix) / 2), int((ty + iy) / 2)
        cv2.circle(
            frame, (pinch_cx, pinch_cy), 8, (0, 255, 255), cv2.FILLED
        )
        cv2.line(frame, (tx, ty), (ix, iy), (0, 255, 255), 3)

        if prev_pinch_y is not None:
          delta_y = prev_pinch_y - pinch_cy 
          if abs(delta_y) > 2:
            brush_thickness = int(
                np.clip(
                    brush_thickness + (delta_y * 0.3),
                    min_thickness,
                    max_thickness,
                )
            )

        prev_pinch_y = pinch_cy
        prev_x, prev_y = 0, 0

      else:
        prev_pinch_y = None

        if index_up and middle_up and not ring_up and not pinky_up:
          gesture_text = "CLEARING"
          canvas = np.zeros((h, w, 3), dtype=np.uint8)
          prev_x, prev_y = 0, 0

        elif index_up and not middle_up:
          gesture_text = "DRAWING"
          cv2.circle(
              frame,
              (ix, iy),
              int(brush_thickness / 2) + 2,
              (255, 0, 255),
              cv2.FILLED,
          )

          if prev_x == 0 and prev_y == 0:
            prev_x, prev_y = ix, iy

          cv2.line(
              canvas, (prev_x, prev_y), (ix, iy), (255, 0, 255), brush_thickness
          )
          prev_x, prev_y = ix, iy

        else:
          gesture_text = "HOVER"
          prev_x, prev_y = 0, 0

    merged_frame = cv2.addWeighted(frame, 1.0, canvas, 0.8, 0)

    text_size = cv2.getTextSize(gesture_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    text_x = w - text_size[0] - 20
    text_y = 40

    cv2.rectangle(
        merged_frame,
        (text_x - 10, text_y - 25),
        (w - 10, text_y + 10),
        (20, 20, 20),
        cv2.FILLED,
    )
    cv2.putText(
        merged_frame,
        gesture_text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )

    cv2.imshow("Finger Painter", merged_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

cap.release()
cv2.destroyAllWindows()