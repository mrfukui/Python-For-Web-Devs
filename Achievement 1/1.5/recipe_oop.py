# Defines the class Recipe
class Recipe(object):
    # Variable to store all ingredients from all recipes
    all_ingredients = []

    # Initializiation method
    def __init__(self, name, cooking_time):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None

    def get_name(self):
        output = self.name
        return output

    def set_name(self):
        self.name = input("Enter the name of the recipe: ")

    def get_cooking_time(self):
        output = self.cooking_time
        return output

    def set_cooking_time(self):
        self.cooking_time = int(input("Enter the cooking time: "))

    # Adds ingredients
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()

    def get_ingredients(self):
        output = self.name
        return output

    # Calculates difficulty of recipe based on cooking time and number of ingredients
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    # Searches whether an ingredient is within the recipe
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # Adds new ingredients to all_ingredients list
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)

    # String representation that prints entire recipe over well formatted string
    def __str__(self):
        output = (
            "Name: "
            + str(self.name)
            + "\nCooking time (min): "
            + str(self.cooking_time)
            + "\nIngredients: "
            + str(self.ingredients)
            + "\nDifficulty: "
            + str(self.difficulty)
            + "\n"
        )
        for ingredient in self.ingredients:
            output += ingredient + "\n"
        return output


# Finds recipes with certain ingredient
def recipe_search(recipes_list, ingredient):
    data = recipes_list
    search_term = ingredient
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


# New objects within Recipe class
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.get_difficulty()
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.get_difficulty()
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients(
    "Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"
)
cake.get_difficulty()
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients(
    "Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"
)
banana_smoothie.get_difficulty()
print(banana_smoothie)

recipes_list = []

recipes_list.extend([tea, coffee, cake, banana_smoothie])

print("\nRecipes that contain Water:")
recipe_search(recipes_list, "Water")

print("\nRecipes that contain Sugar:")
recipe_search(recipes_list, "Sugar")

print("\nRecipes that contain Bananas:")
recipe_search(recipes_list, "Bananas")
