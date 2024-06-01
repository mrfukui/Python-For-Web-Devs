# Initializes empty lists
recipes_list = []
ingredients_list = []

# Asks user for number of recipes and recipe itself
def take_recipe():
  name = input("Recipe name: ")
  cooking_time = int(input("Cooking time: "))
  ingredients = list(input("Ingredients separated by a comma and space: ").split(", "))
  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}

  return recipe

n = int(input("How many recipes would you like to enter: "))

# Iterates through ingredients list to add new ingredients
for i in range(n):
  recipe = take_recipe()
  for ingredient in recipe["ingredients"]:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

# Checks conditions of recipes to label recipe with difficulty level and prints recipe with difficulty level
for recipe in recipes_list:
  if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
    recipe["difficulty"] = "Easy"
  elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
    recipe["difficulty"] = "Medium"
  elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
    recipe["difficulty"] = "Intermediate"
  elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
    recipe["difficulty"] = "Hard"

  print("Recipe: ", recipe["name"])
  print("Cooking Time (min): ", recipe["cooking_time"])
  print("Ingredients: ", recipe["ingredients"])
  print("Difficulty level: ", recipe["difficulty"])

# Prints all ingredients in alphabetical order
def print_all_ingredients():
  print("Ingredients Available Across All Recipes")
  print("----------------------------------------")
  ingredients_list.sort()
  for ingredient in ingredients_list:
    print(ingredient)

print_all_ingredients()