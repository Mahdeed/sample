import DBHandler as db
from flask import Flask, render_template, request, session
app = Flask(__name__)


@app.route('/')
def index():
    db.connect()
    # data = db.get_buyer_data("b@gmail.com")
    # print(data)
    return render_template("index.html", products=[{'id': "03", 'name': "Jeans", 'price': "200"}])


@app.route('/logout')
def logout():
   session.pop('email', None)
   return render_template('index.html')



@app.route('/login', methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Login", msg=None)
    else:
        print("Signin")
        errorMsg = ' '
        email = request.form.get("email")
        password = request.form.get("password")
        # function to chck valid email and password:
        if db.isEmailExists_in_buyer(email):
            if db.isPasswordCorrect_in_buyer(email, password):
                account, data = db.get_buyer_data(email)
        else:
            if db.isPasswordCorrect_in_seller(email, password):
                account, data = db.get_seller_data(email)

        if data is not None:
            session['email'] = email
            print("Printing user data in app.py and the function signin : " + data)
            user = {'account': account, 'name': data[1], 'email': data[3], 'address': data[5], 'phone': data[4]}
            # user will have data extracted from db for the buyer or the seller
            return render_template("profile.html", user=user["account"], username=user["name"], email=user["email"],
                                   address=user["address"], phone=user["phone"])
        else:
            errorMsg = 'Invalid email/password!!'
            return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Sign In", msg=errorMsg)

@app.route('/register', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Register", msg=None)
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        securityQuestion = request.form.get("securityQuestion")
        answer = request.form.get("answer")
        account = request.form.get("account")
        print(name)
        print(email)
        print(password)
        print(securityQuestion)
        print(answer)
        print(account)
        if account == "Buyer":
            if db.isEmailExists_in_buyer(email):
                msg = 'Email already exists!!'
                print("data not inserted in buyer!")
                return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg=msg)
            else:
                print("data inserted!!")
                db.insert_into_Buyer(name, password, email, ' ', ' ', securityQuestion, answer)
                return render_template("index.html")
        else:
            if db.isEmailExists_in_seller(email):
                msg = 'Email already exists in seller!'
                print('DATA NOT INSERTED IN SELLER!')
                return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg=msg)
            else:
                db.insert_into_seller(name, '', email, '', password, '', securityQuestion, answer)
                print("Data inserted into Seller!")

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

@app.route('/forget')
def forget_password_form():
    return render_template("forget.html")

@app.route('/question')
def security_question_form():
    return render_template("security.html")

@app.route('/reset')
def reset_password_form():
    return render_template("reset.html", email="bcsf17a@pucit.edu.pk")

@app.route('/forget_password')
def forget_password():
    return render_template("forget.html")

@app.route('/security_question')
def security_question():
    return render_template("security.html")

@app.route('/reset_password')
def reset_password():
    return render_template("reset.html", email="bcsf17a@pucit.edu.pk")

@app.route('/product/<int:id>')
def product_detail(id):
    return render_template("product-detail.html")

if __name__ == '__main__':
    app.run()
