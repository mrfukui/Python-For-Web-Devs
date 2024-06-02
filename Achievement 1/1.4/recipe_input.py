# Import pickle module
import pickle

# Take recipes from user
def take_recipe():
  name = input("Recipe name: ")
  cooking_time = int(input("Cooking time: "))
  ingredients = list(input("Ingredients separated by a comma and space: ").split(", "))
  difficulty = calc_difficulty(cooking_time, ingredients)
  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}

  return recipe

# Calculate difficulty level of a recipe
def calc_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    return "Easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
    return "Medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
    return "Intermediate"
  elif cooking_time >= 10 and len(ingredients) >= 4:
    return "Hard"

# Take filename for saving recipes from user
filename = input("Enter the filename you want to save your recipes to: ")

# try-except-else-finally block that has a user attempt to open a binary file in read mode
try:
  file = open(filename, 'rb')
  data = pickle.load(file)
  print("File load successful")
except FileNotFoundError:
  print("Files doesn't exist, creating a new file")
  data = {"recipes_list": [], "all_ingredients": []}
except:
  print("An unexpected error occured.")
  data = {"recipes_list": [], "all_ingredients": []}
else:
  file.close()
finally:
  recipes_list = data["recipes_list"]
  all_ingredients = data["all_ingredients"]

# Asks the user to enter the number of recipes they would like to enter
n = int(input("Enter the number of recipes you would like to enter: "))

# Adds each recipe to recipes list and adds new ingredients to all ingredients list
for i in range(n):
  recipe = take_recipe()
  recipes_list.append(recipe)
  for ingredient in recipe["ingredients"]:
    if not ingredient in all_ingredients:
      all_ingredients.append(ingredient)

# Creates updated dictionary
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Opens binary file with user-defined filename and writes data into it
with open(filename, 'wb') as file:
  pickle.dump(data, file)