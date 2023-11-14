import sqlite3
from faker import Faker
from datetime import datetime, timedelta

# Connexion à la base de données SQLite
db_connection = sqlite3.connect("identifier")
cursor = db_connection.cursor()

# Initialisation de Faker
fake = Faker()

# Générer des utilisateurs et des adresses
for _ in range(10):
    firstname = fake.first_name()
    lastname = fake.last_name()
    username = fake.user_name()

    # Insérer dans la table user
    cursor.execute("INSERT INTO user (firstname, lastname, username) VALUES (?, ?, ?)", (firstname, lastname, username))
    db_connection.commit()
    user_id = cursor.lastrowid

    street_address = fake.street_address()
    city = fake.city()
    postal_code = fake.postcode()

    # Insérer dans la table address
    cursor.execute("INSERT INTO address (user_id, street_address, city, postal_code) VALUES (?, ?, ?, ?)",
                   (user_id, street_address, city, postal_code))
    db_connection.commit()

# Générer des produits
for _ in range(10):
    product_name = fake.word()
    product_description = fake.sentence()
    price = fake.random_float(2, 10, 100)
    stock_available = fake.random_int(1, 100)

    # Insérer dans la table product
    cursor.execute("INSERT INTO product (name, description, price, stock_available) VALUES (?, ?, ?, ?)",
                   (product_name, product_description, price, stock_available))
    db_connection.commit()

# Générer des paniers et des commandes
cursor.execute("SELECT user_id FROM user")
users = cursor.fetchall()
cursor.execute("SELECT product_id FROM product")
products = cursor.fetchall()

for user in users:
    cart_products = fake.random_elements(products, length=fake.random_int(1, 5))
    for product in cart_products:
        quantity = fake.random_int(1, 5)
        cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                       (user[0], product[0], quantity))
        db_connection.commit()

    command_products = fake.random_elements(products, length=fake.random_int(1, 3))
    for product in command_products:
        quantity = fake.random_int(1, 3)
        cursor.execute("INSERT INTO command (user_id, product_id, quantity) VALUES (?, ?, ?)",
                       (user[0], product[0], quantity))
        db_connection.commit()

# Générer des factures
for user in users:
    invoice_products = fake.random_elements(products, length=fake.random_int(1, 3))
    for product in invoice_products:
        quantity = fake.random_int(1, 3)
        order_date = fake.date_time_this_decade()
        cursor.execute("INSERT INTO invoices (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
                       (user[0], product[0], quantity, order_date))
        db_connection.commit()

# Fermeture de la connexion
cursor.close()
db_connection.close()
