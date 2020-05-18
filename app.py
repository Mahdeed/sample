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

def buyer_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'buyer' in session:
            return test(*args,**kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

def seller_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'seller' in session:
            return test(*args,**kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            return redirect(url_for('signin'))
    return wrap

@app.route('/')
def index():
    if is_user_login():
        return render_template("index.html", products=db.get_4_products(), user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("index.html", products=db.get_4_products(), user_login=False,buyer_login=('buyer' in session))

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    if request.method == "POST":
        session.pop('logged_in', None)
        if 'buyer' in session:
            session.pop('buyer', None)
        else:
            session.pop('seller', None)
        session.pop('email', None)
        return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        if is_user_login():
            return redirect(url_for('index'))
        else:
            return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Login", msg=None, user_login=False,buyer_login=('buyer' in session))
    else:
        print("Signin")
        errorMsg = ' '
        email = request.form.get("email")
        password = request.form.get("password")
        # function to chck valid email and password:
        if db.isEmailExists_in_buyer(email):
            if db.isPasswordCorrect_in_buyer(email, password):
                account, data = db.get_buyer_data(email)
                session['buyer'] = True
        else:
            if db.isPasswordCorrect_in_seller(email, password):
                account, data = db.get_seller_data(email)
                session['seller'] = True

        if data is not None:
            session['logged_in'] = True
            session['email'] = email
            print(session['email'])
            print(data)
            user = {'account': account, 'name': data[1], 'email': data[3], 'address': data[5], 'phone': data[4]}
            # user will have data extracted from db for the buyer or the seller
            return redirect(url_for('profile'))
        else:
            errorMsg = 'Invalid email/password!!'
            return render_template("sign_in_sign_up_slider_form.html", signin=True, title="Sign In", msg=errorMsg, user_login=False,buyer_login=('buyer' in session))

@app.route('/register', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if is_user_login():
            return redirect(url_for('index'))
        else:
            return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Register", msg=None, user_login=False,buyer_login=('buyer' in session))
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
                return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Register", msg=msg, user_login=False,buyer_login=('buyer' in session))
            else:
                print("data inserted!!")
                db.insert_into_Buyer(name, password, email, ' ', ' ', securityQuestion, answer)
                return redirect(url_for('signin'))
        else:
            if db.isEmailExists_in_seller(email):
                msg = 'Email already exists in seller!'
                print('DATA NOT INSERTED IN SELLER!')
                return render_template("sign_in_sign_up_slider_form.html", signin=False, title="Sign Up", msg=msg, user_login=False,buyer_login=('buyer' in session))
            else:
                db.insert_into_seller(name, '', email, '', password, 4, securityQuestion, answer)
                print("Data inserted into Seller!")
                return redirect(url_for('signin'))

@app.route('/cart')
@login_required
@buyer_required
def cart():
    if request.method == "GET":
        items = db.get_cart_items(session['email'])
        total = 0
        for x in items:
            total = total + (x['price'] * x['quantity'])
        charges = 0
        for x in items:
            charges = charges + x['charges']
        print(total)
        print(charges)
        return render_template("cart.html",products=items,total=total,charges=charges, user_login=True,buyer_login=('buyer' in session))

@app.route('/invoice')
@login_required
@buyer_required
def invoice():
       items = db.get_cart_items(session['email'])
       account,buyer = db.get_buyer_data(session['email'])
       total=0
       for x in items:
           total = total+(x['price'] * x['quantity'])
           total=total+x['charges']
       db.insert_into_invoice(buyer[1],buyer[0],total)
       print(total)
       return render_template("invoice.html",buyer=buyer, total=total, user_login=True,buyer_login=('buyer' in session))

@app.route('/product_delete/<int:id>', methods=["GET", "POST"])
@login_required
@seller_required
def delete_product(id):
    if request.method == "POST":
        product_data = db.get_product_by_id(id);
        if product_data:
            print("Delete Data in app.py")
            print(product_data)
            db.remove_product_from_product_table_via_id(id)
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('pageNotFound'))
    else:
        return redirect(url_for('pageNotFound'))

@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        seller_product = None
        account,data = db.get_buyer_data(session['email'])
        if data == None:
            account, data = db.get_seller_data(session['email'])
            seller_product = db.get_products_of_seller(session['email'])
        return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[5],
                               phone=data[4], user_login=True, seller_product=seller_product,buyer_login=('buyer' in session))
    else:
        account, data = db.get_buyer_data(session['email'])
        address = request.form.get('address')
        if not address:
            address =data[5]
        phoneNumber = request.form.get('phoneNumber')
        if not phoneNumber:
            phoneNumber=data[4]
        account, data = db.get_buyer_data(session['email'])
        print(data)
        print("profile data")
        print(address)
        print(phoneNumber)
        if data == None:
            account, data = db.get_seller_data(session['email'])
            db.insert_into_seller_address_and_phoneN(session['email'], address, phoneNumber)
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[2], phone=data[4], user_login=True,buyer_login=('buyer' in session))
        else:
            db.insert_into_buyer_address_and_phoneN(session['email'], address, phoneNumber)
            return render_template("profile.html", user=account, username=data[1], email=data[3], address=data[5], phone=data[4], user_login=True,buyer_login=('buyer' in session))

@app.errorhandler(404)
def page_not_found(e):
    if is_user_login():
        return render_template('404.html', user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template('404.html', user_login=False, buyer_login=('buyer' in session))

@app.route('/404')
def pageNotFound():
    if is_user_login():
        return render_template('404.html', user_login=True, buyer_login=('buyer' in session))
    else:
        return render_template('404.html', user_login=False, buyer_login=('buyer' in session))

@app.route('/edit_product/<int:id>', methods=["GET", "POST"])
@login_required
@seller_required
def edit_product(id):
    if request.method == "GET":
        product_data = db.get_product_by_id(id)
        print("Check exist or not:")
        print(product_data)
        if product_data:
            print("Edit Data in app.py")
            print(product_data)
            return render_template("add_edit_product.html",title="Edit",ids=product_data[0]['id'],product_name=product_data[0]['name'],  name=product_data[0]['name'], type=product_data[0]['type'], warranty=product_data[0]['warranty'], quantity= product_data[0]['quantity'], price=product_data[0]['price'], charges=product_data[0]['charges'], user_login=True,buyer_login=('buyer' in session))
        else:
            return redirect(url_for('pageNotFound'))

    else:
        product_data = db.get_product_by_id(id)
        name = request.form.get('name')
        if not name:
            name=product_data[0]['name']
        type = request.form.get('type')
        if not type:
            type=product_data[0]['type']
        price = request.form.get('price')
        if price:
            price = int(price)
        else:
            price=product_data[0]['price']
        warranty = request.form.get('warranty')
        if warranty:
            warranty = int(warranty)
        else:
            warranty = product_data[0]['warranty']
        charges = request.form.get('charges')
        if charges:
            charges = int(charges)
        else:
            charges=product_data[0]['charges']
        email = session['email']
        seller_id = db.get_seller_id(email)
        db.edit_product(name, price, warranty, type, charges, seller_id,id)
        return redirect(url_for('profile'))

@app.route('/add_product',methods=["GET", "POST"])
@login_required
@seller_required
def add_product():
    if request.method == "GET":
        return render_template("add_edit_product.html", title="Add Product", name="Product Name", type="Type",
                               price="123", quantity='20', warranty="Years", charges="123", user_login=True,buyer_login=('buyer' in session))
    else:
        name = request.form.get('name')
        type = request.form.get('type')
        price = int(request.form.get('price'))
        quantity = int(request.form.get('quantity'))
        warranty = request.form.get('warranty')
        if warranty:
            warranty=int(warranty)
        charges = request.form.get('charges')
        if charges:
            charges=int(charges)
        email = session['email']
        id = db.get_seller_id(email)
        db.insert_into_product(name, price, warranty, type, charges, id,quantity)
        return redirect(url_for('profile'))

@app.route('/product')
def product():
    if is_user_login():
        return render_template("product.html", products=db.get_all_products(), user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("product.html", products=db.get_all_products(),user_login=False,buyer_login=('buyer' in session))

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
            return render_template("forget.html", user_login=False,buyer_login=('buyer' in session))

    if is_user_login():
        return redirect(url_for('index'))
    else:
        return render_template("forget.html", user_login=False,buyer_login=('buyer' in session))

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
                return render_template("security.html",user_login=False,buyer_login=('buyer' in session))
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
                return render_template("reset.html", email=session['email'],user_login=False,buyer_login=('buyer' in session))
            else:
                return redirect(url_for('signin'))

@app.route('/product/<int:id>')
def product_detail(id):
    product_data = db.get_product_by_id(id);
    print("Check exist or not:")
    print(product_data)
    if product_data:
        if is_user_login():
            return render_template("product-detail.html",id = product_data[0]['id'], name=product_data[0]['name'],price=product_data[0]['price'], user_login=True,buyer_login=('buyer' in session))
        else:
            return render_template("product-detail.html", id = product_data[0]['id'], name=product_data[0]['name'],price=product_data[0]['price'], user_login=False,buyer_login=('buyer' in session))
    else:
        return redirect(url_for('pageNotFound'))

@app.route('/product/filter', methods=["GET", "POST"])
def filter():
    if request.method == "POST":
        lower_price = request.form.get('lower_price')
        higher_price = request.form.get('higher_price')
        msg = 'Search: \t'
        if lower_price and higher_price is not None:
            print(db.get_products_in_range(int(lower_price), int(higher_price)))

        if(lower_price):
            msg += 'Price: '+lower_price
        if(higher_price):
            msg += ' to '+higher_price

        flash(msg)

        if is_user_login():
            return render_template("product.html",products=db.get_products_in_range(lower_price,higher_price),user_login=True,buyer_login=('buyer' in session))
        else:
            return render_template("product.html", products=db.get_products_in_range(lower_price,higher_price), user_login=False,buyer_login=('buyer' in session))
    else:
        return redirect(url_for('product'))

@app.route('/product/search', methods=["GET", "POST"])
def search_product():
    if request.method == "POST":
        name = request.form.get('search-product')
        print(name)
        flash('Search: ' + name)
        data = db.get_product_by_name(name)
        if is_user_login():
            return render_template("product.html", products=data,user_login=True,buyer_login=('buyer' in session))
        else:
            return render_template("product.html", products=data, user_login=False,buyer_login=('buyer' in session))
    else:
        return redirect(url_for('product'))

@app.route('/product/<search>', methods=["GET", "POST"])
def index_button(search):
    name = search
    print(name)
    flash('Search: ' + name)
    data = db.get_product_by_name(name)
    print(data)
    if data:
        if is_user_login():
            return render_template("product.html", products=data,user_login=True,buyer_login=('buyer' in session))
        else:
            return render_template("product.html", products=data, user_login=False,buyer_login=('buyer' in session))
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

@socketio.on('add_to_cart')
def add_to_cart(data):
    if(data['id'] == None):
        print(data['check'])
        print(data['all_data'])
        buyer_email = db.get_buyer_id(session['email'])
        if (buyer_email):
            for all_products in data['all_data']:
                db.insert_into_cart(buyer_email, all_products['id'], all_products['quantity'])
    else:
        print(data['check'])
        print(data['id'])
        print(data['quantity'])
        print(data['all_data'])
        buyer_email = db.get_buyer_id(session['email'])
        if (buyer_email):
            db.insert_into_cart(buyer_email,data['id'],data['quantity'])

@socketio.on('update_cart')
def update_cart(data):
    print(data['check'])
    db.remove_from_cart_via_email(session['email'])
    emit('cart_removed_via_email',True,request.sid)

@socketio.on('remove_from_cart')
def remove_from_cart(data):
    print(data['check'])
    print(data['id'])
    buyer_email = db.get_buyer_id(session['email'])
    if (buyer_email):
        db.remove_from_cart(buyer_email,data['id'])
    else:
        db.remove_from_cart(db.get_seller_id(session['email']),data['id'])

    items = db.get_cart_items(session['email'])
    total = 0
    for x in items:
        total = total + (x['price'] * x['quantity'])
    charges = 0
    for x in items:
        charges = charges + x['charges']
    print(total)
    print(charges)
    emit('charges_total_header',{'total':total+charges,'charges':charges},request.sid)

@socketio.on('add_to_wishlist')
def add_to_wishlist(data):
    print(data['check'])
    print(data['id'])
    buyer_email = db.get_buyer_id(session['email'])
    if(buyer_email):
        db.insert_into_wish_list(buyer_email,data['id'])
    else:
        db.insert_into_wish_list(db.get_seller_id(session['email']), data['id'])

@socketio.on('remove_from_wishlist')
def remove_from_wishlist(data):
    print(data['check'])
    print(data['id'])
    buyer_email = db.get_buyer_id(session['email'])
    if (buyer_email):
        db.remove_from_wishlist(buyer_email,data['id'])
    else:
        db.remove_from_wishlist(db.get_seller_id(session['email']), data['id'])

@socketio.on('wishlistItem')
def wishlistItem(data):
    print(data['check'])
    print(data['flag'])
    items = db.get_wishlist(session['email'])
    print(items)
    emit('wishlistItem',{'html':render_template('header_wishlist.html',products=items),'flag':data['flag']},request.sid)

@socketio.on('viewCartItem')
def viewCartItem(data):
    print(data['check'])
    print(data['flag'])
    items = db.get_cart_items(session['email'])
    total = 0
    for x in items:
        total = total + (x['price']* x['quantity'])
    charges = 0
    for x in items:
        charges = charges + x['charges']
    print(total)
    print(charges)
    emit('viewCartItem',{'html':render_template('header_cart.html',products=items,total=total+charges,charges=charges),'flag':data['flag']},request.sid)

############### Static Pages ################################
@app.route('/faq')
def faq():
    if is_user_login():
        return render_template("faq.html",user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("faq.html", user_login=False,buyer_login=('buyer' in session))

@app.route('/terms_conditions')
def terms_conditions():
    if is_user_login():
        return render_template("terms_and_condition.html",user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("terms_and_condition.html", user_login=False,buyer_login=('buyer' in session))

@app.route('/privacy_agreement')
def privacy_agreement():
    if is_user_login():
        return render_template("privacy.html",user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("privacy.html", user_login=False,buyer_login=('buyer' in session))

@app.route('/contact')
def contact():
    if is_user_login():
        return render_template("contact.html",user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("contact.html", user_login=False,buyer_login=('buyer' in session))

@app.route('/about')
def about():
    if is_user_login():
        return render_template("about.html",user_login=True,buyer_login=('buyer' in session))
    else:
        return render_template("about.html", user_login=False,buyer_login=('buyer' in session))

if __name__ == '__main__':
    socketio.run(app)
