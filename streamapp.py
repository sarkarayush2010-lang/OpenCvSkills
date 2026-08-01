import cv2
import numpy as np
import streamlit as st
from PIL import Image
import time
import math

# =========================================== Basic Layout ========================================

st.set_page_config(page_title="Cv2 & AI stuff i learned", layout="wide")
st.title("Image Processing & AI Sandbox")
st.write("things i learned with open cv, numpy and more!")

st.sidebar.header("Navigation")
mode = st.sidebar.radio(
    "Choose Media Type:", 
    ["Image Filters", "Live Filters", "Data Visualization", "Image Recognition (Keras)", "Hand Tracking", "Finger Painter", "Graphing Calculator", "music visualizer"]
)

kernel = np.ones((5, 5), np.uint8)

# ============================================== Mode 1 - Static Image =====================================

if mode == "Image Filters":
    st.subheader("Image Filters")
    uploaded_file = st.file_uploader("Upload any image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Image", width='content')
            
        with col2:
            filter_choice = st.selectbox(
                "Select Transformation Engine:",
                [
                    "Original printed Matrix",
                    "Resized image",
                    "Grayscale",
                    "Black and white",
                    "Eroded",
                    "Dilated",
                    "Inverse (Black & White)",
                    "Add Shapes",
                    "Caption",
                    "Contour"
                ]
            )
            
            if filter_choice == "Original printed Matrix":
                st.write("Raw pixel array")
                st.code(str(img))
                st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), width='content')
            
            elif filter_choice == "Resized image":
                resized = cv2.resize(img, (640, 480))
                st.image(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB), caption="Resized (640x480)", width='content')
            
            elif filter_choice == "Grayscale":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                st.image(gray, caption="Grayscale", clamp=True, width='content')
                
            elif filter_choice == "Black and white":
                thresh_val = st.slider("Contrast Threshold:", 0, 255, 150)
                gray_base = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, b_w = cv2.threshold(gray_base, thresh_val, 255, cv2.THRESH_BINARY)
                st.image(b_w, caption="Black and White", clamp=True, width='content')
                
            elif filter_choice == "Eroded":
                eroded = cv2.erode(img, kernel, iterations=1)
                st.image(cv2.cvtColor(eroded, cv2.COLOR_BGR2RGB), caption="Eroded View", width='content')
                
            elif filter_choice == "Dilated":
                dilated = cv2.dilate(img, kernel, iterations=1)
                st.image(cv2.cvtColor(dilated, cv2.COLOR_BGR2RGB), caption="Dilated view", width='content')
            
            elif filter_choice == "Inverse (Black & White)":
                thresh_val = st.slider("Contrast Threshold:", 0, 255, 150)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, b_w = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
                inverted = cv2.bitwise_not(b_w)
                st.image(inverted, caption="Inverted B&W", clamp=True, width='content')

            elif filter_choice == "Add Shapes":
                annotated = img.copy()
                h, w, _ = annotated.shape
                cv2.rectangle(annotated, (int(w*0.05), int(h*0.05)), (int(w*0.3), int(h*0.3)), (0, 255, 0), 3)
                cv2.line(annotated, (int(w*0.05), int(h*0.9)), (int(w*0.3), int(h*0.7)), (255, 0, 0), 3)
                cv2.circle(annotated, (int(w*0.7), int(h*0.2)), int(min(w, h)*0.1), (0, 0, 255), 3)
                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), width='content')
                
            elif filter_choice == "Caption":
                text_img = img.copy()
                h, w, _ = text_img.shape
                cv2.putText(text_img, "Hello World", (int(w*0.1), int(h*0.5)), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 4)
                st.image(cv2.cvtColor(text_img, cv2.COLOR_BGR2RGB), caption="Captioned Image", width='content')
                
            elif filter_choice == "Contour":
                contour_img = img.copy()
                gray = cv2.cvtColor(contour_img, cv2.COLOR_BGR2GRAY)
                _, b_w = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
                contours, _ = cv2.findContours(b_w.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(contour_img, contours, -1, (0, 255, 150), 3)
                for cntr in contours:
                    bx, by, bw, bh = cv2.boundingRect(cntr)
                    cv2.rectangle(contour_img, (bx-10, by-10), (bx+bw+10, by+bh+10), (0, 255, 0), 2)
                st.image(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB), caption="Contour Boxes", width='content')
    else:
        st.info("Drop an image into the uploader above to get started!")

# ============================================== Mode 2 - Video Filters =====================================

elif mode == "Live Filters":
    st.subheader("Live Video Effects")
    
    from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
    import av

    live_filter = st.selectbox(
        "Select Active Effect:",
        ["Regular Video", "Line Filter", "Threshold Matrix", "Slicing", "Make Half Red"]
    )
    
    speed = st.sidebar.slider("Line Speed", 1, 12, 4) if live_filter == "Line Filter" else 4
    live_thresh = st.slider("Binary Contrast Threshold", 0, 255, 80) if live_filter == "Threshold Matrix" else 80

    class VideoProcessor(VideoTransformerBase):
        def __init__(self):
            self.liney = 0
            self.canvas = None

        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            
            if live_filter == "Regular Video":
                out_frame = img
                
            elif live_filter == "Threshold Matrix":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, blackf = cv2.threshold(gray, live_thresh, 255, cv2.THRESH_BINARY_INV)
                gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                bin_3ch = cv2.cvtColor(blackf, cv2.COLOR_GRAY2BGR)
                out_frame = np.hstack((gray_3ch, bin_3ch))
                
            elif live_filter == "Slicing":
                h, w, _ = img.shape
                out_frame = img[0:int(h), 0:int(w/2)]
                
            elif live_filter == "Make Half Red":
                out_frame = img.copy()
                h, w, _ = img.shape
                out_frame[0:h, 0:int(w/2)] = (0, 0, 255)
                
            elif live_filter == "Line Filter":
                if self.canvas is None or self.canvas.shape != img.shape:
                    self.canvas = img.copy()
                    
                self.canvas[self.liney:self.liney+speed, :] = img[self.liney:self.liney+speed, :]
                out_frame = img.copy()
                if self.liney > 0:
                    out_frame[0:self.liney, :] = self.canvas[0:self.liney, :]
                    
                cv2.line(out_frame, (0, self.liney), (img.shape[1], self.liney), (255, 50, 50), 2)
                
                self.liney += speed
                if self.liney >= img.shape[0]:
                    self.liney = 0
                    self.canvas = img.copy()

            rgb_out = cv2.cvtColor(out_frame, cv2.COLOR_BGR2RGB)
            return av.VideoFrame.from_ndarray(rgb_out, format="rgb24")

    webrtc_streamer(key=f"opencv-filter-{live_filter}-{speed}-{live_thresh}", video_processor_factory=VideoProcessor)

# ============================================== Mode 3 - Data Analytics =====================================

elif mode == "Data Visualization":
    st.subheader("Pandas & Matplotlib Visualizer")
    import pandas as pd
    import matplotlib.pyplot as plt

    uploaded_data = st.file_uploader("Upload CSV or TXT file:", type=["csv", "txt"])
    if uploaded_data is not None:
        if uploaded_data.name.endswith('.txt'):
            df = pd.read_csv(uploaded_data, sep=None, engine="python")
        else:
            df = pd.read_csv(uploaded_data)
        
        if df is not None:
            st.markdown("### Dataset Preview")
            st.dataframe(df, width='content')
            st.caption(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
            st.markdown("---")
            
            chart_type = st.selectbox(
                "Choose Visualization Type:",
                ["Line/Scatter Plot", "Pie Chart", "Double Bar Chart", "Histogram"]
            )   
            all_columns = list(df.columns)
            fig, ax = plt.subplots()

            if chart_type == "Line/Scatter Plot":
                col_x = st.selectbox("X-Axis", all_columns, index=0)
                col_y = st.selectbox("Y-Axis", all_columns, index=min(1, len(all_columns)-1))
                markercolor = st.selectbox("Marker Color", ["green", "red", "blue"])
                markershape = st.selectbox("Marker Style", ["o (circle)", "h (hexagon)", "- (line)", "s (square)"])
                marker_style = markercolor[0] + markershape[0]
                
                ax.plot(df[col_x], df[col_y], marker_style)
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                st.pyplot(fig)
                
            elif chart_type == "Pie Chart":
                label_col = st.selectbox("Category Column:", all_columns)
                value_col = st.selectbox("Numeric Value Column:", all_columns)
                
                ax.pie(df[value_col], labels=df[label_col], autopct='%1.1f%%', shadow=True)
                st.pyplot(fig)

            elif chart_type == "Double Bar Chart":
                x_axis_col = st.selectbox("X-Axis (Independent):", all_columns)
                series_1 = st.selectbox("Series 1:", all_columns)
                series_2 = st.selectbox("Series 2:", all_columns)
                
                ax.bar(df[x_axis_col], df[series_1], alpha=0.5, label=series_1, color='blue')
                ax.bar(df[x_axis_col], df[series_2], alpha=0.5, label=series_2, color='green')
                ax.set_xlabel(x_axis_col)
                ax.legend()
                st.pyplot(fig)
            
            elif chart_type == "Histogram":
                data_col = st.selectbox("Select Numeric Column:", all_columns)
                bin_count = st.slider("Bins:", 3, 20, 6)
                
                ax.hist(df[data_col], bins=bin_count, rwidth=0.8, color='purple', alpha=0.7)
                ax.set_ylabel("Frequency")
                ax.set_xlabel(data_col)
                st.pyplot(fig)

# ============================================== Mode 4 - Keras AI Recognition =====================================

elif mode == "Image Recognition (Keras)":
    st.subheader(" Image recognition! ")
    st.write("AI? more like artificial image-recognition because this thing isnt accurate at all!")
    st.write("Well... see for yourself! ")
    st.write("also whats the difference between jpg and jpeg bro its the same thingggg")
    st.write("P.S. images that are as close to perfect squares are the best for recognition! but it works anyways, just a little less acurate")

    try:
        from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
        from tensorflow.keras.preprocessing.image import img_to_array

        @st.cache_resource
        def load_keras_model():
            return MobileNetV2(weights="imagenet")

        model = load_keras_model()

        img_file = st.file_uploader("Upload an photo jpeg, jpg, or png:", type=["jpg", "jpeg", "png"], key="keras_upload")

        if img_file is not None:
            col1, col2 = st.columns(2)

            image = Image.open(img_file).convert("RGB")
            with col1:
                st.image(image, caption="Uploaded Image", width='content')

            with col2:
                with st.spinner("Classifying with MobileNetV2..."):
                    resized_img = image.resize((224, 224))
                    img_array = img_to_array(resized_img)
                    img_batch = np.expand_dims(img_array, axis=0)
                    prepared_img = preprocess_input(img_batch)

                    predictions = model.predict(prepared_img)
                    top_preds = decode_predictions(predictions, top=3)[0]

                st.markdown("### Top Predictions")
                for i, (imagenet_id, label, score) in enumerate(top_preds):
                    confidence = float(score) * 100
                    st.write(f"**{i+1}. {label.replace('_', ' ').title()}**")
                    st.progress(int(confidence))
                    st.caption(f"Confidence: {confidence:.2f}%")

    except ImportError:
        st.error("TensorFlow is not installed in your environment! Run `pip install tensorflow` to use this tab.")

# ============================================== Mode 5 - Hand Tracking (MediaPipe) =====================================

elif mode == "Hand Tracking":
    st.subheader("🖐️ Real-Time Hand & Finger Landmark Tracking")
    st.markdown("since when did google make these stuff? anmd what does mediapipe even mean")
    st.markdown("chose camera, and just wave your hand around, it creates 20 points on the hands")

    import cv2
    import numpy as np
    import mediapipe as mp
    from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
    import av

    max_hands = st.sidebar.slider("Maximum hands to detect", 1, 4, 2)
    detection_con = st.sidebar.slider("mIn detection confidence (decrease to make it show up even if its not sure its a hand)", 0.1, 1.0, 0.5)

    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    #hehe i stole this from google idk what im even doing
    HAND_CONNECTIONS = [
        (0,1), (1,2), (2,3), (3,4),        # Thumb
        (0,5), (5,6), (6,7), (7,8),        # Index finger
        (5,9), (9,10), (10,11), (11,12),   # Middle finger
        (9,13), (13,14), (14,15), (15,16), # Ring finger
        (13,17), (0,17), (17,18), (18,19), (19,20) # Pinky & Palm base
    ]

    class HandProcessor(VideoTransformerBase):
        def __init__(self):
            options = HandLandmarkerOptions(
                base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
                running_mode=VisionRunningMode.IMAGE,
                num_hands=max_hands,
                min_hand_detection_confidence=detection_con
            )
            self.landmarker = HandLandmarker.create_from_options(options)
    #  dont worry i know the rest i think
        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            h, w, _ = img.shape
            
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

            results = self.landmarker.detect(mp_image)

            if results.hand_landmarks:
                for hand_landmarks in results.hand_landmarks:
                    for start_idx, end_idx in HAND_CONNECTIONS:
                        pt1 = (int(hand_landmarks[start_idx].x * w), int(hand_landmarks[start_idx].y * h))
                        pt2 = (int(hand_landmarks[end_idx].x * w), int(hand_landmarks[end_idx].y * h))
                        cv2.line(img, pt1, pt2, (255, 0, 100), 2)

                    for lm in hand_landmarks:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img, (cx, cy), 4, (0, 255, 0), cv2.FILLED)

            rgb_out = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return av.VideoFrame.from_ndarray(rgb_out, format="rgb24")

    webrtc_streamer(
        key=f"hand-tracking-{max_hands}-{detection_con}", 
        video_processor_factory=HandProcessor
    )

# ============================================== Mode 6 - finger painting! =====================================

elif mode == "Finger Painter":
    st.title("🤏 Gesture Finger Painter")

    import mediapipe as mp

    st.markdown("""
    **Controls & Gestures:**
    * 👆 **Index Finger UP:** Draw on canvas
    * ✌️ **Index + Middle UP (Ring/Pinky DOWN):** Clear canvas
    * 🤏 **Emoji Pinch (Thumb + Index pinched + 3 fingers OUT):** Move UP/DOWN to change brush size
    """)

    run_app = st.sidebar.checkbox("Power Camera", value=True)
    brush_color_hex = st.sidebar.color_picker(
        "Pick Brush Color", "#1ACA31"
    ) 

    hex_val = brush_color_hex.lstrip("#")
    rgb_color = tuple(int(hex_val[i : i + 2], 16) for i in (0, 2, 4))
    bgr_color = (rgb_color[2], rgb_color[1], rgb_color[0])

    frame_placeholder = st.empty()

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

    canvas = None
    prev_x, prev_y = 0, 0
    brush_thickness = 5
    min_thickness = 2
    max_thickness = 50
    prev_pinch_y = None

    cap = cv2.VideoCapture(0)

    try:
        with HandLandmarker.create_from_options(options) as landmarker:
            while cap.isOpened() and run_app:
                ret, frame = cap.read()
                if not ret:
                    st.error("Webcam feed not available.")
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
                        cv2.circle(frame, (pinch_cx, pinch_cy), 8, (0, 255, 255), cv2.FILLED)
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
                                bgr_color,
                                cv2.FILLED,
                            )

                            if prev_x == 0 and prev_y == 0:
                                prev_x, prev_y = ix, iy

                            cv2.line(
                                canvas, (prev_x, prev_y), (ix, iy), bgr_color, brush_thickness
                            )
                            prev_x, prev_y = ix, iy

                        else:
                            gesture_text = "HOVER"
                            prev_x, prev_y = 0, 0

                merged_frame = cv2.addWeighted(frame, 1.0, canvas, 0.8, 0)

                text_size = cv2.getTextSize(
                    gesture_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2
                )[0]
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

                display_frame = cv2.cvtColor(merged_frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(display_frame, channels="RGB", width='content')

    finally:
        cap.release()
        
        
        
        
#===============================================================Graphing calculator cuz im a chud and miscalculated and i need 41 more minutes so imma just do this and optimize some more stuff sjassdija=======
        
        
elif mode=="Graphing Calculator":
    st.subheader("Ripoff Desmos")
    st.write("Uhh can plot functions because it can")
    st.write("\"where the f the function\" - drake im pretty sure")
    col1,col2=st.columns([1,2])
    with col1:
        func_input=st.text_input("gimme the function", value="sin(x)")
        x_min=st.number_input("Min X", value=10.0,step=1.0)
        x_max=st.number_input("X Max", value=10.0, step=1.0)
        num_points=st.slider("resolution(lower makes it more efficient pls dont waste my streamlit resources im broke i cant afford ts)", 100, 2000, 500)
        line_color=st.ccolor_picker("Line color?", "#0195FF")
        show_grid=st.checkbox("show grid", value=True)
    
    with col2:
        if x_min>=xMax:
            st.error("dawg how is xmin lower then xmax ts cant be graphed bro")
        else:
            try:
                import pandas as pd
                import sympy as sp
                
                x_vals=np.linspace(x_min, x_max, num_points)
                
                x_sym=sp.Symbol("x")
                sym_expr=sp.sympify(func_input)

                funct=sp.lambdify(x_sym,sym_expr,modules=["numpy"])
                
                y_vals=np.full_like(x_vals, y_vals)
                
                if np.isscalar(y_vals):
                    y_vals=np.full_like(x_vals,y_vals)
                
                fig,ax=plt.subplots(figsize=(8,5))
                ax.plot(x_vals,y_vals, color=line_color,linewidth=2,label=f"f(x) = {func_input}")
                
                ax.axhline(0,color='black',linewidth=1)
                ax.axvline(0,color="black", linewidth=1)#im the alpha
                
                ax.set_xlabel("x")
                ax.set_ylabel("f(x)")
                ax.set_title(f"graph of f(x)={func_input}")
                ax.legend(loc="upper left")
                
                st.pyplot(fig)
                with st.expander("view tabel"):
                    sample_indices = np.linspace(0, len(x_vals) - 1, 11, dtype=int)
                    df_coords = pd.DataFrame({
                        "x": np.round(x_vals[sample_indices], 3),
                        "f(x)": np.round(y_vals[sample_indices], 3)
                    })
                    st.dataframe(df_coords, use_container_width=True)
            
            except Exception as e:
                st.error("your functions invalid:", str(e))


#==========================Music visualizer because i saw a cool one on reels and wanna copy it ok :skull: im cookeed=================================

elif mode=="music visualizer":
    st.subheader("Retro music visualizer(and player!)")
    st.write("cool retro visualizer i totally didnt copy the entire design off a reel i saw earlier today no who would ever do that not me")
    st.write("Also one more thing for some reason it worked with like half the files i tried and not the other half i have no clue why but uh good luck!")
    
    import librosa
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    
    uploaded_audio=st.file_uploader("Upload mp3 or .wav but who uses .wav anyways and who actually pays for mp3s ahoy matey", type=["wav", "mp3"])
    if uploaded_audio is not None:
        st.audio(uploaded_audio)
        col1,col2=st.columns([1,2])
        
        with col1:
            num_bands=st.slider("how many colomns", 8,32,16)
            grid_height=st.slider("Eq height", 8,20,10)
            time_offset=st.slider("track time(secs)", 0.0,60.0,0.0, step=0.5)
        
        with col2:
            with st.spinner("Processing audio"):
                y,sr=librosa.load(uploaded_audio,sr=None,offset=time_offset, duration=0.1)
                
                if len(y)>0:
                    fft_spectrum=np.abs(np.fft.rfft(y))
                    band_split = np.array_split(fft_spectrum[:len(fft_spectrum)//2], num_bands)
                    band_amplitudes = [np.mean(band) if len(band) > 0 else 0 for band in band_split]

                    max_amp = max(band_amplitudes) if max(band_amplitudes) > 0 else 1
                    scaled_levels = [int((amp / max_amp) * grid_height) for amp in band_amplitudes]

                    
                    fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
                    ax.set_facecolor('black')

                    # i just realized i was wrong before i had 43 minutes left lol
                    def get_led_color(row, max_rows):
                        ratio = row / max_rows
                        #bottom
                        if ratio < 0.4: 
                            return (0.1, 0.85, 0.2)
                        #middle
                        elif ratio < 0.65:
                            return (0.8, 0.9, 0.1)
                        #like 2/3ds or something idk
                        elif ratio < 0.85: 
                            return (0.95, 0.5, 0.0)
                        #top black red is that brown idk im kinda tweaking rn my brain isnt in nthe right place
                        else:
                            return (0.5, 0.15, 0.05)

                    #drawing leds! vow so tuff i totally didnt have to search half this up on google cuz i had zero idea what to do lollolol
                    for col, level in enumerate(scaled_levels):
                        for row in range(grid_height):
                            if row < level:
                                color = get_led_color(row, grid_height)
                                alpha = 1.0
                            else:
                                color = get_led_color(row, grid_height)
                                alpha = 0.08 

                            rect = Rectangle(
                                (col * 1.2, row * 1.2), 
                                1.0, 1.0, 
                                facecolor=color, 
                                edgecolor='black', 
                                linewidth=1.5, 
                                alpha=alpha
                            )
                            ax.add_patch(rect)

                    ax.set_xlim(-0.5, num_bands * 1.2 + 0.5)
                    ax.set_ylim(-3, grid_height * 1.2 + 0.5)
                    ax.axis('off')

                    st.pyplot(fig)
                else:
                    st.warning("Selected audio segment is empty.")
            