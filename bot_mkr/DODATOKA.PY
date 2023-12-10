import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
import re
import statsmodels.api as sm

sns.set(style="darkgrid")
df = pd.read_excel('/content/drive/MyDrive/Salary_Data.xlsx')
display(df)

df.info()

print("Кількість рядків, що повторяється", df[df.duplicated()].shape)

print("Кількість рядків з нульовими значенями", df[df.isnull()].shape)

a = df['salary']

mean = np.mean(a)
median = np.median(a)
mode = stats.mode(a)
varience = np.var(a)
std_deviation = np.std(a)

print(f"Середнє: {mean:.2f}")
print(f"Мода: {mode}")
print(f"Дисперсія: {varience:.2f}")
print(f"Стандартне відхилення: {std_deviation:.2f}")

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(a[a > 30000], bins=20, edgecolor='k')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Гістограма')

plt.show()

plt.subplot(2, 1, 2)
stats.probplot(a, dist="norm", plot=plt)
plt.title('Q-Q plot')

plt.show()

pearson_corr = df.corr(method='pearson')
spearman_corr = df.corr(method='spearman')
kendall_corr = df.corr(method='kendall')

print("Кореляція Пірсона:")
print(pearson_corr,'\n')
print("Кореляція Спірмена:")
print(spearman_corr, '\n')
print("Кореляція Кендала:")
print(kendall_corr,'\n')

corr_matrix = df.corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix, annot = True, cmap='coolwarm', linewidths=0.5)
plt.title('Теплокарта кореляції')
plt.show()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Завантаження даних
# df = pd.read_csv("Salary Data.csv")  # Переконайтеся, що ви завантажили ваш датасет
# Вибірка ознак та цільової змінної
columns_to_drop = ["age", "years_of_experience", "emotional_satisfaction", "gender", "job_title", "education_level","date"]
X = df.drop(columns=columns_to_drop, axis=1)  # Ознаки (всі стовпці, крім вищезазначених)
y = df["salary"]  # Цільова змінна (salary)


# Розділення на навчальний та тестовий набори
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

# Створення та навчання моделі Випадковий ліс
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Прогнози для тестового набору
y_pred = rf_model.predict(X_test)

# Оцінка якості прогнозу
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("За ансамблевим методом (випадкового лісу): ")
print(f"Середньоквадратична похибка (MSE): {mse}")
print(f"Коефіцієнт детермінації (R^2): {r2}")

columns_to_drop = ["age", "years_of_experience", "emotional_satisfaction", "gender", "job_title", "education_level","date"]
X_m = df.drop(columns=columns_to_drop, axis=1)  # Ознаки (всі стовпці, крім вищезазначених)
y_m = df["salary"]  # Цільова змінна (salary)

X_train_sm_m = sm.add_constant(X_m)
lr_m = sm.OLS(y_m, X_train_sm_m).fit()

lr_m.params

print(lr_m.summary())


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Завантаження даних
# df = pd.read_csv("Salary Data.csv")  # Переконайтеся, що ви завантажили ваш датасет

# Вибірка ознак та цільової змінної
columns_to_drop = ["age", "years_of_experience", "emotional_satisfaction", "gender", "job_title", "education_level", "date"]
X = df.drop(columns=columns_to_drop, axis=1)  # Ознаки (всі стовпці, крім вищезазначених)
y = df["salary"]  # Цільова змінна (salary)

# Розділення на навчальний та тестовий набори
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Створення поліноміальних ознак
poly = PolynomialFeatures(degree=2)  # Задайте бажаний ступінь полінома (у цьому випадку 2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Побудова поліноміальної регресії
poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)

# Прогнози для тестового набору
y_pred_poly = poly_model.predict(X_test_poly)

# Оцінка якості прогнозу
mse_poly = mean_squared_error(y_test, y_pred_poly)
r2_poly = r2_score(y_test, y_pred_poly)

print(f"Середньоквадратична похибка (MSE) для поліноміальної регресії: {mse_poly}")
print(f"Коефіцієнт детермінації (R^2) для поліноміальної регресії: {r2_poly}")


import pandas as pd

# Завантаження даних та встановлення індексу на дати

df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)


train_size = int(len(df) * 0.8)
train_data = df.iloc[:train_size]
test_data = df.iloc[train_size:]


import statsmodels.api as sm

p = 1
d = 1
q = 1
P = 1
D = 1
Q = 1
s = 8  # Наприклад, щомісячна сезонність


model = sm.tsa.SARIMAX(train_data['salary'], order=(p, d, q), seasonal_order=(P, D, Q, s))
results = model.fit()


forecast = results.get_forecast(steps=len(test_data))
forecast_mean = forecast.predicted_mean
