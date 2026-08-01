# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# from sklearn import neighbors


# file=pd.read_csv("iris.data")

# inputs=file.drop(["class"],axis=1)

# outputs=file["class"]

# inputs=np.array(inputs)
# outputs=np.array(outputs)

# #print(inputs.shape, "\n", outputs.shape)

# traindata,testdata,trainlabels,testlabels=train_test_split(inputs,outputs,test_size=0.2)

# print(traindata.shape, "\n", testdata.shape)

# model=neighbors.KNeighborsClassifier()
# model.fit(traindata,trainlabels)

# predictions=model.predict(testdata)
# print(predictions)
# accuracy=model.score(testdata,testlabels)
# print(accuracy)

#=========================Cancer one
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# from sklearn import neighbors



# file = pd.read_csv("breast-cancer-wisconsin.data", na_values="?")
# file.dropna(inplace=True)

# inputs=file.drop(["class","samplenum"], axis=1)

# outputs=file["class"]

# inputs=np.array(inputs)
# outputs=np.array(outputs)

# traindata,testdata,trainlabels,testlabels=train_test_split(inputs,outputs,test_size=0.2)

# model=neighbors.KNeighborsClassifier()
# model.fit(traindata,trainlabels)

# predictions=model.predict(testdata)

# count=0
# for i in range(len(predictions)):
#     if predictions[i]==testlabels[i]:
#         count+=1
        
# print((count/len(predictions)) *100)

#========================processed hearet disease
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn import neighbors

file = pd.read_csv("processed.cleveland.data", names=[
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"
], na_values="?")

file.dropna(inplace=True)

inputs = file.drop(["num"], axis=1)
outputs = file["num"]

unchangedoutputs = list(file["num"])

binary = []
'''
couldnt figure this out, chatgpt just said that im supposed to replace my score thing with: 

outputs = (outputs > 0).astype(int) but that isnt working either


'''


# outputs = (outputs > 0).astype(int)


# for score in unchangedoutputs: #apparently anything but 0 is heart disease everything else isnt?
    
#     if int(score) > 0: 
#         binary.append(1) 
#     else:
#         binary.append(0)

# outputs = np.array(binary)

# inputs = np.array(inputs)
# outputs = np.array(outputs)

# traindata, testdata, trainlabels, testlabels = train_test_split(inputs, outputs, test_size=0.2)

# model = neighbors.KNeighborsClassifier()
# model.fit(traindata, trainlabels)

# predictions = model.predict(testdata)
# count = 0
# for i in range(len(predictions)):
#     if predictions[i] == testlabels[i]:
#         count += 1
        
# print((count / len(predictions)) * 100)




