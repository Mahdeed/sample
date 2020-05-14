from functools import wraps
import DBHandler as db
from flask import Flask, render_template, request, session, flash,redirect,url_for
from flask_socketio import SocketIO, emit
app = Flask(__name__)

socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'secret!'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

def is_user_login():
    if 'logged_in' in session:
        return True
    return False

def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('signin'))
    return wrap

@app.route('/')
def index():
    if is_user_login():
        return render_template("index.html", products=db.get_4_products(), user_login=True)
    else:
        return render_template("index.html", products=db.get_4_products(), user_login=False)

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    if request.method == "POST":
        session.pop('logged_in', None)
        session.pop('email', None)
        flash('You were logged out...!')
        return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        if is_user_login():
            return redirect(url_for('index'))
        else:
            return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Login", msg=None, user_login=False)
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
            session['logged_in'] = True
            session['email'] = email
            print(session['email'])
            print(data)
            user = {'account': account, 'name': data[1], 'email': data[3], 'address': data[5], 'phone': data[4]}
            # user will have data extracted from db for the buyer or the seller
            return redirect(url_for('profile', user=user["account"], username=user["name"], email=user["email"],
                                   address=user["address"], phone=user["phone"], user_login=True))
        else:
            errorMsg = 'Invalid email/password!!'
            return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Sign In", msg=errorMsg, user_login=False)

@app.route('/register', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if is_user_login():
            return redirect(url_for('index'))
        else:
            return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Register", msg=None, user_login=False)
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
        session['email'] = email
        if account == "Buyer":
            if db.isEmailExists_in_buyer(email):
                msg = 'Email already exists!!'
                print("data not inserted in buyer!")
                return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Register", msg=msg, user_login=False)
            else:
                print("data inserted!!")
                db.insert_into_Buyer(name, password, email, ' ', ' ', securityQuestion, answer)
                return redirect(url_for('signin'))
        else:
            if db.isEmailExists_in_seller(email):
                msg = 'Email already exists in seller!'
                print('DATA NOT INSERTED IN SELLER!')
                return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg=msg, user_login=False)
            else:
                db.insert_into_seller(name, '', email, '', password, 4, securityQuestion, answer)
                print("Data inserted into Seller!")
                return redirect(url_for('signin'))

@app.route('/cart', methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "GET":
        items = db.get_cart_items(session['email'])
        total = 0
        for x in items:
            total = total + x['price']
        charges = 0
        for x in items:
            charges = charges + x['charges']
        print(total)
        print(charges)
        return render_template("cart.html",products=items,total=total,charges=charges, user_login=True)
    else:
          print("hello from cart :)")
          id=request.form.get('id')
          data=db.get_product_by_id(id)
          buyerId=db.get_buyer_id(session['email'])
          db.insert_into_cart(buyerId)
          print(session['email'])
          cart=db.get_cart_no(buyerId)
          db.insert_into_cartItems(id, cart, 1)
          items=db.get_cart_items(session['email'])
          print(data)
          print(items)
          total = 0
          for x in items:
              total = total + x['price']
          charges = 0
          for x in items:
              charges = charges + x['charges']
          print(total)
          print(charges)
          return render_template("cart.html", products=items, total=total, charges=charges, user_login=True)

@app.route('/invoice', methods=["GET", "POST"])
@login_required
def invoice():
    if request.method == "GET":
           items = db.get_cart_items(session['email'])
           account,buyer = db.get_buyer_data(session['email'])
           total=0
           for x in items:
               total = total+x['price']
               total=total+x['charges']
           db.insert_into_invoice(buyer[1],buyer[0],total)
           print(total)
           return render_template("invoice.html",buyer=buyer, total=total, user_login=True)

@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        account,data = db.get_buyer_data(session['email'])
        if data == None:
            account, data = db.get_seller_data(session['email'])
        return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[2],
                               phone=data[4], user_login=True)
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
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[2], phone=data[4], user_login=True)
        else:
            db.insert_into_buyer_address_and_phoneN(session['email'], address, phoneNumber)
            db.get_buyer_data(session['email'])
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[5], phone=data[4], user_login=True)

@app.route('/edit_product', methods=["GET", "POST"])
@login_required
def edit_product():
    if request.method == "GET":
        return render_template("add_edit_product.html",title="Edit", name="shirt", type="men", warranty="2 years", price="123", charges="123", user_login=True)
    else:
        name = request.form.get('name')
        type = request.form.get('type')
        price = int(request.form.get('price'))
        warranty = int(request.form.get('warranty'))
        charges = int(request.form.get('charges'))
        email = 'mahad@kutta.com'
        id = db.get_seller_id(email)
        db.edit_product(name, price, warranty, type, charges, id)
        data=db.get_products_of_seller(email)
        return render_template("add_edit_product.html",title="Edit", name="cocaine", type="men", warranty="2 years", price="123",
                               charges="1234", user_login=True)

@app.route('/add_product',methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "GET":
        return render_template("add_edit_product.html", title="Add Product", name="Product Name", type="Type",
                               price="123", warranty="Years", charges="123", user_login=True)
    else:
        name = request.form.get('name')
        type = request.form.get('type')
        price = int(request.form.get('price'))
        warranty = int(request.form.get('warranty'))
        charges = int(request.form.get('charges'))
        email = session['email']
        id = db.get_seller_id(email)
        db.insert_into_product(name, price, warranty, type, charges, id)
        data = db.get_products_of_seller(email)
        return render_template("add_edit_product.html", name="product", type=" ", warranty=" ", price=" ",
                               charges=" ",products=data, user_login=True)

@app.route('/product')
def product():
    if is_user_login():
        return render_template("product.html", products=db.get_all_products(), user_login=True)
    else:
        return render_template("product.html", products=db.get_all_products(),user_login=False)

@app.route('/forget_password', methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        if db.isEmailExists_in_buyer(request.form.get('email')):
            session['email'] = request.form.get('email')
            session['forget'] = True
            return redirect(url_for("security_question"))
        elif db.isEmailExists_in_seller(request.form.get('email')):
            session['email'] = request.form.get('email')
            session['forget'] = True
            return redirect(url_for("security_question"))
        else:
            return render_template("forget.html", user_login=False)

    if is_user_login():
        return redirect(url_for('index'))
    else:
        return render_template("forget.html", user_login=False)

@app.route('/security_question', methods=["POST", "GET"])
def security_question():
    if request.method == "POST":
        securityQuestion = request.form.get('securityQuestion')
        answer = request.form.get('answer')
        if db.is_security_question_and_answer_correct_in_buyer(session['email'], securityQuestion, answer):
            session.pop('forget',None)
            session['security'] = True
            return redirect(url_for("reset_password", email=session['email']))
        elif db.is_security_question_and_answer_correct_in_seller(session['email'], securityQuestion, answer):
            session.pop('forget', None)
            session['security'] = True
            return redirect(url_for("reset_password", email=session['email']))
    else:
        if is_user_login():
            return redirect(url_for('index'))
        else:
            if 'forget' in session:
                return render_template("security.html",user_login=False)
            else:
                return redirect(url_for('signin'))

@app.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        password = request.form.get('password')
        if db.isEmailExists_in_buyer(session['email']):
            db.insert_password_in_buyer(session['email'], password)
            session.pop('security', None)
            return redirect(url_for('signup'))
        else:
            db.insert_password_in_seller(session['email'], password)
            session.pop('security', None)
            return redirect(url_for('signup'))
    else:
        if is_user_login():
            return redirect(url_for('index'))
        else:
            if 'security' in session:
                return render_template("reset.html", email=session['email'],user_login=False)
            else:
                return redirect(url_for('signin'))

@app.route('/product/<int:id>')
@login_required
def product_detail(id):
    return render_template("product-detail.html",user_login=True)

@app.route('/product/filter', methods=["GET", "POST"])
@login_required
def filter():
    if request.method == "POST":
        list_category = request.form.getlist('category')
        print(list_category)
        lower_price = request.form.get('lower_price')
        higher_price = request.form.get('higher_price')
        if lower_price and higher_price is not None:
            print(db.get_products_in_range(int(lower_price), int(higher_price)))

        return render_template("product.html",user_login=True)

@app.route('/product/search', methods=["GET", "POST"])
@login_required
def search_product():
    if request.method == "POST":
        name = request.form.get('search-product')
        data = db.get_product_by_name(name)
        return render_template("product.html", products=data,user_login=True)
    else:
        return redirect(url_for('product'))

@socketio.on('connect')
def connect():
    print("Socket connected")
    emit('connetion',"Done",request.sid)

@socketio.on('event')
def event(data):
    print(request.sid)
    print(data['name'])

############### Static Pages ################################
@app.route('/faq')
def faq():
    if is_user_login():
        return render_template("faq.html",user_login=True)
    else:
        return render_template("faq.html", user_login=False)

@app.route('/terms_conditions')
def terms_conditions():
    if is_user_login():
        return render_template("terms_and_condition.html",user_login=True)
    else:
        return render_template("terms_and_condition.html", user_login=False)

@app.route('/privacy_agreement')
def privacy_agreement():
    if is_user_login():
        return render_template("privacy.html",user_login=True)
    else:
        return render_template("privacy.html", user_login=False)

@app.route('/contact')
def contact():
    if is_user_login():
        return render_template("contact.html",user_login=True)
    else:
        return render_template("contact.html", user_login=False)

@app.route('/about')
def about():
    if is_user_login():
        return render_template("about.html",user_login=True)
    else:
        return render_template("about.html", user_login=False)

if __name__ == '__main__':
    socketio.run(app)
