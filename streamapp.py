#this took me longer than 4 hours please help me
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
st.markdown("Also learned numpy and pandas, you can upload your own csvs or txt files and visualize them in the \"Data Visualization\" tab!")
st.markdown("Seems to be a bug with streamlit publishing. The videos are all blue(no idea how to fix lol) but also for the video filters, you have to reload the page, navigate to the filter you want, then press start each time you want to do a new filter.")

st.sidebar.header("Source")
mode = st.sidebar.radio("Choose Media Type:", ["Image Filters", "Live Filters", "Data Visualization"])

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
                st.image(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB), caption="Resized image!", width="stretch")
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
        st.info("Drop in an image to the uploader thingy first!")
        
        
        
#==============================================Mode 2 - video =====================================

elif mode == "Live Filters":
    st.subheader("Live video effects! yayyayayay")
    
    
    from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

    live_filter = st.selectbox(
        "Select Active Effect:",
        [
            "regular video", 
            "Line filter",
            "Threshold Matrix",
            "Slicing",
            "make half red"
        ]
    )
    
    speed = st.sidebar.slider("Line Speed", 1, 12, 4) if live_filter == "Line filter" else 0
    live_thresh = st.slider("Binary contrast threshold", 0, 255, 80) if live_filter == "Threshold Matrix" else 80

    class VideoProcessor(VideoProcessorBase):
        def __init__(self):
            self.liney = 0
            self.canvas = None
            #hiosjaifj

        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")
            
            if live_filter == "regular video":
                out_frame = img
                
            elif live_filter == "Threshold Matrix":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, blackf = cv2.threshold(gray, live_thresh, 255, cv2.THRESH_BINARY_INV)
                gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                bin_3ch = cv2.cvtColor(blackf, cv2.COLOR_GRAY2BGR)
                out_frame = np.hstack((gray_3ch, bin_3ch))
                
            elif live_filter == "Slicing":
                out_frame = img[0:480, 0:320]
                
            elif live_filter == "make half red":
                out_frame = img.copy()
                out_frame[0:480, 0:320] = (0, 0, 255)
                
            elif live_filter == "Line filter":
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
            
            import av
            return av.VideoFrame.from_ndarray(out_frame, format="rgb24")

    webrtc_streamer(key="opencv-filter-streamer", video_processor_factory=VideoProcessor)
        
#==============================================Mode 3 - Data Analytics Sandbox =====================================
elif mode=="Data Visualization":
    st.subheader("Pandas and Matplotlib visualizer thing")
    st.markdown("")
    import pandas as pd
    import matplotlib.pyplot as plt
    uploaded_data=st.file_uploader("Upload a csv or txt NOTHING ELSE IT DOESNT WORK: ", type = ["csv","txt"])
    if uploaded_data is not None:
        if uploaded_data.name.endswith('.txt'):
            df=pd.read_csv(uploaded_data, sep=None, engine="python")
        else:
            df=pd.read_csv(uploaded_data)
        st.markdown("Pandas data array matrix")
        
        if df is not None:
            st.markdown("Pandas matrix")
            st.dataframe(df,use_container_width = True)
            st.caption(f"shape matrix dimensions side x: {df.shape[0]} rows by side y {df.shape[1]} columns")
            st.markdown("---")
            st.markdown("Matplotlib renders") 
            chart_type=st.selectbox(
                "What plot visualization?",
                [
                    "line/scatter plot", 
                    "Pie chart generator",
                    "double bar graph comparison",
                    "histogram"
                 ]

            )   
            all_columns=list(df.columns)
            fig,ax=plt.subplots()
            if chart_type =="line/scatter plot":
                col_x=st.selectbox("Whats the x axis", all_columns, index=0)
                col_y=st.selectbox("whats the y axis", all_columns, index=min(1,len(all_columns)-1))
                markercolor = st.selectbox("What color marker", ["green", "red", "blue"])
                markershape = st.selectbox("what shape", ["o (circle)", "h (hexagon)", "- (line)", "p (pentagon)", "s (square)"])
                marker=markercolor[0]+markershape[0]
                
                ax.plot(df[col_x], df[col_y], marker)
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                st.pyplot(fig)
                
            elif chart_type=="Pie chart generator":
                label_col = st.selectbox("Select Category (like ingredient, hobby, ect):", all_columns)
                value_col = st.selectbox("Select quantitative values ", all_columns)
                
                ax.pie(df[value_col], labels=df[label_col], autopct='%1.2f%%', shadow=True)
                st.pyplot(fig)
            elif chart_type=="double bar graph comparison":
                x_axis_col = st.selectbox("Select Independent Variable (years, time, amount):", all_columns)
                series_1 = st.selectbox("Select group 1:", all_columns)
                series_2 = st.selectbox("Select group 2:", all_columns)
                
                ax.bar(df[x_axis_col], df[series_1], alpha=0.5, label=series_1, color='blue')
                ax.bar(df[x_axis_col], df[series_2], alpha=0.5, label=series_2, color='green')
                ax.set_xlabel(x_axis_col)
                ax.legend()
                st.pyplot(fig)
            
            elif chart_type== "histogram":
                data_col = st.selectbox("Select Numeric Column (like amazon ratings or sum):", all_columns)
                bin_count = st.slider("Select quantity partitions", 3, 20, 6)
                
                ax.hist(df[data_col], bins=bin_count, rwidth=0.8, color='purple', alpha=0.7)
                ax.set_ylabel("Frequency Counts")
                ax.set_xlabel(data_col)
                st.pyplot(fig)
            else:
                st.info("Put in csv or or an xy coordinate text file OR ELSE IT WONT WORK")