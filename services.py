"""
──── Basic formatting (0-7) ────────────────────────────────────────────────────────────────── 
─ Used to change the style of the text in the terminal. 
─ Each style is represented by a specific escape code. 
─ I decided to add all of them but in the end i only used RESET, which is the most common one.
─ ANSI escape codes for text styling: \033 signals the terminal to read what follows as a
formatting instruction, [ opens it, the number sets the style, and m closes/applies it
"""
RESET   = "\033[0m" 
BOLD    = "\033[1m"
DIM     = "\033[2m"
ITALIC  = "\033[3m"
UNDER   = "\033[4m"
BLINK   = "\033[5m"
INVERT  = "\033[7m"

"""     
──── Text colors (30-37) ─────────────────────────────────────────────────────────────────────────────────────
─ Used to change the color of the text in the terminal. 
─ Each color is represented by a specific escape code. 
─ I decided to add all of them even if I only use a few, so I have them ready for future use (THIS IS NOT AI).
─ ANSI escape codes for text color: same structure as above, 3X where X is the color number (0-7)
"""
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"

# ──── Reusable input function ────────────────────────────────────────────────────────────────────────────────────
def get_info(prompt, type=str):
    """
    Repeatedly prompts the user until a valid value of the given type is entered.

    Catches ValueError for non-convertible input. For numeric types (int, float),
    also rejects values lower than 1.

    Args:
        prompt (str): The message shown to the user in the terminal.
        type (type): The expected data type for the input. Defaults to str.

    Returns:
        The user's input converted to the specified type.
    """
    keep_going = "y"
    while keep_going != "n":                # Infinite loop to keep asking until valid input is received        
        try:
            value = type(input(prompt))
            if type == int or type == float:
                if value < 1:
                    print(f"{RED}❌ Value cannot be lower than 1. Try again. ❌{RESET}\n")
                    continue
            keep_going = "n"
        except ValueError:
            print(f"{RED}❌ Invalid input. Try again. ❌{RESET}\n")
    return value

# ──── 1. Add product ──────────────────────────────────────────────────────────────────────────────────── 
def add_product(Inventory):
    """
    Collects product data from the user and appends it to the inventory.

    Prompts for name (str), price (float), and quantity (int) using get_info(),
    then builds a dictionary and adds it to the Inventory list.

    Args:
        Inventory (list): The current list of product dictionaries.

    Returns:
        None. Modifies Inventory in place.
    """
    name     = get_info(f"{GREEN}~ Product name: {RESET}", str)
    price    = get_info(f"{GREEN}~ Price: {RESET}", float)
    quantity = get_info(f"{GREEN}~ Quantity: {RESET}", int)
    Product = {"name": name, "price": price, "quantity": quantity}
    Inventory.append(Product)

# ──── 2. Show all products ────────────────────────────────────────────────────────────────────────────────────
def show_inventory(Inventory):
    """
    Prints all products in the inventory to the terminal.

    If the inventory is empty, displays a warning message and returns early.
    Otherwise, iterates over the list and prints each product's name, price,
    and quantity with a separator line between entries.

    Args:
        Inventory (list): The current list of product dictionaries.

    Returns:
        None.
    """
    if not Inventory:
        print(f"{YELLOW}The inventory is currently empty.{RESET}\n")
        return
    else:
        for product in Inventory:
            print(f"{GREEN}— Product: {product['name']} | Price: ${product['price']:.2f} | Quantity: {product['quantity']}{RESET}")
            print(f"{GREEN}{'─'*50}{RESET}")

# ──── 3. Find product by name ────────────────────────────────────────────────────────────────────────────────────
def find_product(Inventory, name):
    """
    Searches the inventory for a product matching the given name.

    Performs a case-sensitive linear search through the inventory list.
    Used internally by update_product() and delete_product().

    Args:
        Inventory (list): The current list of product dictionaries.
        name (str): The exact product name to search for.

    Returns:
        dict: The matching product dictionary if found.
        None: If no product with that name exists.
    """
    for product in Inventory:
        if product['name'] == name:
            return product
    return None

# ──── 4. Update product data —──────────────────────────────────────────────────────────────────────────────────── 
def update_product(Inventory, name, new_price=None, new_quantity=None):
    """
    Updates the price and/or quantity of an existing product.

    Uses find_product() to locate the product by name. Only updates
    the fields that are explicitly passed (not None). If the product
    is not found, returns False without modifying the inventory.

    Args:
        Inventory (list): The current list of product dictionaries.
        name (str): The exact name of the product to update.
        new_price (float, optional): New price to set. Defaults to None (no change).
        new_quantity (int, optional): New quantity to set. Defaults to None (no change).

    Returns:
        bool: True if the product was found and updated, False otherwise.
    """
    product = find_product(Inventory, name)

    if product:
        if new_price is not None:
            product["price"] = new_price
        if new_quantity is not None:
            product["quantity"] = new_quantity
        return True

    return False

# ──── 5. Delete product from inventory —────────────────────────────────────────────────────────────────────────────────────
def delete_product(Inventory, name):
    """
    Removes a product from the inventory by name.

    Uses find_product() to locate the product, then removes it from the list
    using list.remove(). If the product does not exist, returns False.

    Args:
        Inventory (list): The current list of product dictionaries.
        name (str): The exact name of the product to delete.

    Returns:
        bool: True if the product was found and removed, False otherwise.
    """
    product = find_product(Inventory, name)

    if product:
        Inventory.remove(product)
        return True 

    return False

# ──── 6. Calculate inventory statistics —────────────────────────────────────────────────────────────────────────────────────
def calculate_statistics(Inventory):
    """
    Computes and displays key statistics about the current inventory.

    Calculates total inventory value (price x quantity for each product),
    total number of units, the most expensive product, and the product
    with the highest stock. Uses sum() with generator expressions for
    efficiency. If the inventory is empty, notifies the user instead.

    Args:
        Inventory (list): The current list of product dictionaries.

    Returns:
        None. Prints results directly to the terminal.
    """
    if not Inventory:
        print(f"{YELLOW}The inventory is currently empty. No statistics to show.{RESET}\n")
    else:
        total_value = sum(product["price"] * product["quantity"] for product in Inventory)
        total_items = sum(product["quantity"] for product in Inventory)
        print(f"{GREEN}Total inventory value: ${total_value:.2f}{RESET}")
        print(f"{GREEN}Total number of items: {total_items}{RESET}")
