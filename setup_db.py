import sqlite3

def create_database():
    conn = sqlite3.connect('recipes.db')  # Create database file
    cursor = conn.cursor()

    # Create a table to store recipes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL
        )
    ''')

    # Insert sample recipes into the database
    sample_recipes = [
        ('Pasta Alfredo', 'pasta, cream, butter, cheese', 'Boil pasta, make Alfredo sauce, mix.'),
        ('Banana Smoothie', 'banana, milk, honey', 'Blend all ingredients.'),
        ('Omelette', 'eggs, onion, tomato, cheese', 'Whisk eggs, fry veggies, cook omelette.'),
        ('Vegetable Salad', 'lettuce, tomato, cucumber, olive oil', 'Chop vegetables, mix with dressing.'),
        ('Grilled Sandwich', 'bread, cheese, tomato, butter', 'Assemble sandwich, grill until golden.')
    ]
    cursor.executemany(
        'INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)',
        sample_recipes
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
