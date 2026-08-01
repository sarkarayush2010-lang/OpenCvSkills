import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


x=np.linspace(1,10,50).reshape(-1,1)
y=np.linspace(1,10,50)+np.random.random(50)
# print(x)
# print(y)


# plt.scatter(x,y,alpha=0.7)
# plt.show()


model=LinearRegression()

model.fit(x,y)

y_predict=model.predict(x)
print(y_predict)

plt.scatter(x,y,alpha=0.7)

print(model.coef_, model.intercept_)

value=model.predict([[20]])
value = model.predict([[20]])

y_predict = np.append(y_predict, value)
x = np.append(x, [[20]], axis=0)


plt.plot(x,y_predict, color="red", linewidth=1)

print(value)


plt.show()