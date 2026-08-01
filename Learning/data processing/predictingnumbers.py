import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
import keras
from keras.models import load_model

model=load_model("numbermodel.h5")
offset=20


key=[6,7,9,3,5,8,7,4,1,6,0,2,4,3]
#thing i took from imageprocessing.py
image = cv2.imread("photo1.jpg")
greyimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold, blackandwhiteimage = cv2.threshold(greyimage, 80, 255, cv2.THRESH_BINARY_INV)

contours, hirearchy = cv2.findContours(blackandwhiteimage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 255, 150), 3)

count=0
for cntr in contours:
    x, y, w, h = cv2.boundingRect(cntr)
    if w > 5 and h > 10:
        cv2.rectangle(image, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 255, 0), 3)
        digit_crop = blackandwhiteimage[y-offset:y+h+offset, x-offset:x+w+offset]
        resized = cv2.resize(digit_crop, (28, 28))
        reshaped_images=np.reshape(resized,(1,28,28))
        normalized_image=reshaped_images/255
        predictions=model.predict(normalized_image)
        #print(predictions)
        highestindex=np.argmax(predictions[0])
        print(highestindex)
        cv2.putText(image, str(highestindex), (x , y ), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
    

cv2.imshow("normal",image)
cv2.imshow("bandw", blackandwhiteimage)

cv2.waitKey()
cv2.destroyAllWindows()


        
        
#         # #predictions
#         # prediction = model.predict(digit_input, verbose=0)
#         # predicted_digit = np.argmax(prediction)
        
        
#         cv2.putText(image, str(predicted_digit), (x - 20, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
#         print("supposed to be :",key[count],"Predicted: , ", predicted_digit)
#         count+=1

# plt.figure(figsize=(8, 12))
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# plt.show()




