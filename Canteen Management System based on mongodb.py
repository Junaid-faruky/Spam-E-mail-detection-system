from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client["canteen_management"]
menu_collection = db["menu"]
orders_collection = db["orders"]

# Function to add a menu item
def add_menu_item(name, price):
    menu_item = {"name": name, "price": price}
    menu_collection.insert_one(menu_item)
    print(f"Menu item '{name}' added successfully!")

# Function to view all menu items
def view_menu():
    print("\n--- Menu ---")
    for item in menu_collection.find():
        print(f"ID: {item['_id']}, Name: {item['name']}, Price: {item['price']}")

# Function to update a menu item
def update_menu_item(item_id, name, price):
    result = menu_collection.update_one(
        {"_id": item_id}, {"$set": {"name": name, "price": price}}
    )
    if result.modified_count > 0:
        print("Menu item updated successfully!")
    else:
        print("No menu item found with the given ID.")

# Function to delete a menu item
def delete_menu_item(item_id):
    result = menu_collection.delete_one({"_id": item_id})
    if result.deleted_count > 0:
        print("Menu item deleted successfully!")
    else:
        print("No menu item found with the given ID.")

# Function to place an order
def place_order(customer_name, items):
    order = {"customer_name": customer_name, "items": items}
    orders_collection.insert_one(order)
    print("Order placed successfully!")

# Function to view all orders
def view_orders():
    print("\n--- Orders ---")
    for order in orders_collection.find():
        print(f"Order ID: {order['_id']}, Customer Name: {order['customer_name']}, Items: {order['items']}")

# Main menu
def main():
    while True:
        print("\n--- Canteen Management System ---")
        print("1. Add Menu Item")
        print("2. View Menu")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. Place Order")
        print("6. View Orders")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            add_menu_item(name, price)
        elif choice == "2":
            view_menu()
        elif choice == "3":
            try:
                item_id = ObjectId(input("Enter item ID to update: "))
                name = input("Enter new name: ")
                price = float(input("Enter new price: "))
                update_menu_item(item_id, name, price)
            except:
                print("Invalid ID format.")
        elif choice == "4":
            try:
                item_id = ObjectId(input("Enter item ID to delete: "))
                delete_menu_item(item_id)
            except:
                print("Invalid ID format.")
        elif choice == "5":
            customer_name = input("Enter customer name: ")
            items = input("Enter items (comma-separated): ").split(",")
            place_order(customer_name, [item.strip() for item in items])
        elif choice == "6":
            view_orders()
        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
