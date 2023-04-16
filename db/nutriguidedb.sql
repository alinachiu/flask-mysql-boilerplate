-- Create a new database called nutriguidedb
CREATE DATABASE nutriguidedb;

-- Set NutriGuideDB as the current database. All subsequent
-- commands will be executed in the context of NutriGuideDB
USE nutriguidedb;

CREATE TABLE User (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    height FLOAT,
    weight FLOAT,
    activity_level ENUM('Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extra Active')
);


CREATE TABLE HealthExpert (
    expert_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    years_of_experience INT NOT NULL,
    biography TEXT,
    degree VARCHAR(255) NOT NULL
);


CREATE TABLE NutritionalAdvice (
    post_id  INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    text_body TEXT NOT NULL,
    date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_1 FOREIGN KEY (author_id) REFERENCES HealthExpert(expert_id) ON DELETE CASCADE
);


CREATE TABLE Recipe (
    recipe_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    preparation_time TIME NOT NULL,
    cooking_time TIME NOT NULL,
    serving_size INT NOT NULL,
    image_url VARCHAR(255),
    source_url VARCHAR(255),
    calories INT,
    carbohydrates FLOAT,
    protein FLOAT,
    fat FLOAT,
    sodium FLOAT,
    fiber FLOAT,
    sugar FLOAT
);


CREATE TABLE Ingredient (
    ingredient_id INT PRIMARY KEY,
    ingredient_name VARCHAR(255) NOT NULL,
    calories INT NOT NULL,
    carbohydrates FLOAT,
    protein FLOAT,
    fat FLOAT,
    sodium FLOAT,
    fiber FLOAT,
    sugar FLOAT
);


CREATE TABLE RecipeIngredient (
    recipe_id INT,
    ingredient_id INT,
    quantity FLOAT NOT NULL,
    unit VARCHAR(50) NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id),
    CONSTRAINT fk_2 FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
    CONSTRAINT fk_3 FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE MealPlan (
    meal_plan_id INT PRIMARY KEY,
    user_id INT,
    dietitian_id INT,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT fk_4 FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_5 FOREIGN KEY (dietitian_id) REFERENCES HealthExpert(expert_id) ON DELETE CASCADE
);


CREATE TABLE Meal (
    meal_id INT PRIMARY KEY,
    meal_plan_id INT,
    recipe_id INT,
    meal_time TIME,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
    CONSTRAINT fk_6 FOREIGN KEY (meal_plan_id) REFERENCES MealPlan(meal_plan_id) ON DELETE CASCADE,
    CONSTRAINT fk_7 FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id)
);


CREATE TABLE DietaryRestriction (
    restriction_id INT PRIMARY KEY,
    restriction_name VARCHAR(50) NOT NULL
);


CREATE TABLE UserDietaryRestriction (
    user_id INT,
    restriction_id INT,
    PRIMARY KEY (user_id, restriction_id),
    CONSTRAINT fk_8 FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_9 FOREIGN KEY (restriction_id) REFERENCES DietaryRestriction(restriction_id)
);


CREATE TABLE RecipeDietaryRestriction (
    recipe_id INT,
    restriction_id INT,
    PRIMARY KEY (recipe_id, restriction_id),
    CONSTRAINT fk_10 FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
    CONSTRAINT fk_11 FOREIGN KEY (restriction_id) REFERENCES DietaryRestriction(restriction_id)
);


CREATE TABLE Goal (
    goal_id INT PRIMARY KEY,
    goal_name VARCHAR(50) NOT NULL
);


CREATE TABLE UserGoal (
    user_id INT,
    goal_id INT,
    PRIMARY KEY (user_id, goal_id),
    CONSTRAINT fk_12 FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_13 FOREIGN KEY (goal_id) REFERENCES Goal(goal_id)
);


INSERT INTO User (user_id, username, password, email, first_name, last_name, date_of_birth, gender, height, weight, activity_level) VALUES
(101, 'sara88', 'p@ssword', 'sara88@gmail.com', 'Sara', 'Johnson', '1988-03-15', 'Female', 165, 65, 'Moderately Active'),
(102, 'johnny92', 'john123', 'johnny92@yahoo.com', 'John', 'Doe', '1992-07-22', 'Male', 180, 80, 'Moderately Active');


INSERT INTO HealthExpert (expert_id, username, password, email, first_name, last_name, date_of_birth, gender, years_of_experience, biography, degree) VALUES
(201, 'mark.smith', 'expert@123', 'mark.smith@nutritionist.com', 'Mark', 'Smith', '1975-01-10', 'Male', 15, 'Mark is a registered dietitian and a certified specialist in sports dietetics with over 15 years of experience helping athletes and fitness enthusiasts optimize their performance through optimal nutrition. He holds a master’s degree in sports science and a Ph.D. in exercise physiology.', 'Ph.D. in Exercise Physiology'),
(202, 'jane.nutrition', 'jane456', 'jane.nutritionist@gmail.com', 'Jane', 'Johnson', '1980-06-05', 'Female', 10, 'Jane is a registered dietitian with over 10 years of experience helping people achieve their health and fitness goals through nutrition. She specializes in weight management and chronic disease prevention.', 'MS in Nutrition');


INSERT INTO NutritionalAdvice (author_id, title, text_body, date_posted) VALUES
(201, 'The Benefits of Eating Whole Grains', 'Incorporating whole grains into your diet can provide numerous health benefits such as reduced risk of heart disease and improved digestion. Try swapping out white bread for whole grain bread or substituting brown rice for white rice.', '2022-03-29'),
(202, 'The Importance of Hydration', 'Staying hydrated is essential for maintaining proper bodily functions and preventing dehydration. Aim to drink at least 8 cups of water per day, and more if you are engaging in physical activity.', '2022-03-30');


INSERT INTO Recipe (recipe_id, name, description, preparation_time, cooking_time, serving_size, image_url, source_url, calories, carbohydrates, protein, fat, sodium, fiber, sugar) VALUES
(026, 'Grilled Chicken with Roasted Vegetables', 'This simple and healthy recipe features grilled chicken breasts and a variety of colorful roasted vegetables. Perfect for a quick and easy weeknight meal.', '15', '25', '4', 'https://example.com/grilled-chicken.jpg', 'https://example.com/grilled-chicken-recipe', 350, 10, 25, 8, 300, 5, 3),
(027, 'Vegetarian Chili', 'This hearty and flavorful chili is packed with protein and fiber from a variety of beans and vegetables. Perfect for a cozy winter meal.', '20', '30', '6', 'https://example.com/vegetarian-chili.jpg', 'https://example.com/vegetarian-chili-recipe', 250, 30, 20, 5, 400, 10, 8);


INSERT INTO Ingredient (ingredient_id, ingredient_name, calories, carbohydrates, protein, fat, sodium, fiber, sugar) VALUES
(046, 'Chicken Breast', 110, 0, 26, 1, 45, 0, 0),
(057, 'Broccoli', 55, 10, 4, 1, 30, 4, 2),
(011, 'Red Bell Pepper', 30, 6, 1, 0, 0, 2, 3);


INSERT INTO RecipeIngredient (recipe_id, ingredient_id, quantity, unit)
VALUES (026, 046, 2, 'cups'),
      (027, 057, 1, 'tablespoon');


INSERT INTO MealPlan (meal_plan_id, user_id,dietitian_id, start_date, end_date) VALUES
(001, 101,201, '2023-04-01', '2023-04-07'),
(002, 102,202, '2023-04-01', '2023-04-07');


INSERT INTO Meal (meal_id, meal_plan_id, recipe_id, meal_time) VALUES
(001, 001, 026, '2023-04-01 12:00:00'),
(002, 001, 026, '2023-04-01 18:00:00'),
(003, 002, 026, '2023-04-01 12:00:00'),
(004, 002, 027, '2023-04-01 18:00:00');


INSERT INTO DietaryRestriction (restriction_id, restriction_name)VALUES
(150, 'Nuts'),
(200, 'Vegetarian');




INSERT INTO UserDietaryRestriction (user_id, restriction_id) VALUES
(101, 150),
(102, 200);




INSERT INTO RecipeDietaryRestriction (recipe_id, restriction_id)
VALUES (027, 200),
      (026, 150);


-- Insert two rows into the Goal table
INSERT INTO Goal (goal_id, goal_name)
VALUES (540, 'Weight loss'),
      (240, 'Muscle gain');


-- Insert two rows into the UserGoal table
INSERT INTO UserGoal (user_id, goal_id)
VALUES (101, 540),
      (102, 240);

