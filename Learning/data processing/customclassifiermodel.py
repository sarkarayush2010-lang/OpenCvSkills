import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

main_folder="images"
#print(os.listdir())

subcategories=["pens","picks"]
allimages=[]
alllabels=[]


for subcategory in subcategories:
    pathtofolder=os.path.join(main_folder,subcategory)
    # print(pathtofolder)
    filesinfolder=os.listdir(pathtofolder)
    # print(filesinfolder)
    for file in filesinfolder:
        pathtofile=os.path.join(pathtofolder,file)
        image=cv2.imread(pathtofile)
        image=cv2.resize(image,(120,120))
        
        greyimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        allimages.append(greyimage)
        value=-1
        if subcategory=="pens":
            value=0
        elif subcategory=="picks":
            value=1
        alllabels.append(value)
        

        # cv2.imshow(subcategory,image)
        
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        

alllabels=np.array(alllabels)
allimages=np.array(allimages)
print(allimages.shape)   
        
trainimages,testimages,trainlabels,testlabels=train_test_split(allimages,alllabels,test_size=0.2)
