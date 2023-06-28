from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY'] = 'HeisKing!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_homepage():
    return render_template('home.html')

@app.route('/users')
def user_screen():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET'])
def add_user_form():
    return render_template('new_user.html')

@app.route('/users/add', methods=['POST'])
def add_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_page.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_update.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#Posts routes -----------------------------------------------------------------------------------

@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/posts/<int:post_id>')
def posts_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_page.html', post=post)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

