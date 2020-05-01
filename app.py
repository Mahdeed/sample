from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Sign In")

@app.route('/signup')
def signup():
    return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/profile')
def profile():
    return render_template("profile.html", user="seller", username="Ecommerce", email="bcsf17@gmail.com", address="Lahore", phone="0900780601")

@app.route('/edit_product')
def edit_product():
    return render_template("add_edit_product.html", title="Edit", product_name="Shirt", type="Mens", price= "123", warranty="2 years", charges="123")

@app.route('/add_product')
def add_product():
    return render_template("add_edit_product.html", title="Add Product", product_name="Product Name", type="Type", price= "123", warranty="Years", charges="123")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/product')
def product():
    return render_template("product.html")

@app.route('/forget_password')
def forget_password():
    return render_template("forget.html")

@app.route('/security_question')
def security_question():
    return render_template("security.html")

@app.route('/reset_password')
def reset_password():
    return render_template("reset.html", email="bcsf17a@pucit.edu.pk")

@app.route('/<int:id>')
def product_detail(id):
    return render_template("product-detail.html")

if __name__ == '__main__':
    app.run()
