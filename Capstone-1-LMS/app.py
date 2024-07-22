from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, session, flash
from auth_service import authenticate
from book_service import get_books, add_to_cart, get_cart, calculate_due_date, get_books_by_ids
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/Capstone11'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define SQLAlchemy models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('Book', backref='user')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    issue_date = db.Column(db.DateTime, default=datetime.now)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create tables function within app context
with app.app_context():
    db.create_all()

    # Check if the 'admin' user already exists
    existing_user = User.query.filter_by(username='admin').first()
    if not existing_user:
        admin = User(username='admin')
        db.session.add(admin)
        db.session.commit()
    

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('book_management'))
        else:
            return "Login failed"
    return render_template('login_page.html')



@app.route('/book_management', methods=['GET', 'POST'])
def book_management():
    books = get_books()
    
    # Organize books by category
    books_by_category = {}
    for book in books:
        if book['category'] not in books_by_category:
            books_by_category[book['category']] = []
        books_by_category[book['category']].append(book)
    
    if request.method == 'POST':
        selected_books = request.form.getlist('book')
        existing_books = [book['id'] for book in get_cart()]

        duplicate_books = []
        new_books = []

        for book_id in selected_books:
            if int(book_id) in existing_books:
                duplicate_books.append(book_id)
            else:
                new_books.append(book_id)

        if duplicate_books:
            duplicate_titles = [book['title'] for book in get_books_by_ids(duplicate_books)]
            flash(f'Duplicate books not added: {", ".join(duplicate_titles)}', 'danger')

        if new_books:
            add_to_cart(new_books)
            save_books_to_db(new_books)
            flash('Books added to cart successfully.', 'success')
        
        return redirect(url_for('cart'))
    
    return render_template('book_management_page.html', books_by_category=books_by_category)

def save_books_to_db(selected_books):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    books_data = get_books_by_ids(selected_books)
    for book_data in books_data:
        book = Book(
            title=book_data['title'],
            category=book_data['category'],
            issue_date=datetime.now(),
            end_date=calculate_due_date(datetime.now()),
            user_id=user.id
        )
        db.session.add(book)
    db.session.commit()

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('login'))
    
    cart_items = get_cart()
    start_date = datetime.now()
    cart_with_dates = [(book, calculate_due_date(start_date)) for book in cart_items]
    return render_template('cart_page.html', cart_items=cart_with_dates)

# Test Db connection
@app.route('/test_db')
def test_db():
    try:
        users = User.query.all()
        return f"Users: {[user.username for user in users]}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
