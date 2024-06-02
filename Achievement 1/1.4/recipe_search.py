# Import pickle module
import pickle

# Displays recipe information
def display_recipe(recipe):
  print("Recipe: ", recipe["name"])
  print("Cooking Time (min): ", recipe["cooking_time"])
  print("Ingredients: ", recipe["ingredients"])
  print("Difficulty level: ", recipe["difficulty"])

# Asks user to input the number that matches an ingredient within All Ingredients List then displays recipes with ingredient
def search_ingredient(data):
  numbered_ingredients = list(enumerate(data["all_ingredients"]))
  print("All Ingredients List:")
  for ele in numbered_ingredients:
    print(ele[0], ele[1])
  try:
    n = int(input("Enter the number of the ingredient you would like to search: "))
    ingredient_searched = numbered_ingredients[n][1]
  except ValueError:
    print("Input must be an integer and an integer that is on the All Ingredients List")
  else:
    for recipe in data["recipes_list"]:
      if ingredient_searched in recipe["ingredients"]:
        print(recipe)

# Asks user for the name of the file that contains recipe
filename = input("Enter the name of the file that contains recipe data: ")

# Uses pickle module and try block to extract recipe data from file
try:
  file = open(filename, "rb")
  data = pickle.load(file)
  print("File load successful")
except:
  print("File was not found")
else:
  search_ingredient(data)
  file.close()