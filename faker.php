<?php
require 'vendor/autoload.php'; // Assurez-vous que le chemin du fichier autoload.php est correct

$faker = Faker\Factory::create();

// Connexion à la base de données
$pdo = new PDO('mysql:host=your_host;dbname=e_commerce_db', 'your_username', 'your_password');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// Générer des utilisateurs et des adresses
for ($i = 0; $i < 10; $i++) {
    $username = $faker->userName;
    $passwordHash = password_hash($faker->password, PASSWORD_BCRYPT);

    // Insérer dans la table user
    $pdo->query("INSERT INTO user (username, password_hash) VALUES ('$username', '$passwordHash')");
    $userId = $pdo->lastInsertId();

    $streetAddress = $faker->streetAddress;
    $city = $faker->city;
    $postalCode = $faker->postcode;

    // Insérer dans la table address
    $pdo->query("INSERT INTO address (user_id, street_address, city, postal_code) VALUES ($userId, '$streetAddress', '$city', '$postalCode')");
}

// Générer des produits
for ($i = 0; $i < 10; $i++) {
    $productName = $faker->word;
    $productDescription = $faker->sentence;
    $price = $faker->randomFloat(2, 10, 100);
    $stockAvailable = $faker->numberBetween(1, 100);

    // Insérer dans la table product
    $pdo->query("INSERT INTO product (name, description, price, stock_available) VALUES ('$productName', '$productDescription', $price, $stockAvailable)");
}

// Générer des paniers et des commandes
$users = $pdo->query("SELECT user_id FROM user")->fetchAll(PDO::FETCH_COLUMN);
$products = $pdo->query("SELECT product_id FROM product")->fetchAll(PDO::FETCH_COLUMN);

foreach ($users as $user) {
    $cartProducts = $faker->randomElements($products, $faker->numberBetween(1, 5));
    foreach ($cartProducts as $product) {
        $quantity = $faker->numberBetween(1, 5);
        $pdo->query("INSERT INTO cart (user_id, product_id, quantity) VALUES ($user, $product, $quantity)");
    }

    $commandProducts = $faker->randomElements($products, $faker->numberBetween(1, 3));
    foreach ($commandProducts as $product) {
        $quantity = $faker->numberBetween(1, 3);
        $pdo->query("INSERT INTO command (user_id, product_id, quantity) VALUES ($user, $product, $quantity)");
    }
}
