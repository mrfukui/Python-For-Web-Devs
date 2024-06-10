import mysql.connector

conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="password")

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS Recipes(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  ingredients VARCHAR(255),
  cooking_time INT,
  difficulty VARCHAR(20)            
)"""
)


def main_menu(conn, cursor):

    choice = ""

    while choice != "quit":
        print("Main Menu")
        print("==================================")
        print("Pick a choice 1-4:")
        print("    1. Create a new recipe")
        print("    2. Search for a recipe by ingredient")
        print("    3. Update an existing recipe")
        print("    4. Delete a recipe")
        print("    Type 'quit' to exit the program.")
        choice = input("Your choice: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "quit":
            print("Thank you for using the Recipe App")
            break

    conn.close()


def view_all_recipes(conn, cursor):
    print("All recipes:\n")

    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    for row in results:
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time(min): ", row[3])
        print("Difficulty: ", row[4])


def create_recipe(conn, cursor):
    ingredients = []
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time: "))
    ingredients = list(
        input("Ingredients separated by a comma and space: ").split(", ")
    )
    difficulty = calc_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)

    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print("Recipe has been entered into the database")


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return "Hard"


def search_recipe(conn, cursor):
    all_ingredients = set()
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    all_ingredients_list = list(enumerate(all_ingredients))

    print("All ingredients list:")

    for index, tup in enumerate(all_ingredients_list):
        print(str(tup[0] + 1) + ". " + tup[1])

    try:
        n = input("Enter the number of the ingredient you would like to search:")

        ingredient_searched_index = int(n) - 1

        ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

    except:
        print("Unexpected error.  Please select a number within the list.")
        return

    print("Recipes with ingredient selected:\n")

    cursor.execute(
        "SELECT * FROM Recipes WHERE ingredients LIKE %s",
        ("%" + ingredient_searched + "%",),
    )

    recipes_results = cursor.fetchall()

    for row in recipes_results:
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time(min): ", row[3])
        print("Difficulty: ", row[4])


def update_recipe(conn, cursor):

    view_all_recipes(conn, cursor)

    recipe_id_update = int(
        input("Enter the ID of the recipe you would like to update: ")
    )
    column_update = input(
        "Enter the data you would like to update which would be 'name', 'cooking_time' or 'ingredients': "
    )
    new_data = input("Enter the new data for the recipe: ")

    if column_update == "name":
        cursor.execute(
            "UPDATE Recipes SET name = %s WHERE id = %s", (new_data, recipe_id_update)
        )

    elif column_update == "cooking_time":
        cursor.execute(
            "UPDATE Recipes SET cooking_time = %s WHERE id = %s",
            (new_data, recipe_id_update),
        )
        cursor.execute(
            "SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id_update,)
        )
        current_ingredients = cursor.fetchone()[0].split(", ")
        updated_difficulty = calc_difficulty(int(new_data), current_ingredients)
        cursor.execute(
            "UPDATE Recipes SET difficulty = %s WHERE id = %s",
            (updated_difficulty, recipe_id_update),
        )
    elif column_update == "ingredients":
        ingredients = list(new_data.split(", "))
        ingredients_str = ", ".join(ingredients)
        cursor.execute(
            "UPDATE Recipes SET ingredients = %s WHERE id = %s",
            (ingredients_str, recipe_id_update),
        )
        cursor.execute(
            "SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id_update,)
        )
        current_cooking_time = cursor.fetchone()[0]
        updated_difficulty = calc_difficulty(current_cooking_time, ingredients)
        cursor.execute(
            "UPDATE Recipes SET difficulty = %s WHERE id = %s",
            (updated_difficulty, recipe_id_update),
        )
    else:
        print("Invalid column name.")

    conn.commit()
    print("Recipe updated")


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    recipe_id_delete = int(
        input("Enter the ID of the recipe you would like to delete: ")
    )
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id_delete,))
    conn.commit()
    print("Recipe deleted")

main_menu(conn, cursor)