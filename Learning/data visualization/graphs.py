#learned pandas and matplotlib

import matplotlib.pyplot as plt
'''
x=[5,7,2,4,3]
y=[2,9,0,3,6]
plt.plot(x,y,"go")
plt.show()
'''
'''
#piechart

ingredients=["dough", "sauce", "cheese", "peperoni", "olives"]
data=[30,5,30,20,15]
colors=['red','orange','yellow','green','blue']
explosions=[0,1,0,0.5,0]
autopct='%1.2f%%'
plt.pie(data,labels=ingredients, shadow=True, colors=colors, explode=explosions,autopct=autopct)
plt.show()'''

'''#bargraph
years=[2004,2008,2012,2016]
michaelphelps=[1,8,3,4]
markspitz=[2,4,7,3]
plt.bar(years,michaelphelps, alpha=0.5, label="Phelps", color='blue')
plt.bar(years,markspitz, alpha=0.5, label="Spitz",color="green")
plt.legend()
plt.show()
'''
'''
#histogram

movieratings=[4,3,3,4,5,1,2,1,3,4]
bins=[0,1,2,3,4,5,6]
plt.hist(movieratings,bins, rwidth=0.5)
plt.show()
'''
# filex=open("x.txt","r")
# filey=open("y.txt","r")
# xvals=[]
# yvals=[]
# for lines in filex:
#     xvals.append(lines)
# for lines in filey:
#     yvals.append(lines)
# plt.plot(xvals,yvals,'bh')
# plt.show()

# file=open("xy.txt","r")
# xvals=[]
# yvals=[]
# for line in file:
#     line=line.strip()
#     line=line.split(",")
#     xvals.append(int(line[0]))
#     yvals.append(int(line[1]))
# print (xvals)
# print (yvals)
# plt.plot(xvals,yvals,'bh')
# plt.show() 

# import pandas as pd
# file=pd.read_csv("xy.txt")
# xvals=list(file["x"])
# yvals=list(file["y"])
# print (xvals)
# print (yvals)
# plt.plot(xvals,yvals,'bh')
# plt.show() 

# import pandas as pd
# file=pd.read_csv("hobby.txt")
# dict={}
# names=list(file["name"])
# hobbies=list(file["hobby"])
# for i in hobbies:
#     if i.strip() not in dict:
#         dict[i.strip()]=1
#     else:
#         dict[i.strip()]=dict[i.strip()]+1
# hobbylist=list(dict.keys())
# hobbyamounts=list(dict.values())    
# autopct='%1.2f%%'

# plt.pie(hobbyamounts, labels=hobbylist, autopct=autopct)
# plt.show()
