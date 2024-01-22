# Salary Prediction Telegram Bot

# Introduction:
The Salary Prediction Telegram Bot utilizes a linear regression model to predict salaries based on age and years of experience. This interactive bot is designed to assist users in exploring and analyzing a salary dataset. Users can perform tasks such as data analysis, regression calculations, and receive predictions for their salary based on input parameters.

# Features:

Data Preparation: The bot loads a salary dataset ('Salary Data.csv') and handles missing values. It then splits the data into training and testing sets for model training.\

Linear Regression Model: Utilizes the scikit-learn library to create and train a linear regression model based on the input features (age and years of experience).\

Telegram Integration: Powered by the telebot library, the bot connects to the Telegram platform and responds to user commands.

# Interactive Commands:

/start: Greets users and presents options for further interaction.\
/help: Provides information about the bot and its functionalities.\
/feedback: Allows users to provide feedback, suggestions, or report issues to the bot's developer.

# Data Analysis Options:

Dataset Preparation: Allows users to explore dataset preparation options.\
Regression Analysis: Enables users to perform regression analysis using different methods.\
# Regression Analysis Options:

Random Forest: Displays results of regression calculation using the Random Forest method.\
Linear Regression: Presents results of regression calculation using the Linear Regression method.\
Polynomial Regression: Shows results of regression calculation using the Polynomial Regression method.\

# Visualization:

The bot supports visual aids, such as histograms, Q-Q plots, and dependency graphs, providing users with a clear understanding of the dataset.

# Dependencies:

telebot: Python library for building Telegram bots.\
numpy, pandas: Python libraries for data manipulation and analysis.\
scikit-learn: Python library for machine learning tasks.\

# Setup Instructions:

Install the required Python libraries: telebot, numpy, pandas, scikit-learn.\
Load the 'Salary Data.csv' dataset.\
Run the script to start the bot.\

# Usage:

Start a chat with the bot using the /start command.\
Explore dataset preparation or regression analysis options.\
Receive salary predictions based on age and years of experience.\
Provide feedback using the /feedback command.\

# Contact Information:
For further assistance or feedback, contact:
Telegram: @wnezoxq

# Disclaimer:
This project is designed for educational purposes and may not be suitable for production use. The predictions are generated based on the linear regression model trained on the provided dataset. Users are encouraged to use the bot responsibly and understand the limitations of regression models. Also, this project is a term paper, so its use for similar purposes is a violation of academic integrity.
