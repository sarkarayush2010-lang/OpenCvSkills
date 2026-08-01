'''
import numpy as np
import pandas as pd

file=pd.read_csv("population_total_long.csv")

yearandcount=file.groupby(["Year"])["Count"].sum()

yearandcount=yearandcount.reset_index()

year=yearandcount["Year"]
count=yearandcount["Count"]

yeararray=np.array(year).reshape(-1,1)
countarray=np.array(count)

print(yeararray)




homework

predict world population in 2030


'''



# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression

# file = pd.read_csv("population_total_long.csv")

# us_data = file[file['Country Name'] == 'United States'] 

# year_and_count = us_data.groupby(["Year"])["Count"].sum().reset_index()

# X = np.array(year_and_count["Year"]).reshape(-1, 1)
# y = np.array(year_and_count["Count"])

# model = LinearRegression()
# model.fit(X, y)

# year_2030 = np.array([[2030]])
# predicted_2030 = model.predict(year_2030)

# print("Poopulation in 2030: "+str(predicted_2030[0]))
# plt.scatter(X, y, color="blue", alpha=0.7, label="Historical Data")
# plt.plot(X, model.predict(X), color="red", linewidth=2, label="Regression Line")
# plt.scatter(2030, predicted_2030, color="green", marker="*", s=200, label="2030 Prediction")

# plt.xlabel("Year")
# plt.ylabel("Population")
# plt.legend()
# plt.show()





# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression

# file = pd.read_csv("population_total_long.csv")

# #us_data = file[file['Country Name'] == 'United States'] 

# year_and_count = file.groupby(["Year"])["Count"].sum().reset_index()

# X = np.array(year_and_count["Year"]).reshape(-1, 1)
# y = np.array(year_and_count["Count"])

# model = LinearRegression()
# model.fit(X, y)

# year_2030 = np.array([[2030]])
# predicted_2030 = model.predict(year_2030)

# print("Poopulation in 2030: "+str(predicted_2030[0]))
# plt.scatter(X, y, color="blue", alpha=0.7, label="Historical Data")
# plt.plot(X, model.predict(X), color="red", linewidth=2, label="Regression Line")
# plt.scatter(2030, predicted_2030, color="green", marker="*", s=200, label="2030 Prediction")

# plt.xlabel("Year")
# plt.ylabel("Population")
# plt.legend()
# plt.show()



