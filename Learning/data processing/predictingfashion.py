import cv2
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import load_model

model = load_model("fashionmodel.h5")
offset = 20

class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
] 

# image = cv2.imread("blank-t-shirt-png-16.jpg")
#image = cv2.imread("nikeshoe.webp")
image = cv2.imread("shirt.webp")


# image=cv2.resize(image,(640,480))
greyimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold, blackandwhiteimage = cv2.threshold(greyimage, 100, 255, cv2.THRESH_BINARY_INV)

contours, hirearchy = cv2.findContours(blackandwhiteimage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 255, 150), 3)

for cntr in contours:
    x, y, w, h = cv2.boundingRect(cntr)
    if w > 5 and h > 10:
        y1, y2 = max(0, y - offset), min(blackandwhiteimage.shape[0], y + h + offset)
        x1, x2 = max(0, x - offset), min(blackandwhiteimage.shape[1], x + w + offset)
        
        digit_crop = blackandwhiteimage[y1:y2, x1:x2]

        resized = cv2.resize(digit_crop, (28, 28))
        reshaped_images = np.reshape(resized, (1, 28, 28))
        normalized_image = reshaped_images / 255.0

        predictions = model.predict(normalized_image)
        highestindex = np.argmax(predictions[0])
        
        label_text = class_names[highestindex]
        print(f"Predicted: {label_text} (Index {highestindex})")

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label_text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

cv2.imshow("normal", image)
cv2.imshow("bandw", blackandwhiteimage)

cv2.waitKey(0)
cv2.destroyAllWindows()