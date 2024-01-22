import telebot
from telebot import types
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# Завантаження та підготовка даних
df = pd.read_csv('C:/Users/38098/Desktop/bot_mkr/Salary Data.csv')
df.fillna(0, inplace=True)
age = df['Age']  # Вік
years_of_experience = df['Years of Experience']  # Роки досвіду
salary = df['Salary']  # Зарплатня
X = np.column_stack((age, years_of_experience))
X_train, X_test, y_train, y_test = train_test_split(X, salary, test_size=0.2, random_state=0)

# Створення моделі лінійної регресії
model = LinearRegression()
model.fit(X_train, y_train)

bot = telebot.TeleBot('YOUR-TELEGRAMBOT-TOKEN')
WAITING_FOR_AGE = 1
WAITING_FOR_EXPERIENCE = 2
user_state = {}
user_data = {}
feedback_mode = False
user_id_to_notify = '259958572'  # ID автора для надсилання повідомлень

# Функції для створення клавіатур
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_mkr = types.KeyboardButton("Матеріали МКР 🛠️")
    button_salary = types.KeyboardButton("Прогнозування заробітньої плати 💰")
    keyboard.add(button_mkr, button_salary)
    return keyboard

def create_keyboard1():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_mkr1 = types.KeyboardButton("Підготовка датасету 📊")
    button_salary1 = types.KeyboardButton("Обчислення регресій різними методами 🧮")
    back = types.KeyboardButton("Назад ↩️")
    keyboard.add(button_mkr1, button_salary1, back)
    return keyboard

def create_analysis_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Датасет"),
        types.KeyboardButton("Гістограма частот"),
        types.KeyboardButton("Графік аналізу викидів"),
        types.KeyboardButton("Q-Q plot"),
        types.KeyboardButton("Залежність заробітньої плати від років досвіду"),
        types.KeyboardButton("Залежність заробітньої плати від віку"),
        types.KeyboardButton("Обчислення кореляцій"),
        types.KeyboardButton("Теплокарта кореляції"),
        types.KeyboardButton("Назад ↩️")
    ]
    keyboard.add(*buttons)
    return keyboard

def create_regression_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Random Forest"),
        types.KeyboardButton("Лінійна регресія"),
        types.KeyboardButton("Поліноміальна регресія"),
        types.KeyboardButton("Назад ↩️")
    ]
    keyboard.add(*buttons)
    return keyboard   

# Обробники команд
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Вітаю Вас! Оберіть потрібний Вам варіант нижче.", reply_markup=create_keyboard())
    
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Цей бот розроблений студентом групи КН-31 Ковальковським Віталієм.\nЙого призначення - наглядне розкриття сутті роботи.", reply_markup=create_keyboard())

@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
    global feedback_mode
    feedback_mode = True
    bot.send_message(message.chat.id, "Для зв'язку з автором введіть свою пропозицію,\nпитання або проблему опишіть нижче:", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: feedback_mode)
def handle_feedback_message(message):
    global feedback_mode
    bot.send_message(user_id_to_notify, f"Користувач (ID: {message.chat.id}) надіслав вам повідомлення:\n{message.text}")
    feedback_mode = False
    bot.send_message(message.chat.id, "Ваше повідомлення надіслано автору.", reply_markup=create_keyboard())

# Обробник текстових повідомлень
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    chat_id = message.chat.id

    if chat_id in user_state and user_state[chat_id] == WAITING_FOR_AGE:
        try:
            user_age = float(message.text)
            user_data[chat_id] = {'age': user_age}
            bot.send_message(chat_id, "Тепер введіть кількість років досвіду:")
            user_state[chat_id] = WAITING_FOR_EXPERIENCE
        except ValueError:
            bot.send_message(chat_id, "Будь ласка, введіть коректний вік.")
        return

    elif chat_id in user_state and user_state[chat_id] == WAITING_FOR_EXPERIENCE:
        try:
            user_experience = float(message.text)

        # Використання моделі для передбачення зарплати
            age = user_data[chat_id]['age']
            if age <= user_experience:
                bot.send_message(chat_id, "Роки досвіду не можуть бути більшими або дорівнювати вашим рокам! Введіть коректні значення досвіду.")
                user_state[chat_id] = WAITING_FOR_EXPERIENCE  # Повертаємо користувача до стану введення досвіду
            if (age == 0) or (user_experience == 0):# Виконати певні дії, якщо вік або досвід дорівню
                bot.send_message(chat_id, "Роки досвіду або вік не можуть дорівнювати 0!")
                user_state[chat_id] = WAITING_FOR_EXPERIENCE  # Повертаємо користувача до стану введення досвіду
            else:
                user_data[chat_id]['experience'] = user_experience
                predicted_salary = model.predict(np.array([[age, user_experience]]))
                
                bot.send_message(chat_id, f"На основі введених даних, прогнозована зарплатня: {predicted_salary[0]:.2f}")
            # Очистка даних користувача
                del user_state[chat_id]
                del user_data[chat_id]
        except ValueError:
            bot.send_message(chat_id, "Будь ласка, введіть коректну кількість років досвіду.")
        return

    if message.text == "Підготовка датасету 📊":
        bot.send_message(message.chat.id, "Оберіть опцію для аналізу даних:", reply_markup=create_analysis_keyboard())
        return
    
    elif message.text in ["Датасет", "Гістограма частот", "Графік аналізу викидів", "Q-Q plot", "Залежність заробітньої плати від років досвіду", "Залежність заробітньої плати від віку", "Обчислення кореляцій", "Теплокарта кореляції","Назад ↩️"]:
        # Тут ви можете додати логіку для відправлення відповідних фотографій
        # Наприклад:
        if message.text == "Датасет":
            bot.send_message(message.chat.id, "На фото ви бачите датасет для мого проекту")
            bot.send_photo(message.chat.id, open('df.png', 'rb'))
            return
        
        elif message.text == "Гістограма частот":
            bot.send_message(message.chat.id, "На фото ви бачите графік частотної залежності розміру заробітніх плат")
            bot.send_photo(message.chat.id, open('gistograma_valuefrequency.png', 'rb'))
            return
        
        elif message.text == "Графік аналізу викидів":
            bot.send_message(message.chat.id, "Визначаємо видити для заробітніх плат")
            bot.send_photo(message.chat.id, open('limits_salary.png', 'rb'))
            return
        
        elif message.text == "Q-Q plot":
            bot.send_message(message.chat.id, "На фото ви бачите Q-Q графік")
            bot.send_photo(message.chat.id, open('q-q_plot.png', 'rb'))
            return
        
        elif message.text == "Залежність заробітньої плати від років досвіду":
            bot.send_message(message.chat.id, "Графік залежності ЗП від років досвіду")
            bot.send_photo(message.chat.id, open('salary_years_of_experience.png', 'rb'))
            return
        
        elif message.text == "Залежність заробітньої плати від віку":
            bot.send_message(message.chat.id, "Графік залежності ЗП від віку")
            bot.send_photo(message.chat.id, open('salary_age.png', 'rb'))
            return
        
        elif message.text == "Обчислення кореляцій":
            bot.send_message(message.chat.id, "Обчислення кореляцій різними методами")
            bot.send_photo(message.chat.id, open('correlations.png', 'rb'))
            return
        
        elif message.text == "Теплокарта кореляції":
            bot.send_message(message.chat.id, "Матриця теплокарт кореляцій")
            bot.send_photo(message.chat.id, open('teplocard_correlations.png', 'rb'))      
            return
        
        elif message.text == "Назад ↩️":
            bot.send_message(message.chat.id, "Оберіть потрібний Вам варіант нижче.", reply_markup=create_keyboard())
            return
        
    if message.text == "Обчислення регресій різними методами 🧮":
        bot.send_message(message.chat.id, "Оберіть опцію:", reply_markup=create_regression_keyboard())
        return
    
    elif message.text in ["Random Forest","Лінійна регресія","Поліноміальна регресія","Назад ↩️"]:
        # Тут ви можете додати логіку для відправлення відповідних фотографій
        # Наприклад:
        if message.text == "Random Forest":
            bot.send_message(message.chat.id, "На фото ви бачите результати обчислення регресії ансамблевим методом")
            bot.send_photo(message.chat.id, open('randomforest.png', 'rb'))
            return
        
        elif message.text == "Лінійна регресія":
            bot.send_message(message.chat.id, "На фото ви бачите результати обчислення регресії лінійним методом")
            bot.send_photo(message.chat.id, open('lineal.png', 'rb'))   
            return
        
        elif message.text == "Поліноміальна регресія":
            bot.send_message(message.chat.id, "На фото ви бачите результати обчислення регресії поліноміальним методом")
            bot.send_photo(message.chat.id, open('polinomial.png', 'rb'))  
            return  
          

    elif message.text == "Матеріали МКР 🛠️":
        bot.send_message(message.chat.id, "Тут будуть матеріали МКР.", reply_markup=create_keyboard1())
        return
    
    elif message.text == "Прогнозування заробітньої плати 💰":
        bot.send_message(message.chat.id, "Введіть свій вік:")
        user_state[chat_id] = WAITING_FOR_AGE
        return
    
    elif message.text == "Назад ↩️":
        bot.send_message(message.chat.id, "Оберіть потрібний Вам варіант нижче.", reply_markup=create_keyboard())
        return
    

    else:
        bot.send_message(message.chat.id, "Я не розумію цю команду. Ви можете скористатися командою /help, щоб дізнатись про функціонал бота.")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
