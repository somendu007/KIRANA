from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

#creating a database
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


# Creating the categories table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')
# Creating the products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        unit TEXT NOT NULL,       
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')

#creating the cart table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        product_id INTEGER,
        product_name TEXT,
        price REAL,
        quantity INTEGER,
        subtotal REAL,
        unit TEXT
    )
''')
               

# Commiting changes and closing the connection
conn.commit()
conn.close()

#function to get all the categories
def get_all_categories_from_database():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return categories
#function to get all products
def get_all_products_from_database():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products
#function to add category to the categories database
def add_category_to_database(category_name):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
    conn.commit()
    conn.close()
#function to add product to the products database
def add_product_to_database(product_name, product_price, product_quantity, category_id, product_unit):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, quantity, category_id, unit) VALUES (?, ?, ?, ?, ?)',
                   (product_name, product_price, product_quantity, category_id, product_unit))
    conn.commit()
    conn.close()
#function to get category name given category ID
def get_category_name(category_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
    category_name = cursor.fetchone()[0]
    conn.close()
    return category_name


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = [
    User(1, 'admin@gmail.com', 'admin123'),
    User(2, 'user@gmail.com', 'user123'),
    User(3, 'user2@gmail.com', 'user12345')
]
#function to check if username exists in the database
def get_user(username):
    for user in users:
        if user.username == username:
            return user
    return None

# Routes
@app.route('/') 
def home_page():
    return render_template('home.html')

@app.route('/user', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user.password == password:
            if username == 'user@gmail.com':
                return redirect(url_for('user_dashboard',username=username))
        else:
            return redirect(url_for('user_login'))
    return render_template('user_login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user.password == password:
            if username == 'admin@gmail.com':
                return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')


@app.route('/admin/create_category', methods=['POST'])
def create_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        add_category_to_database(category_name)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_category/<int:category_id>', methods=['POST'])
def edit_category(category_id):
    if request.method == 'POST':
        new_category_name = request.form['new_category_name']
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (new_category_name, category_id))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/remove_category/<int:category_id>', methods=['POST'])
def remove_category(category_id):
    if request.method == 'POST':
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/create_product', methods=['POST'])
def create_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = float(request.form['product_price'])
        product_quantity = int(request.form['product_quantity'])
        category_id = int(request.form['category_id'])
        product_unit=request.form['product_unit']
        add_product_to_database(product_name, product_price, product_quantity, category_id, product_unit)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    if request.method == 'POST':
        new_product_price = float(request.form['new_product_price'])
        new_product_quantity = int(request.form['new_product_quantity'])
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET price = ?, quantity = ? WHERE id = ?', (new_product_price, new_product_quantity, product_id))
        conn.commit()
        conn.close()
        
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    if request.method == 'POST':
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    categories = get_all_categories_from_database()
    products = get_all_products_from_database()
    return render_template('admin_dashboard.html', categories=categories, products=products)


@app.route('/user/dashboard/<username>', methods=['GET', 'POST'])
def user_dashboard(username):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    available_categories = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE name LIKE ?", ('%' + search_query + '%',))
        section_search_results = cursor.fetchall()
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_query + '%',))
        product_search_results = cursor.fetchall()
        search_results = []
        for section in section_search_results:
            search_results.append({
                'Type': 'Category',
                'Name': section[1],
                'ID': section[0]
            })
        for product in product_search_results:
            search_results.append({
                'Type': 'Product',
                'Name': product[1],
                'Price': product[2],
                'Quantity': product[3],
                'Unit': product[4],
                'ID': product[0]
            })
        conn.close()
        return render_template('user_dashboard.html', username=username, search_results=search_results)
    return render_template('user_dashboard.html', username=username, available_categories=available_categories)

@app.route('/user/cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}  
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    
    if product[3]<quantity:
        return f'only {product[3]} left' 
    
    elif product[3]<0:
        return f'out of stock'
        
    else:
        cart_item = {
            'name': product[1],
            'price': product[2],
            'quantity': quantity,
            'subtotal': product[2] * quantity,
            'unit' : product[5]
        }

        if product_id in session['cart']:
            session['cart'][product_id]['quantity'] += quantity
            session['cart'][product_id]['subtotal'] += cart_item['subtotal']
        else:
            session['cart'][product_id] = cart_item

        cursor.execute('SELECT * FROM cart WHERE product_id = ?', (product_id,))
        cartitem = cursor.fetchone()

        if cartitem is None:
            cursor.execute('INSERT INTO cart (product_id, product_name, price, quantity, subtotal, unit) VALUES (?, ?, ?, ?, ?, ?)',
                        (product_id, cart_item['name'], cart_item['price'], quantity, cart_item['subtotal'], cart_item['unit']))

        else:
            updated_quantity = cartitem[3] + quantity
            updated_subtotal = cartitem[4] + cart_item['subtotal']
            cursor.execute('UPDATE cart SET quantity = ?, subtotal = ? WHERE product_id = ?', (updated_quantity, updated_subtotal, product_id))
        conn.commit()
        conn.close()
        return redirect(request.referrer)

@app.route('/user/cart', methods=['GET'])
def view_cart():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()
    total_price = sum(item[4] for item in cart_items)
    conn.close()
    return render_template('view_cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/user/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))

@app.route('/user/display_category_products/<int:category_id>', methods=['GET'])
def display_category_products(category_id):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE category_id=?", (category_id,))
    products = cursor.fetchall()
    conn.close()
    category_name = get_category_name(category_id)

    return render_template('display_category_products.html', products=products, category_name=category_name)



@app.route('/user/checkout', methods=['POST'])
def checkout():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()
    for item in cart_items:
        cursor.execute('SELECT quantity FROM products WHERE id = ?', (item[0],))
        product_quantity = cursor.fetchone()[0]
        updated_quantity = product_quantity - item[3]
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (updated_quantity, item[0],))
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()
    session.pop('cart', None)
    return redirect(url_for('user_dashboard', username='username'))


if __name__ == '__main__':
    app.run(debug=True)
