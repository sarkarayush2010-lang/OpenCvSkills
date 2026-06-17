#this took me longer than 3 hours please help me
#
import cv2
import numpy as np
import streamlit as st
from PIL import Image

#===========================================Basic image Layout ========================================

st.set_page_config(page_title="Cv2 stuff!", layout="wide")
st.title("I learned image processing with open cv")
st.markdown("Here are some of the things I can do!")
st.markdown("Streamlit sidebar for navigation, chose image filters or live video effects!")


st.sidebar.header("Source")
mode = st.sidebar.radio("Choose Media Type:", ["Image Filters", "Live Filters"])

kernel = np.ones((5, 5), np.uint8)

#==============================================Mode 1 - static image =====================================

if mode == "Image Filters":
    st.subheader("Image filters!")
    uploaded_file = st.file_uploader("Upload any png, jpg jpeg", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        col1, col2 = st.columns(2)
        with col1:
            # FIX: Updated width parameter to remove warnings
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Image", width="stretch")
            
        with col2:
            filter_choice = st.selectbox(
                "Select Transformation Engine: ",
                [
                    "Original printed Matrix",
                    "resized image",
                    "Grayscale",
                    "Black and white",
                    "eroded",
                    "Dialated",
                    "Inverse (black and white)",
                    "Add Shapes",
                    "Caption",
                    "Contour"
                ]
            )
            
            if filter_choice == "Original printed Matrix":
                st.write("Raw pixel array")
                st.code(str(img))
                st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), width="stretch")
            elif filter_choice == "resized image":
                resized=cv2.resize(img,(640,480))
                st.image(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB), caption="Resized image!")
            elif filter_choice == "Grayscale":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                st.image(gray, caption="Grayscale", clamp=True, width="stretch")
                
            elif filter_choice == "Black and white":
                thresh_val=st.slider("Set contrast needed for it to be black: ",0,255,150)
                gray_base = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, b_w = cv2.threshold(gray_base, thresh_val, 255, cv2.THRESH_BINARY)
                st.image(b_w, caption="Black and White", clamp=True, width="stretch")
                
            elif filter_choice == "eroded":
                eroded = cv2.erode(img, kernel, iterations=1)
                st.image(cv2.cvtColor(eroded, cv2.COLOR_BGR2RGB), caption="Eroded View", width="stretch")
                
            elif filter_choice == "Dialated":
                dialated = cv2.dilate(img, kernel, iterations=1)
                st.image(cv2.cvtColor(dialated, cv2.COLOR_BGR2RGB), caption="Dialated view", width="stretch")
            
            elif filter_choice == "Inverse (black and white)":
                thresh_val=st.slider("Set contrast needed for it to be black: ",0,255,150)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, b_w = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
                inverted = cv2.bitwise_not(b_w)
                st.image(inverted, caption="Inverted Black and White", clamp=True, width="stretch")

            elif filter_choice == "Add Shapes":
                annotated = img.copy()
                h, w, _ = annotated.shape
                cv2.rectangle(annotated, (int(w*0.05), int(h*0.05)), (int(w*0.3), int(h*0.3)), (0, 255, 0), 3)
                cv2.line(annotated, (int(w*0.05), int(h*0.9)), (int(w*0.3), int(h*0.7)), (255, 0, 0), 3)
                cv2.circle(annotated, (int(w*0.7), int(h*0.2)), int(min(w, h)*0.1), (0, 0, 255), 3)
                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), width="stretch")
                
            elif filter_choice == "Caption":
                text_img = img.copy()
                h, w, _ = text_img.shape
                cv2.putText(text_img, "Hello World", (int(w*0.1), int(h*0.5)), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 4)
                st.image(cv2.cvtColor(text_img, cv2.COLOR_BGR2RGB), caption="Captioned Image", width="stretch")
                
            elif filter_choice == "Contour":
                contour_img = img.copy()
                gray = cv2.cvtColor(contour_img, cv2.COLOR_BGR2GRAY)
                _, b_w = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
                contours, _ = cv2.findContours(b_w.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(contour_img, contours, -1, (0, 255, 150), 3)
                for cntr in contours:
                    bx, by, bw, bh = cv2.boundingRect(cntr)
                    cv2.rectangle(contour_img, (bx-10, by-10), (bx+bw+10, by+bh+10), (0, 255, 0), 2)
                st.image(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB), caption="Contour Boxes", width="stretch")
    else:
        st.info("Drop in an image file to the uploader first!")
        
        
        
        
#==============================================Mode 2 - video =====================================

elif mode == "Live Filters":
    st.subheader("Live video effects! yayyayayay")
    
    # Move the pipeline selector to the main page area for a cleaner layout
    live_filter = st.selectbox(
        "Select Active Pipeline:",
        [
            "regular video", 
            "Line filter",
            "Threshold Matrix",
            "Slicing",
            "make half red"
        ]
    )
    
    # Keep the custom speed modifier in the sidebar if the line filter is active
    speed = st.sidebar.slider("Line Speed", 1, 12, 4) if live_filter == "Line filter" else 0
    run_cam = st.checkbox("< -- click here to give me FULL control over your camera (dont worry it only enables the program to see your camera lol its not dangerous i think)")
    
    # CRITICAL: Create the two stable side-by-side layout columns *before* the loop starts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("###Original Live Feed")
        LIVE_CONTAINER = st.image([])
        
    with col_right:
        st.markdown(f"###Applied Effect: {live_filter}")
        EFFECT_CONTAINER = st.image([])
    
    if run_cam:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        liney = 0
        canvas = None
        
        while run_cam:
            ret, frame = camera.read()
            if not ret:
                st.error("Error: Camera stream stopped working")
                break
            
            raw_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            LIVE_CONTAINER.image(raw_rgb)
            
            if live_filter == "regular video":
                EFFECT_CONTAINER.image(raw_rgb)
                
            elif live_filter == "Threshold Matrix":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, blackf = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
                
                # Stack the gray and binary frames side-by-side for the effect column
                gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                bin_3ch = cv2.cvtColor(blackf, cv2.COLOR_GRAY2BGR)
                matrix_strip = np.hstack((gray_3ch, bin_3ch))
                
                EFFECT_CONTAINER.image(cv2.cvtColor(matrix_strip, cv2.COLOR_BGR2RGB))
                
            elif live_filter == "Slicing":
                roi = frame[0:480, 0:320]
                EFFECT_CONTAINER.image(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
                
            elif live_filter == "make half red":
                overwritten = frame.copy()
                overwritten[0:480, 0:320] = (0, 0, 255)
                EFFECT_CONTAINER.image(cv2.cvtColor(overwritten, cv2.COLOR_BGR2RGB))
                
            elif live_filter == "Line filter":
                if canvas is None or canvas.shape != frame.shape:
                    canvas = frame.copy()
                    
                canvas[liney:liney+speed, :] = frame[liney:liney+speed, :]
                display_frame = frame.copy()
                if liney > 0:
                    display_frame[0:liney, :] = canvas[0:liney, :]
                    
                cv2.line(display_frame, (0, liney), (frame.shape[1], liney), (255, 50, 50), 2)
                
                liney += speed
                if liney >= frame.shape[0]:
                    liney = 0
                    canvas = frame.copy()
                    
                EFFECT_CONTAINER.image(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB))
                
        camera.release()
    else:
        st.warning("Camera hardware module doesnt exist, plug it back in now. or your computers bugged")