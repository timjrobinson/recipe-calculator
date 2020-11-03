import os
import re

database_location = '/mnt/md0/documents/obsidian/cooking'
file_extension = '.md'

# Given a recipe file name, 
# Calculate the cost of the recipe
# And update the Cost:: tag with the total cost
def update_recipe_cost(filename):
    pass

# Given a recipe file
# Calculate and return the cost of the recipe
def get_recipe_cost(filename):
    with open(os.path.join(database_location, filename + file_extension)) as reader:
        file_contents = reader.read()
        lines = file_contents.split("\n")
        ingredients_line = None
        next_headline = None
        for idx, line in enumerate(lines):
            if re.match(r"## ", line) and ingredients_line != None:
                next_headline = idx
                break
            if re.match(r"## Ingredients", line):
                ingredients_line = idx
        # print(f"ingredients_line: {ingredients_line} next_headline: {next_headline}")
        if ingredients_line == None:
            raise Exception(f"Could not find Ingredients line in file {filename}")
        cost = get_cost_of_ingredients(lines[ingredients_line:next_headline])
        print(f"Total Cost is {cost}")
        return cost
    
# Returns the value of a metadata item in a file
def get_metadata_item(filename, metadata_name):
    with open(os.path.join(database_location, filename + file_extension)) as reader:
        file_contents = reader.read()
        value_search = re.search(r"Cost::[\s]+([0-9.]+)", file_contents).groups()
        if len(value_search) != 1:
            raise Exception(f"Found {len(value_search)} cost values in {filename}, expecting 1")
        return float(value_search[0])
                
# Update the metadata in a file, setting it to a new value, creating it if it doesn't exist. 
# Tags are of format <Name>:: and are the topmost thing in a file. 
def update_metadata_item(filename, metadata_item_name, value):
    pass
    
    
# Given a block of ingredients text,
# Calculate the total cost of the recipe
# And return that as a float. 
def get_cost_of_ingredients(ingredients_lines):
    ingredients_array = gather_ingredients(ingredients_lines)
    ingredients_array_with_costs = map(lambda ia: {**ia, "cost": get_ingredient_cost(ia["name"])}, ingredients_array)
    total_cost = 0
    for item in ingredients_array_with_costs:
        item_cost = round(item['qty'] * item['cost'], 2)
        total_cost += item_cost
        print(f"Cost of {item['name']} is {item_cost}")
    return total_cost
    
    
# Given a block of ingredients text, 
# Create an array of dictionaries of contents [{qty, name}]. 
def gather_ingredients(ingredients_lines):
    ingredients_parsed = []
    for line in ingredients_lines:
        line_parsed = re.match(r"[- ]+([0-9/]+)[\s]+\[\[([\w\s]+)\]\]", line)
        if line_parsed != None:
            qty, name = line_parsed.groups()
            ingredients_parsed.append({
                "qty": float(eval(qty)),
                "name": name
            })
    return ingredients_parsed
    
    
    
def get_ingredient_cost(ingredient_name):
    return get_metadata_item(ingredient_name, 'Cost')


if __name__ == '__main__':
    # red_onion_cost = get_metadata_item('Red Onion', 'Cost')
    # print("Red onion cost:")
    # print(red_onion_cost)
    recipe_cost = get_recipe_cost("Tuna Melt on Flatbread")
