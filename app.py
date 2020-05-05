from flask import Flask, render_template, request, session
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin',  methods=['GET', 'POST'])
def signin():
    errorMsg = ' '
    email = request.form['email']
    password = request.form['password']
    if True:
      #function to chck valid email and password:
            session['email'] = email
            user = {}
            #user will have data extracted from db for the buyer or the seller
            return render_template("profile.html", user=user["account"], username=user["name"], email=user["email"],
                       address=user["address"], phone=user["phone"])

    else:
        errorMsg = 'invalid email/password'
        return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign In", msg=errorMsg)

@app.route('/logout')
def logout():
   session.pop('email', None)
   return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    msg = ' '
    name = request.form("Name")
    email = request.form("Email")
    password = request.form("Password")
    securityQuestion = request.form("securityQuestion")
    answer = request.form("answer")
    account = request.form("account")
    user = {
        "name": name,
        "email": email,
        "password": password,
        "securityQuestion": securityQuestion,
        "answer": answer,
        "account": account,
    }
    if True:
    #check if the account pahle se exists:
          msg = 'email already exists'
          return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg=msg)
    else:
          #insert in db
          return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route('/profile')
def profile():
    return render_template("profile.html", user="seller", username="abc", email="bcsf17@gmail.com", address="address", phone="090078601")

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
