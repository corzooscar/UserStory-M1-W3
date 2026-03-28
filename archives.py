"""
──── Basic formatting (0-7) ───────────────────────────────────────────────────────────────────────────────── 
─ Used to change the style of the text in the terminal. 
─ Each style is represented by a specific escape code. 
─ I decided to add all of them even if I only use a few, so I have them ready for future use (THIS IS NOT AI).
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

# ──── Save inventory to CSV file ─────────────────────────────────────────────────────────────────────────────────────
def save_csv(Inventory, path, include_header=True):
    """
    Writes the current inventory to a CSV file at the given path.

    Each product is saved as a comma-separated row with the fields name, price,
    and quantity. If include_header is True, a header row is written first.
    Returns early with a warning if the inventory is empty. Catches any
    file system errors (permissions, invalid path, etc.) without closing the program.

    Args:
        Inventory (list): The current list of product dictionaries.
                          Each product must have keys: "name" (str), "price" (float), "quantity" (int).
        path (str): The file path where the CSV will be saved (e.g. "inventory.csv").
        include_header (bool): Whether to write the header row "name,price,quantity". Defaults to True.

    Returns:
        None. Prints a success or error message to the terminal.
    """
    if not Inventory:
        print(f"{YELLOW}{ITALIC}Inventory is empty.{RESET}")
        return

    try:
        with open(path, "w") as file:
            if include_header:
                file.write("name,price,quantity\n")

            for p in Inventory:
                file.write(f"{p['name']},{p['price']},{p['quantity']}\n")

        print(f"{BLUE}{ITALIC}Inventory saved in: {path}{RESET}")

    except Exception as e:
        print(f"{RED}Error saving file: {e}{RESET}")


# ──── Load inventory from CSV file ─────────────────────────────────────────────────────────────────────────────────────
def load_csv(path):
    """
    Reads a CSV file and returns its contents as a list of product dictionaries.

    Validates the header row, then processes each data row individually.
    Rows with the wrong number of columns, non-numeric price/quantity, or
    negative values are skipped and counted as invalid. Handles missing files,
    encoding errors, and any other exceptions without closing the program.

    Args:
        path (str): The file path of the CSV to load (e.g. "inventory.csv").

    Returns:
        tuple:
            - list: Products successfully parsed from the file. Empty list if the file
                    could not be read or had no valid rows.
            - int:  Number of rows skipped due to validation errors.
    """
    Inventory = []
    invalid_rows = 0

    try:
        with open(path, "r") as file:
            lines = file.readlines()

        # Validate header
        if lines[0].strip() != "name,price,quantity":
            print(f"{YELLOW}{ITALIC}Invalid file format.{RESET}")
            return [], 0

        for line in lines[1:]:
            parts = line.strip().split(",")

            if len(parts) != 3:
                invalid_rows += 1
                continue

            name, price, quantity = parts

            try:
                price = float(price)
                quantity = int(quantity)

                if price < 0 or quantity < 0:
                    invalid_rows += 1
                    continue

                Inventory.append({
                    "name": name,
                    "price": price,
                    "quantity": quantity
                })

            except ValueError:
                invalid_rows += 1

        return Inventory, invalid_rows

    except FileNotFoundError:
        print(f"{RED}File not found.{RESET}")
        return [], 0
    except UnicodeDecodeError:
        print(f"{RED}File encoding error.{RESET}")
        return [], 0
    except Exception as e:
        print(f"{RED}Error loading file: {e}{RESET}")
        return [], 0
