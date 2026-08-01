import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
file=pd.read_csv("iris.data")

inputs=file.drop(["class"],axis=1)

outputs=file["class"]

inputs=np.array(inputs)
outputs=np.array(outputs)

#print(inputs.shape, "\n", outputs.shape)

traindata,testdata,trainlabels,testlabels=train_test_split(inputs,outputs,test_size=0.2)

print(traindata.shape, "\n", testdata.shape)

model=LogisticRegression()
model.fit(traindata,trainlabels)

predictions=model.predict(testdata)
print(predictions)

count=0
for i in range(len(predictions)):
    if predictions[i]==testlabels[i]:
        count+=1
        
print((count/len(predictions))*100)

# cm=confusion_matrix(testlabels,predictions)
# display=ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Iris-setosa","Iris-versicolor","Iris-virginica"])
# display.plot(cmap=plt.cm.Blues)
# plt.show()

ourdata=[[5.6,3.2,5.3,1.8]]
ourdata=np.array(ourdata)
print(ourdata.shape)


predictions=model.predict(ourdata)
print(predictions)


'''
homework

bigger dataset 

more important part is 11 collumns

columns may have missing data (question marks)


'''

# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# file = pd.read_csv("breast-cancer-wisconsin.data", na_values="?")
# file.dropna(inplace=True)

# inputs=file.drop(["class","samplenum"], axis=1)

# outputs=file["class"]

# inputs=np.array(inputs)
# outputs=np.array(outputs)

# traindata,testdata,trainlabels,testlabels=train_test_split(inputs,outputs,test_size=0.2)

# model=LogisticRegression(max_iter=1000)
# model.fit(traindata,trainlabels)

# predictions=model.predict(testdata)
# count=0
# for i in range(len(predictions)):
#     if predictions[i]==testlabels[i]:
#         count+=1
        
# print((count/len(predictions)) *100)