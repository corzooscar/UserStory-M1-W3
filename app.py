from services import *
from archives import *

"""
──── Basic formatting (0-7) ─────────────────────────────────────────────────────────────────────────────────── 
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

# Main data structure — each product will be stored as a dictionary inside this list
Inventory = []
Showtime = True

# Welcome banner
print(f"""{BOLD}{MAGENTA}╔═══════════════════════════════════════════════════════════╗{RESET}
                {BOLD}{GREEN}🐧📦  INVENTORY MANAGER  📦🐧{RESET}
            {GREEN}Welcome to the Inventory Manager!{RESET}
    {DIM}{MAGENTA}By: Oscar Corzo | GitHub: {RESET}{DIM}{CYAN}https://github.com/corzooscar {RESET}
{BOLD}{MAGENTA}╚═══════════════════════════════════════════════════════════╝{RESET}""")

# Main loop
while Showtime:
    try:
        Option = int(input(f"""{BOLD}{MAGENTA}{"="*24}{RESET}{BOLD}{GREEN} MAIN MENU{RESET} {BOLD}{MAGENTA}{"="*25}{RESET}
{BOLD}{MAGENTA}1){RESET}{GREEN} Add product{RESET}
{BOLD}{MAGENTA}2){RESET}{GREEN} Show inventory{RESET}
{BOLD}{MAGENTA}3){RESET}{GREEN} Search product{RESET}
{BOLD}{MAGENTA}4){RESET}{GREEN} Update product from Inventory{RESET}
{BOLD}{MAGENTA}5){RESET}{GREEN} Delete product from Inventory{RESET}
{BOLD}{MAGENTA}6){RESET}{GREEN} Calculate statistics{RESET}
{BOLD}{MAGENTA}7){RESET}{GREEN} Save CSV{RESET}
{BOLD}{MAGENTA}8){RESET}{GREEN} Load CSV{RESET}
{BOLD}{MAGENTA}9){RESET}{GREEN} 🔚​ Exit{RESET}
{BOLD}{MAGENTA}{"="*60}{RESET}
{BOLD}{GREEN}Choose an option:{RESET}
{MAGENTA}➤  {RESET}"""))

        # Option 1 — Enters a sub-loop that keeps adding products until the user types 'exit'
        if Option == 1:
            Process = None
            while Process != "exit":
                print(f"{BOLD}{MAGENTA}{'='*23}{RESET}{BOLD}{GREEN} NEW PRODUCT{RESET} {BOLD}{MAGENTA}{'='*24}{RESET}")
                add_product(Inventory)
                Process = input(f"{YELLOW}{ITALIC}Type 'exit' to return to the main menu, or press Enter to\nadd another product: {RESET}").lower()
                
        # Option 2 — Displays all products currently stored in the inventory
        elif Option == 2:
            print(f"{BOLD}{MAGENTA}{'='*24}{RESET}{BOLD}{GREEN} INVENTORY{RESET} {BOLD}{MAGENTA}{'='*25}{RESET}")            
            show_inventory(Inventory)

        # Option 3 — Search for a product
        elif Option == 3:
            print(f"{BOLD}{MAGENTA}{'='*22}{RESET}{BOLD}{GREEN} SEARCH PRODUCT{RESET} {BOLD}{MAGENTA}{'='*22}{RESET}")            
            name = input(f"{GREEN}~ Name: {RESET}")
            product = find_product(Inventory, name)
            print(f"{GREEN}{product if product else 'Not found'}{RESET}")

        # Option 4 — Update a product
        elif Option == 4:
            print(f"{BOLD}{MAGENTA}{'='*22}{RESET}{BOLD}{GREEN} UPDATE PRODUCT{RESET} {BOLD}{MAGENTA}{'='*22}{RESET}")
            name     = get_info(f"{GREEN}~ Product name: {RESET}", str)
            price    = get_info(f"{GREEN}~ New Price: {RESET}", float)
            quantity = get_info(f"{GREEN}~ New Quantity: {RESET}", int)
            updated = update_product(Inventory, name, price, quantity)
            print(f"{YELLOW}{ITALIC}{'Updated' if updated else 'Not found'}{RESET}")
            

        # Option 5 — Delete a product
        elif Option == 5:
            print(f"{BOLD}{MAGENTA}{'='*22}{RESET}{BOLD}{GREEN} DELETE PRODUCT{RESET} {BOLD}{MAGENTA}{'='*22}{RESET}")
            name = input(f"{GREEN}~ Name: {RESET}")
            deleted = delete_product(Inventory, name)
            print(f"{YELLOW}{ITALIC}{'Deleted' if deleted else 'Not found'}{RESET}")

        # Option 6 — Show statistics
        elif Option == 6:
            stats = calculate_statistics(Inventory)

            if stats:
                print(f"{BOLD}{MAGENTA}{'='*24}{RESET}{BOLD}{GREEN} STATISTICS{RESET} {BOLD}{MAGENTA}{'='*24}{RESET}")
                print(f"{GREEN}Total units: {stats['total_units']}{RESET}")
                print(f"{GREEN}Total value: {stats['total_value']}{RESET}")
                print(f"{GREEN}Most expensive: {stats['most_expensive']['name']} - {stats['most_expensive']['price']}{RESET}")
                print(f"{GREEN}Highest stock: {stats['highest_stock']['name']} - {stats['highest_stock']['quantity']}{RESET}")
            else:
                print(f"{YELLOW}{ITALIC}No data available.{RESET}")

        # Option 7 — Save CSV
        elif Option == 7:
            print(f"{BOLD}{MAGENTA}{'='*24}{RESET}{BOLD}{BLUE} SAVE CSV{RESET} {BOLD}{MAGENTA}{'='*26}{RESET}")
            path = input(f"{BLUE}{ITALIC}~ File path: {RESET}")
            save_csv(Inventory, path)

        # Option 8 — Load CSV
        elif Option == 8:
            print(f"{BOLD}{MAGENTA}{'='*24}{RESET}{BOLD}{BLUE} LOAD CSV{RESET} {BOLD}{MAGENTA}{'='*26}{RESET}")
            path = input(f"{BLUE}{ITALIC}~ File path: {RESET}")
            new_data, errors = load_csv(path)

            if len(new_data) > 0:
                choice = input(f"{BLUE}{ITALIC}~ Overwrite inventory? (S/N): {RESET}")

                if choice.upper() == "S":
                    Inventory = new_data
                    action = "replaced"
                elif choice.upper() == "N":
                    # Merge inventories
                    for new_p in new_data:
                        existing = find_product(Inventory, new_p["name"])

                        if existing:
                            existing["quantity"] += new_p["quantity"]
                            if existing["price"] != new_p["price"]:
                                existing["price"] = new_p["price"]
                        else:
                            Inventory.append(new_p)
                    action = "merged"
                else:
                    print(f"{YELLOW}{ITALIC}Invalid choice. Inventory not modified.{RESET}")
                    action = "not modified"

                print(f"{GREEN}Loaded: {len(new_data)} products{RESET}")
                print(f"{YELLOW}{ITALIC}Invalid rows: {errors}{RESET}")
                print(f"{GREEN}Inventory {action}{RESET}")
            else:
                print(f"{YELLOW}{ITALIC}No valid data loaded.{RESET}")

        # Option 9 — Exits the program cleanly
        elif Option == 9:
            print(f"{GREEN}{'Exiting the program. Goodbye!'.center(60)}{RESET}")
            exit()

        # Any other number — informs the user the option is out of range
        else:
            print(f"{BOLD}{RED}{'❌ ERROR: Please enter a number between 1 and 9. ❌'.center(60)}{RESET}")
            
    # Non-integer input at the main menu — caught here so the program never crashes        
    except ValueError:
        print(f"{BOLD}{RED}{'❌ ERROR: Please enter a valid input. ❌'.center(60)}{RESET}")
