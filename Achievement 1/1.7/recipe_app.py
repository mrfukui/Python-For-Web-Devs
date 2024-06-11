from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Engine object that connects to database
engine = create_engine("mysql://cf-python:password@localhost/my_database")

# Create declarative base which all classes inherit from
Base = declarative_base()


# Define Recipe class
class Recipe(Base):

    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Quick representation of the recipe
    def __repr__(self):
        return (
            "Recipe ID: "
            + str(self.id)
            + ", Name: "
            + self.name
            + ", Difficulty: "
            + self.difficulty
        )

    # Well-formatted version of the recipe
    def __str__(self):
        ingredients_list = self.ingredients.split(", ")
        formatted_ingredients = "\n".join(
            f"- {ingredient.strip()}" for ingredient in ingredients_list
        )
        recipe = (
            f"\nRecipe Name: {self.name}\n"
            f"Cooking time (min): {self.cooking_time}\n"
            f"Ingredients:\n{formatted_ingredients}\n"
            f"Difficulty: {self.difficulty}"
        )
        return recipe

    # Calculates difficulty level of a recipe
    def calculate_difficulty(self):

        num_of_ingredients = len(self.ingredients.split(", "))

        if self.cooking_time < 10 and num_of_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_of_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_of_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_of_ingredients >= 4:
            self.difficulty = "Hard"


# Create all defined tables in database
Base.metadata.create_all(engine)

# Generate session class and bind to engine
Session = sessionmaker(bind=engine)

# Initialize session as object
session = Session()


def create_recipe():
    # Collecting and validating recipe name
    while True:
        name = input("Enter the recipe name: ")
        if len(name) <= 50 and name.isalnum():
            break
        else:
            print(
                "Invalid input. Name must be alphanumeric and up to 50 characters long."
            )

    # Collecting and validating cooking time
    while True:
        cooking_time = input("Enter the cooking time in minutes: ")
        if cooking_time.isnumeric():
            cooking_time = int(cooking_time)
            break
        else:
            print("Invalid input. Cooking time must be a number.")

    # Collecting ingredients
    ingredients = []
    while True:
        num_ingredients = input("How many ingredients would you like to enter? ")
        if num_ingredients.isnumeric():
            num_ingredients = int(num_ingredients)
            break
        else:
            print("Invalid input. Please enter a number.")

    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient.strip())

    ingredients_str = ", ".join(ingredients)

    # Creating new recipe entry
    recipe_entry = Recipe(
        name=name, ingredients=ingredients_str, cooking_time=cooking_time
    )
    recipe_entry.calculate_difficulty()

    # Adding to session and committing to database
    session.add(recipe_entry)
    session.commit()

    print("Recipe added!")


def view_all_recipes():
    # Retrieve all recipes from the database
    recipes = session.query(Recipe).all()

    # Check if there are no recipes
    if not recipes:
        print("There are no recipes in the database.")
        return None

    # Loop through the list of recipes and display each one
    for recipe in recipes:
        print(recipe)


def search_by_ingredients():
    # Check table for recipes
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Retrieve all ingredients
    results = session.query(Recipe.ingredients).all()

    # Initialize an empty list for all ingredients
    all_ingredients = []

    # Go through each entry in results and add ingredients to all_ingredients list
    for result in results:
        ingredients = result[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Display all ingredients to the user
    print("Available ingredients:")
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}. {ingredient}")

    # Number of ingredients to search for
    selected_numbers = input(
        "Enter the numbers of the ingredients you want to search for, separated by spaces: "
    ).split(" ")

    # Validate user inputs
    try:
        selected_indices = [int(num) - 1 for num in selected_numbers]
        search_ingredients = [
            all_ingredients[index]
            for index in selected_indices
            if index < len(all_ingredients)
        ]
    except (ValueError, IndexError):
        print(
            "Invalid input. Please enter valid numbers corresponding to the ingredients."
        )
        return None

    # Initialize an empty list for conditions
    conditions = []

    # Create like conditions for each selected ingredient
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Retrieve all recipes matching the conditions
    recipes = session.query(Recipe).filter(*conditions).all()

    # Check if there are no recipes matching the search
    if not recipes:
        print("No recipes found with the selected ingredients.")
        return None

    # Display the recipes
    for recipe in recipes:
        print(recipe)


def edit_recipe():
    # Check if any recipes exist in the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Retrieve id and name for each recipe from the database
    results = session.query(Recipe.id, Recipe.name).all()

    # Display available recipes to the user with id and name only
    print("Available Recipes:")
    for index, (recipe_id, recipe_name) in enumerate(results, start=1):
        print(f"{index}. ID: {recipe_id}, Name: {recipe_name}")

    # Ask user to pick a recipe by its id
    try:
        selected_id = int(input("Enter the ID of the recipe you want to edit: "))
    except ValueError:
        print("Invalid input. Please enter a valid ID.")
        return None

    # Check if the chosen id exists
    recipe_to_edit = session.query(Recipe).filter_by(id=selected_id).first()
    if not recipe_to_edit:
        print("Recipe ID does not exist.")
        return None

    # Display recipe details for editing
    print("Recipe to edit:")
    print("1. Name:", recipe_to_edit.name)
    print("2. Ingredients:", recipe_to_edit.ingredients)
    print("3. Cooking Time:", recipe_to_edit.cooking_time, "minutes")

    # Ask user which attribute to edit
    attribute_to_edit = input("Enter the number of the attribute you want to edit: ")

    # Edit the selected attribute
    if attribute_to_edit == "1":
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute_to_edit == "2":
        new_ingredients = input("Enter the new ingredients: ")
        recipe_to_edit.ingredients = new_ingredients
    elif attribute_to_edit == "3":
        while True:
            new_cooking_time = input("Enter the new cooking time in minutes: ")
            if new_cooking_time.isnumeric():
                recipe_to_edit.cooking_time = int(new_cooking_time)
                break
            else:
                print("Invalid input. Cooking time must be a number.")
    else:
        print("Invalid input. Please enter a valid attribute number.")
        return None

    # Calculate difficulty again
    recipe_to_edit.calculate_difficulty()

    # Commit changes to the database
    session.commit()
    print("Recipe edited successfully!")


def delete_recipe():
    # Check if any recipes exist in the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    # Retrieve id and name for each recipe from the database
    results = session.query(Recipe.id, Recipe.name).all()

    # Display available recipes to the user with id and name only
    print("Available Recipes:")
    for index, (recipe_id, recipe_name) in enumerate(results, start=1):
        print(f"{index}. ID: {recipe_id}, Name: {recipe_name}")

    # Ask user to pick a recipe by its id
    try:
        selected_id = int(input("Enter the ID of the recipe you want to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid ID.")
        return None

    # Check if the chosen id exists
    recipe_to_delete = session.query(Recipe).filter_by(id=selected_id).first()
    if not recipe_to_delete:
        print("Recipe ID does not exist.")
        return None

    # Confirm deletion with the user
    confirmation = input(
        f"Are you sure you want to delete the recipe '{recipe_to_delete.name}'? (yes/no): "
    ).lower()
    if confirmation == "yes":
        # Perform delete operation and commit change
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Deletion cancelled.")


def main_menu():
    while True:
        print("\nMAIN MENU")
        print("=====================================")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice.lower() == "quit" or choice == "6":
            print("Exiting the recipe app.")
            # Close session and engine
            session.close()
            engine.dispose()
            break
        else:
            print(
                "Invalid choice. Please enter a number from 1 to 6, or type 'quit' to exit."
            )

main_menu()
