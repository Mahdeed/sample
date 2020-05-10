import pymysql as sql

DATABASEIP = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DATABASE = "e_commerce"

def connect():
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DB is connected")
    except Exception as e :
        print("Error DB could not be connected(connect function)")


## FUNCTIONS TO INSERT DATA INTO DATABASE START FROM HERE ##
#############################################################################################


#Function to insert info into 'buyer' table #
def insert_into_Buyer(name, password, email, phoneNumber, address, securityQuestion, answer):
    print("insert_into_Buyer")
    try:
        if isEmailExists_in_seller(email):
            return None
        else:
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED in insert_into_Buyer")
            query = "INSERT INTO buyer(name, password, email, phoneNumber, address, securityQuestion, answer)VALUES(%s, %s, %s, %s, %s, %s, %s)"
            args = (name, password, email, phoneNumber, address, securityQuestion, answer)
            cursor.execute(query, args)
            print("Record inserted into the table 'buyer' ")
    except Exception as e:
        print(str(e))
    finally:
        db.commit()
        db.close()


# FUNCTION to insert only password for table 'buyer'#
def insert_password_in_buyer(email, password):
    print("insert_password_in_buyer(email, password)")
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED in insert_into_Buyer")
        query = "INSERT INTO buyer(password)VALUES(%s) WHERE email = %s"
        args = (password, email)
        cursor.execute(query, args)
        print("Record inserted into the table 'buyer', password inserted ")
    except Exception as e:
        print(str(e))
    finally:
        db.commit()
        db.close()


# Function to insert info into 'buyer' table ###... address and phone Number
def insert_into_buyer_address_and_phoneN(email ,address, phoneNumber):
    print('insert_into_buyer_address_and_phoneN(email ,address, phoneNumber)')
    try:
        if isEmailExists_in_buyer(email):
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED in insert_into_Buyer")
            query = "INSERT INTO buyer(phoneNumber, address)VALUES(%s, %s) WHERE email = %s"
            args = (phoneNumber, address, email)
            cursor.execute(query, args)
            print("Record inserted into the table 'buyer' address and phoneNumber ")
    except Exception as e:
        print(str(e))
    finally:
        db.commit()
        db.close()


# Function to insert info into the 'cart' table
def insert_into_cart(cartNo, quantity):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print('DATABASE for cart function connected')
        query = 'INSERT INTO cart (cartNo, quantity) VALUES (%s, %s)'
        args = (cartNo, quantity)
        cur.execute(query, args)
        print('Record inserted into the table \'cart\' ')
    except Exception as e:
        print(str(e))
    finally:
        db.commit()
        db.close()

# Function to insert info into the 'invoice' table
def insert_into_invoice(invoiceNumber, name, customerId, totalCost):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "INSERT INTO invoice(invoiceNumber, name, customerId, totalCost)VALUES(%s, %s, %s, %s)"
        args = (invoiceNumber, name, customerId, totalCost)
        cursor.execute(query, args)
        print("Record inserted into the table 'invoice' ")

    except Exception as e :
        print("Error DB could not be connected")
    finally:
        db.commit()
        db.close()

# Function to insert info into the 'order' table
def insert_into_order(orderNo, shipmentFee):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "INSERT INTO order(orderNo, shipmentFee)VALUES(%s, %s)"
        args = (orderNo, shipmentFee)
        cursor.execute(query, args)
        print("Record inserted into the table 'order' ")

    except Exception as e :
        print("Error DB could not be connected")
    finally:
        db.commit()
        db.close()

#Function to insert info into 'product' table #
def insert_into_product(name, price, rating, warranty, type, deliveryCharges, seller):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "INSERT INTO product(name, price, rating, warranty, type, deliveryCharges, seller)VALUES(%s, %s, %s, %s, %s, %s, %s)"
        args = (name, price, rating, warranty, type, deliveryCharges, seller)
        cursor.execute(query, args)
        print("Record inserted into the table 'product' ")
    except Exception as e:
        print("Error DB could not be connected")
    finally:
        db.commit()
        db.close()

#Function to insert info into 'seller' table #
def insert_into_seller(name, address, email, phoneNumber, password, ranking, securityQuestion, answer):
    try:
        if isEmailExists_in_buyer():
            return None
        else:
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED")
            query = "INSERT INTO buyer(name, address, email, phoneNumber, password, ranking, securityQuestion, answer)VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            args = (name, address, email, phoneNumber, password, ranking, securityQuestion, answer)
            cursor.execute(query, args)
            print("Record inserted into the table 'seller' ")
    except Exception as e:
        print("Error DB could not be connected")
    finally:
        db.commit()
        db.close()

# FUNCTION to insert only password for table 'buyer'#
def insert_password_in_seller(email, password):
    print("insert_password_in_seller(email, password)")
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED in insert_into_Buyer")
        query = "INSERT INTO seller(password)VALUES(%s) WHERE email = %s"
        args = (password, email)
        cursor.execute(query, args)
        print("Record inserted into the table 'seller', password inserted ")
    except Exception as e:
        print(str(e))
    finally:
        db.commit()
        db.close()



# Function to insert info into 'buyer' table ###... address and phone Number
def insert_into_seller_address_and_phoneN(email ,address, phoneNumber):
    print('insert_into_seller_address_and_phoneN(email ,address, phoneNumber)')
    try:
        if isEmailExists_in_buyer(email):
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED in insert_into_Buyer")
            query = "INSERT INTO seller(phoneNumber, address)VALUES(%s, %s) WHERE email = %s"
            args = (phoneNumber, address, email)
            cursor.execute(query, args)
            print("Record inserted into the table 'seller' address and phoneNumber ")
    except Exception as e:
        print(str(e))
    finally:
        db.commit()
        db.close()


#### FUNCTIONS TO 'INSERT' INTO DB "ENDDD" HEREEEE ####
#################################################################################################################################







#### FUNCTIONS TO GETT USEERRRR DATA STARTTT HEREEE ######
#################################################################################################################################

#Function to get data from the table 'buyer'
def get_buyer_data(email):
    print('get_buyer_data()')
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT * FROM buyer where email = %s'
        args = email
        cur.execute(query, args)
        data = cur.fetchone()
        if (len)(data) < 1:
            data = None
        print("Record obtained from the table 'buyer' ")
    except Exception as e:
        print("Error DB could not be connected")
    finally:
        db.close()
        return "buyer", data

#Function to get wishlist from the table 'buyer'
def get_wishlist(email):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT p.name, p.price, p.rating, p.warranty, p.type, p.deliveryCharges FROM wish_list w, buyer b, product p  where b.email = %s AND w.id=b.wish_list'
        args = email
        cur.execute(query, args)
        wish_list = cur.fetchone()
        if (len)(wish_list) < 1:
            wish_list = None
        print(wish_list)
        print("Record obtained from the table 'wish_list'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from wish_list table")
    finally:
        db.commit()
        db.close()
        return wish_list


#function to get products from the table 'seller'
def get_products_of_seller(email):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT p.name, p.price, p.rating, p.warranty, p.type, p.deliveryCharges FROM seller s, product p  where s.email = %s AND p.seller=s.id'
        args = email
        cur.execute(query, args)
        products = cur.fetchone()
        if (len)(products) < 1:
            products = None
        print(products)
        print("Record obtained from the table 'product'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from product table")
    finally:
        db.commit()
        db.close()
        return products

#Function to get cart items
def get_cart_items(email):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT p.id, p.name, p.price, i.quantity from product p, cart c, cartitems i, buyer b where b.email=%s c.buyerId=b.id and i.cartNo=c.cartNowhere email = %s AND p.seller=s.id'
        args = email
        cur.execute(query, args)
        products = cur.fetchone()
        if (len)(products) < 1:
            products = None
        print(products)
        print("Record obtained from the table 'product'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from product table")
    finally:
        db.commit()
        db.close()
        return products

#Function to get data from the table 'seller'
def get_seller_data(email):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT * FROM seller where email = %s'
        args = email
        cur.execute(query, args)
        data = cur.fetchone()
        if (len)(data) < 1:
            data = None
        print(data)
        print("Record obtained from the table 'seller' ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table")
    finally:
        db.close()
        return "seller", data



# Function to get all the products(id, name, price) from the table 'product'
def get_all_products():
    print('get_product()')
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id, name, price FROM product'
        cur.execute(query)
        data = cur.fetchall()
        if (len)(data) < 1:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price':  temp[2]})
            data = return_data
            print("Record obtained from the table 'product' ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table")
    finally:
        db.close()
        return data


# FUNCTION to get only 4 products from the table 'product'
def get_4_products():
    print('get_4_products()')
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id, name, price FROM product LIMIT 4'
        cur.execute(query)
        data = cur.fetchall()
        if (len)(data) < 1:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2]})
            data = return_data
            print("Record obtained from the table 'product' (only 4 for the time being) ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table")
    finally:
        db.close()
        return data


#FUNCTION to get data in the price range from the table 'product'
def get_products_in_range(lower, upper):
    print('get_products_in_range()')
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id, name, price FROM product WHERE price >= %s and price <= %s LIMIT 10'
        args = (lower, upper)
        cur.execute(query, args)
        data = cur.fetchall()
        if (len)(data) < 1:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2]})
            data = return_data
            print("Record obtained from the table 'product' in the price range ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table")
    finally:
        db.close()
        return data


# FUNCTION to get products from searching by 'name' from the table 'product'
def get_product_by_name(name):
    print('get_products_by_name(name)')
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id, name, price FROM product WHERE name = %s'
        args = (name)
        cur.execute(query, args)
        data = cur.fetchall()
        if (len)(data) < 1:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2]})
            data = return_data
            print("Record obtained from the table 'product' by name of product ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table")
    finally:
        db.close()
        return data


## FUNCTIONS TO GET USER DATA EEENNNDDD HEEERREEEE ####
##################################################################################################################################







#### FUNCTIONS TO CHECK EMAILS AND STUFF START HEREEEEEEEEE ###############################
################################################################################################################################

# Function to check if email exists in buyer
def isEmailExists_in_buyer(email):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        print("DATABASE IS CONNECTED")
        cursor = db.cursor()
        query = "SELECT email FROM buyer where email = %s"
        arg = (email)
        cursor.execute(query, arg)
        emails = cursor.fetchone()
        print(len(emails))
        print(emails[0])
        if email == emails[0]:
            return True
        else:
            return False
    except Exception as e:
        print("ERROR DB is not connected")
    finally:
        if db!=None:
            db.commit()
            db.close()

# Function to check if email exists in seller
def isEmailExists_in_seller(email):
    print("isEmailExists_in_seller")
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        print("DATABASE IS CONNECTED in isEmailExists_in_seller")
        cursor = db.cursor()
        query = "SELECT email FROM seller where email = %s"
        arg = (email)
        cursor.execute(query, arg)
        print("isEmailExists_in_seller execute query")
        emails = cursor.fetchone()
        print(emails)
        #print(emails[0])
        if emails:
            #email == emails[0]:
            return True
        else:
            return False
    except Exception as e:
        print("ERROR DB is not connected")
    finally:
        if db!=None:
            db.close()


# Function to check if password exists in 'buyer'
def isPasswordCorrect_in_buyer(email, password):
    if isEmailExists_in_buyer(email):
        try:
            db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
            print("DATABASE IS CONNECTED")
            cursor = db.cursor()
            query = "SELECT password FROM buyer WHERE email = %s"
            args = (email)
            cursor.execute(query, args)
            passWord = cursor.fetchone()
            print(passWord[0])
            if password == passWord[0]:
                print("password found in buyer")
                return True
            else:
                print("pass not found in buyer")
                return False
        except Exception as e:
            print("ERRORRRR DB not connected in get password for buyer")
        finally:
            if db != None:
                db.close()
                return True


# Function to check if password exists in 'seller'
def isPasswordCorrect_in_seller(email, password):
    if isEmailExists_in_seller(email):
        try:
            db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
            print("DATABASE IS CONNECTED")
            cursor = db.cursor()
            query = "SELECT password FROM seller WHERE email = %s"
            args = (email)
            cursor.execute(query, args)
            passWord = cursor.fetchone()
            print(passWord[0])
            if password == passWord[0]:
                print("password found in seller table")
                return True
            else:
                print("pass not found in seller table")
                return False
        except Exception as e:
            print("ERRORRRR DB could not be connected in get password for seller")
        finally:
            if db != None:
                db.close()
                return True



# FUNCTION to check if security question and both answer are correct#
def is_security_question_and_answer_correct(email, securityQuestion, answer):
    print('is_security_question_and_answer_correct(securityQuestion, answer)')
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        print("DATABASE IS CONNECTED")
        cursor = db.cursor()
        query = "SELECT securityQuestion, answer FROM buyer WHERE email = %s"
        args = (email)
        cursor.execute(query, args)
        securityQuestion_answer = cursor.fetchone()
        print(securityQuestion_answer)
        if securityQuestion_answer[0] == securityQuestion and securityQuestion_answer[1] == answer:
            return True
        else:
            return False
    except Exception as e:
        print("ERRORRRR DB not connected in get password for buyer")
    finally:
        if db != None:
            db.close()


## FUNCTIONS TO CHECKS EMAILS AND STUFF EENNNDDDD Heeerrreeee #######
#################################################################################################################################

