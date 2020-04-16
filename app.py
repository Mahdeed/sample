from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return render_template("sign_in_sign_up_slider_form.html")

@app.route('/login', methods=["GET","POST"])
def login():
    return "Login Successfully!"

@app.route('/signup', methods=["GET","POST"])
def signup():
    return "SignUp Successfully!"

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/product')
def product():
    return render_template("product.html")


@app.route('/<int:id>')
def product_detail(id):
    return render_template("product-detail.html")


if __name__ == '__main__':
    app.run()
