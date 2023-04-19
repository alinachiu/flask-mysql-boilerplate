# NutriGuide

This repo contains a setup for spinning up 3 Docker containers for the NutriGuide Application: 
1. A MySQL 8 container to store data
2. A Python Flask container to implement a REST API
3. A Local AppSmith Server

NutriGuide is a nutrition-focused application that helps users find and create healthy recipes that fit their specific dietary needs and goals. With a database of thousands of recipes, the application allows users to filter their search based on ingredients, cuisine, dietary restrictions, or meal type. The service provides nutritional information for each recipe, including calories, macronutrients, and micronutrients, to help users make informed choices. It also gives the opportunities for dietitians and nutritionists to provide guidance and advice on the type of diet to follow based on your goals. Nutritionists can give general advice, or refer to a specific diet.  The problems that Nutriguide aims to solve are primarily to provide a comprehensive and customizable solution for users who want to eat healthily, save time, and achieve their dietary goals. Additionally, allow users to be connected to experts in the subject who can provide a unique solution for users who want to track their nutritional intake and ensure they are meeting their daily nutritional needs. 

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
2. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
3. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
4. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
5. Build the images with `docker compose build`
6. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

Access the webserver through http://localhost:8001/. Access Appsmith via our appsmith repo (linked for convenience: https://github.com/alinachiu/appsmith-repo) or via http://localhost:8080/
