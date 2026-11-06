# Smart Shopping Cart

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# store stuff
products = {
    "Sprite": 2.00,
    "Air": 2.50,
    "Watermelon": 1.50,
    "Pizza": 4.25,
    "Bagel": 3.75,
}

# what the customer grabbed
shopping_cart = {}


# money formatting
def format_money(amount):
    rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"${rounded:,.2f}"


# keeps asking till you type a real number in range
def get_number(prompt, minimum, maximum=None):
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if number < minimum or (maximum is not None and number > maximum):
            if maximum is None:
                print(f"Please enter a number of at least {minimum}.")
            else:
                print(f"Please enter a number from {minimum} to {maximum}.")
            continue
        return number


# show products, hand back names in same order
def display_products(products):
    product_names = list(products.keys())
    print("\n========== AVAILABLE PRODUCTS ==========")
    for number, (name, price) in enumerate(products.items(), start=1):
        print(f"{number}. {name} - {format_money(Decimal(str(price)))}")
    return product_names


# add to cart
def add_to_cart(products, shopping_cart):
    product_names = display_products(products)
    choice = get_number("Enter product number: ", 1, len(product_names))
    name = product_names[choice - 1]

    quantity = get_number(f"How many {name} would you like to add? ", 1)
    shopping_cart[name] = shopping_cart.get(name, 0) + quantity

    print(f"Added {quantity} {name} to your cart!")
    print(f"{name} quantity is now {shopping_cart[name]}.")


# remove one unit
def remove_from_cart(shopping_cart):
    if not shopping_cart:
        print("Your cart is empty. Nothing to remove.")
        return

    cart_names = list(shopping_cart.keys())
    print("\n========== YOUR SHOPPING CART ==========")
    for number, (name, quantity) in enumerate(shopping_cart.items(), start=1):
        print(f"{number}. {name} - Quantity: {quantity}")

    choice = get_number("Enter item number to remove: ", 1, len(cart_names))
    name = cart_names[choice - 1]

    shopping_cart[name] -= 1
    print(f"Removed 1 {name} from your cart!")
    if shopping_cart[name] == 0:
        del shopping_cart[name]
        print(f"{name} is now gone from your cart.")
    else:
        print(f"{name} quantity is now {shopping_cart[name]}.")


# total units in cart
def calculate_total_items(shopping_cart):
    total_items = 0
    for quantity in shopping_cart.values():
        total_items += quantity
    return total_items


# price x qty for everything
def calculate_subtotal(products, shopping_cart):
    subtotal = Decimal("0")
    for name, quantity in shopping_cart.items():
        unit_price = Decimal(str(products[name]))
        subtotal += unit_price * quantity
    return subtotal


# discount tiers
def calculate_discount_rate(subtotal):
    if subtotal < 10:
        return Decimal("0")
    elif subtotal < 20:
        return Decimal("0.05")
    elif subtotal < 40:
        return Decimal("0.10")
    else:
        return Decimal("0.15")


# cart table
def display_cart(products, shopping_cart):
    if not shopping_cart:
        print("Your cart is empty.")
        return

    print("\n========== YOUR SHOPPING CART ==========")
    print(f"{'Product':<14}{'Unit Price':>12}{'Quantity':>10}{'Line Total':>13}")
    for number, (name, quantity) in enumerate(shopping_cart.items(), start=1):
        unit_price = Decimal(str(products[name]))
        line_total = unit_price * quantity
        label = f"{number}. {name}"
        print(f"{label:<14}{format_money(unit_price):>12}{quantity:>10}{format_money(line_total):>13}")

    print(f"\nTotal Items: {calculate_total_items(shopping_cart)}")
    print(f"Subtotal: {format_money(calculate_subtotal(products, shopping_cart))}")


# just the subtotal
def view_current_total(products, shopping_cart):
    subtotal = calculate_subtotal(products, shopping_cart)
    print(f"Current Subtotal: {format_money(subtotal)}")


# receipt + discount, returns False if cart is empty
def checkout(products, shopping_cart):
    if not shopping_cart:
        print("Your cart is empty. Add products before checking out.")
        return False

    subtotal = calculate_subtotal(products, shopping_cart)
    discount_rate = calculate_discount_rate(subtotal)
    amount_saved = subtotal * discount_rate
    final_total = subtotal - amount_saved
    today = datetime.now().strftime("%m/%d/%Y")

    print("\n========== RECEIPT ==========")
    print(f"Date: {today}\n")
    print(f"{'Product':<14}{'Unit Price':>12}{'Quantity':>10}{'Line Total':>13}")
    for name, quantity in shopping_cart.items():
        unit_price = Decimal(str(products[name]))
        print(f"{name:<14}{format_money(unit_price):>12}{quantity:>10}{format_money(unit_price * quantity):>13}")

    print(f"\nTotal Items:   {calculate_total_items(shopping_cart)}")
    print(f"Subtotal:      {format_money(subtotal)}")
    print(f"Discount:      {int(discount_rate * 100)}%")
    print(f"Amount Saved:  {format_money(amount_saved)}")
    print(f"Final Total:   {format_money(final_total)}")
    print("\nThank you for shopping!")
    return True


# menu text
def print_menu():
    print("\n========== SMART SHOPPING CART ==========")
    print("1. View Available Products")
    print("2. Add Product to Cart")
    print("3. Remove Product from Cart")
    print("4. View Shopping Cart")
    print("5. View Current Total")
    print("6. Checkout")


# main loop
def main():
    while True:
        print_menu()
        choice = get_number("\nEnter your choice: ", 1, 6)

        if choice == 1:
            display_products(products)
        elif choice == 2:
            add_to_cart(products, shopping_cart)
        elif choice == 3:
            remove_from_cart(shopping_cart)
        elif choice == 4:
            display_cart(products, shopping_cart)
        elif choice == 5:
            view_current_total(products, shopping_cart)
        elif choice == 6:
            if checkout(products, shopping_cart):
                break

    print("Program ended.")


if __name__ == "__main__":
    main()
