import DBHandler as db
from flask import Flask, render_template, request, session
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route('/')
def index():
    return render_template("index.html", products=db.get_4_products())

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
            print(data)
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

@app.route('/cart')
def cart():
    return render_template("cart.html",products=[{'id': "03", 'name': "Jeans", 'price': "200", 'quantity': "3"}])

@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        account, data = db.get_buyer_data(session['email'])
        print(data)
        if data == None:
            account, data = db.get_seller_data(session['email'])
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[2], phone=data[4])
        else:
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[5], phone=data[4])
    else:
        email = request.form.get(session['email'])
        address = request.form.get('address')
        phoneNumber = request.form.get('phoneNumber')
        account, data = db.get_buyer_data(session['email'])
        print(data)
        if data == None:
            account, data = db.get_seller_data(session['email'])
            db.insert_into_seller_address_and_phoneN(session['email'], address, phoneNumber)
            data = db.get_seller_data(session['email'])
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[2], phone=data[4])
        else:
            db.insert_into_buyer_address_and_phoneN(session['email'], address, phoneNumber)
            db.get_buyer_data(session['email'])
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[5], phone=data[4])

@app.route('/edit_product')
def edit_product():
    return render_template("add_edit_product.html", title="Edit", product_name="Shirt", type="Mens", price= "123", warranty="2 years", charges="123")

@app.route('/add_product')
def add_product():
    return render_template("add_edit_product.html", title="Add Product", product_name="Product Name", type="Type", price= "123", warranty="Years", charges="123")


@app.route('/product')
def product():
    return render_template("product.html", products=db.get_all_products())






@app.route('/forget_password', methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        session['email'] = request.form.get('email')
        if db.isEmailExists_in_buyer(session['email']):
            return render_template("security.html")
        elif db.isEmailExists_in_seller(session['email']):
            return render_template("security.html")
        else:
            return render_template("forget.html")

    return render_template("forget.html")

@app.route('/security_question', methods=["POST", "GET"])
def security_question():
    if request.method == "POST":
        securityQuestion = request.form.get('securityQuestion')
        answer = request.form.get('answer')
        if db.is_security_question_and_answer_correct(session['email'], securityQuestion, answer):
            return render_template("reset.html", email=session['email'])
    else:
        return render_template("security.html")

@app.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        password = request.form.get('password')
        if db.isEmailExists_in_buyer(session['email']):
            db.insert_password_in_buyer(session['email'], password)
            return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg='')
        else:
            db.insert_password_in_seller(session['email'], password)
            return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg='')
    else:
        return render_template("reset.html", email=session['email'])

@app.route('/product/<int:id>')
def product_detail(id):
    return render_template("product-detail.html")

@app.route('/product/search')
def search():
    pass

@app.route('/product/filter', methods=["GET", "POST"])
def filter():
    if request.method == "POST":
        list_category = request.form.getlist('category')
        print(list_category)
        lower_price = request.form.get('lower_price')
        higher_price = request.form.get('higher_price')
        if lower_price and higher_price is not None:
            print(db.get_products_in_range(int(lower_price), int(higher_price)))

        return render_template("product.html")

############### Static Pages ################################
@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()
