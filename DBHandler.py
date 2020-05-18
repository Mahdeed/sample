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

# Function to insert info into the 'invoice' table
def insert_into_invoice(name, customerId, totalCost):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "INSERT INTO invoice(name, customerId, totalCost)VALUES(%s, %s, %s)"
        args = (name, customerId, totalCost)
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
def insert_into_product(name, price, warranty, type, deliveryCharges, seller):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "INSERT INTO product(name, price, warranty, type, deliveryCharges, seller)VALUES(%s, %s, %s, %s, %s, %s)"
        args = (name, price, warranty, type, deliveryCharges, seller)
        cursor.execute(query, args)
        print("Record inserted into the table 'product' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.commit()
        db.close()

# Generate New Cart No
def new_cart_no(buyerId):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "INSERT INTO cart(buyerId) VALUES(%s) "
        args = buyerId
        cursor.execute(query, args)
        print("New Cart NO is inserted")
    except Exception as e:
        print("New cart no" + str(e))
    finally:
        db.commit()
        db.close()

#Function to insert info into 'cart' table #
def insert_into_cart(buyerId, productId, quantity):
    try:
        cartNo = get_cart_no(buyerId)
        if cartNo == None:
            new_cart_no(buyerId)
            insert_into_cart(buyerId,productId,quantity)
        else:
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED")
            exist_quantity = get_product_quantity_in_cart(cartNo, productId)
            data = get_product_by_id(productId)
            if exist_quantity:
                if data:
                    if data[0]['quantity'] != exist_quantity:
                        increase_product_quantity_in_cart(cartNo, productId)
            else:
                query = "INSERT INTO cartItems(cartNo, productId, quantity) VALUES(%s,%s,%s) "
                args = (cartNo, productId, quantity)
                cursor.execute(query, args)
                print("Record inserted into the table 'cartItems' ")
    except Exception as e:
        print("Error DB could not be connected "+str(e))
    finally:
        db.commit()
        db.close()

#Function to insert into wish_list
def insert_into_wish_list(buyerId, productId):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "Insert into wish_list(buyerId, productId) VALUES(%s,%s)"
        args = (str(buyerId), str(productId))
        cursor.execute(query, args)
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.commit()
        db.close()

#function to increase product quantity
def increase_product_quantity_in_cart(cartNo, productId):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "UPDATE cartitems SET quantity = quantity+1 where cartNo=%s and productId=%s"
        args = (cartNo, productId)
        cursor.execute(query, args)
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.commit()
        db.close()

#Function to edit product from 'product' table
def edit_product(name, price, warranty, type, deliveryCharges, seller):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cursor = db.cursor()
        print("DATABASE IS CONNECTED")
        query = "UPDATE product SET name = %s, price = %s, warranty=%s, type=%s, deliveryCharges=%s where seller=%s"
        args = (name, price, warranty, type, deliveryCharges, seller)
        cursor.execute(query, args)
        print("Record updated in the table 'product' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.commit()
        db.close()

#Function to insert info into 'seller' table #
def insert_into_seller(name, address, email, phoneNumber, password, ranking, securityQuestion, answer):
    try:
        if isEmailExists_in_buyer(email):
            return None
        else:
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED")
            query = "INSERT INTO seller(name, address, email, phoneNumber, password, ranking, securityQuestion, answer)VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            args = (name, address, email, phoneNumber, password, ranking, securityQuestion, answer)
            cursor.execute(query, args)
            print("Record inserted into the table 'seller' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
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

##### FUNCTIONS TO REMOVE DATA FROM DB "START" HEREEE #######
#################################################################################################################################
#Function to remove roduct from cart
def remove_from_cart(buyerId, productId):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        cartNo=get_cart_no(buyerId)
        print("DATABASE IS CONNECTED")
        query = 'DELETE FROM cartitems where cartNo=%s and productId=%s'
        args = (cartNo,productId)
        cur.execute(query, args)
        print("Removed product from 'cartitems' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.commit()
        db.close()

#Function to remove from Wishlist
def remove_from_wishlist(buyerId, productId):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        cartNo=get_cart_no(buyerId)
        print("DATABASE IS CONNECTED")
        query = 'DELETE FROM wish_list where buyerId=%s and productId=%s'
        args = (buyerId,productId)
        cur.execute(query, args)
        print("Removed product from 'wish_list' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.commit()
        db.close()

def remove_from_cart_via_email(email):
    print("remove_from_card_via_email(email)")
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        query_for_buyer_ID = 'SELECT id FROM buyer WHERE email=%s'
        args_id = email
        buyer_id = cur.execute(query_for_buyer_ID, args_id)
        cartNo=get_cart_no(buyer_id)
        print("DATABASE IS CONNECTED")
        query = 'DELETE FROM cartitems where cartNo=%s'
        args = (cartNo)
        cur.execute(query, args)
        print("Removed product from 'cartitems' VIA 'EMAIL' ")
    except Exception as e:
        print("Error DB could not be connected" + str(e))
    finally:
        db.commit()
        db.close()

##### FUNCTIONS TO REMOVE DATA FROM DB "ENNNDDDDD" HEREEE #######
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
        if not data:
            data = None
        print("Record obtained from the table 'buyer' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.close()
        return "buyer", data

#Function to get seller id from table 'seller'
def get_seller_id(email):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id FROM seller where email = %s'
        args = email
        cur.execute(query, args)
        id = cur.fetchone()
        if not id:
            id = None
        print("id obtained from the table 'seller' ")
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.close()
        return id

#function to get product quantity from cart
def get_product_quantity_in_cart(cartNo, productId):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT quantity FROM cartitems where cartNo = %s and productId = %s'
        args = (cartNo, productId)
        cur.execute(query, args)
        quantity = cur.fetchone()
        if not quantity:
            quantity = None
        else:
            quantity=quantity[0]
        print("quantity obtained from the table 'cartItems' ")
        print(quantity)
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.close()
        return quantity
#Function to get buyer id from table 'buyer'
def get_buyer_id(email):
    try:
        db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id FROM buyer where email = %s'
        args = email
        cur.execute(query, args)
        id = cur.fetchone()
        if not id:
            id = None
        else:
            id=id[0]
        print("id obtained from the table 'buyer' ")
        print(id)
    except Exception as e:
        print("Error DB could not be connected"+str(e))
    finally:
        db.close()
        return id

#Function to get wishlist from the table 'buyer'
def get_wishlist(email):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        buyerId=get_buyer_id(email)
        query = 'SELECT p.name, p.price, p.rating, p.warranty, p.type, p.deliveryCharges, p.id FROM wish_list w, product p  where w.buyerId = %s AND p.id=w.productId'
        args = buyerId
        cur.execute(query, args)
        list = []
        products = cur.fetchall()
        if not products:
            products = None
        for p in products:
            list.append({'name': str(p[0]), 'price': p[1], 'rating': p[2], 'warranty': p[4], 'type': p[3],
                         'deliveryCharges': p[5],'id':str(p[6])})
        print(list)
        print("Record obtained from the table 'wish_list'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from wish_list table"+str(e))
    finally:
        db.commit()
        db.close()
        return list

#Function to get cartNo from 'buyer id'
def get_cart_no(buyerId):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT cartNo from cart where buyerId=%s'
        args = buyerId
        cur.execute(query, args)
        id = cur.fetchone()
        if id:
            id=id[0]
        else:
            id=None
        print("Record obtained from the table 'cart'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from cart table"+str(e))
    finally:
        db.commit()
        db.close()
        return id

#function to get products from the table 'seller'
def get_products_of_seller(email):
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT p.name, p.price, p.rating, p.warranty, p.type, p.deliveryCharges FROM seller s, product p  where s.email = %s AND p.seller=s.id'
        args = email
        cur.execute(query, args)
        products = cur.fetchall()
        if not products:
            products = None
        print(products)
        print("Record obtained from the table 'product'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from product table"+str(e))
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
        query = 'SELECT p.id, p.name, p.price, p.deliveryCharges, i.quantity from product p, cart c, cartitems i, buyer b where b.email=%s AND c.buyerId=b.id and i.cartNo=c.cartNo and p.id=i.productId'
        args = email
        cur.execute(query, args)
        list=[]
        products = cur.fetchall()
        if not products:
            products = None
        for p in products:
            product_max_quantity = get_product_by_id(p[0])
            list.append({'id':str(p[0]),'name': p[1],'price':p[2],'quantity':p[4],'charges':p[3], 'max_quantity': product_max_quantity[0]['quantity']})
        print(list)
        print("Record obtained from the table 'product'  ")
    except Exception as e:
        print("Error DB could not be connected in getting data from product table"+str(e))
    finally:
        db.commit()
        db.close()
        return list

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
        if not data:
            data = None
        print(data)
        print("Record obtained from the table 'seller' ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table"+str(e))
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
        if not data:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price':  temp[2]})
            data = return_data
            print("Record obtained from the table 'product' ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table"+str(e))
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
        query = 'SELECT id, name, price FROM product LIMIT 6'
        cur.execute(query)
        data = cur.fetchall()
        if not data:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2]})
            data = return_data
            print("Record obtained from the table 'product' (only 4 for the time being) ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table"+str(e))
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
        if not data:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2]})
            data = return_data
            print("Record obtained from the table 'product' in the price range ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table"+str(e))
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
        if not data:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2]})
            data = return_data
            print("Record obtained from the table 'product' by name of product ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table"+str(e))
    finally:
        db.close()
        return data


# FUNCTION to get products from searching by 'id' from the table 'product'
def get_product_by_id(id):
    print('get_products_by_id(id)')
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        cur = db.cursor()
        print("DATABASE IS CONNECTED")
        query = 'SELECT id, name, price, deliveryCharges, quantity FROM product WHERE id = %s'
        args = (id)
        cur.execute(query, args)
        data = cur.fetchall()
        if not data:
            data = None
        else:
            return_data = []
            for temp in data:
                return_data.append({'id': str(temp[0]), 'name': temp[1], 'price': temp[2], 'charges': temp[3], 'quantity': temp[4]})
            data = return_data
            print("Record obtained from the table 'product' by name of product ")
    except Exception as e:
        print("Error DB could not be connected in getting data from seller table"+str(e))
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
        if emails:
            emails=emails[0]
        else:
            emails=None
        print(emails)
        if email == emails:
            return True
        else:
            return False
    except Exception as e:
        print("ERROR DB is not connected"+str(e))
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
        print("ERROR DB is not connected"+str(e))
    finally:
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
            if passWord:
                passWord=passWord[0]
            else:
                passWord=None
            print(passWord)
            if password == passWord:
                print("password found in buyer")
                return True
            else:
                print("pass not found in buyer")
                return False
        except Exception as e:
            print("ERRORRRR DB not connected in get password for buyer"+str(e))
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
            if passWord:
                passWord=passWord[0]
            else:
                passWord=None
            if password == passWord:
                print("password found in seller table")
                return True
            else:
                print("pass not found in seller table")
                return False
        except Exception as e:
            print("ERRORRRR DB could not be connected in get password for seller"+str(e))
        finally:
            if db != None:
                db.close()
                return True



# FUNCTION to check if security question and both answer are correct in buyer table#
def is_security_question_and_answer_correct_in_buyer(email, securityQuestion, answer):
    print('is_security_question_and_answer_correct(securityQuestion, answer in buyer)')
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
        print("ERRORRRR DB not connected in get password for buyer"+str(e))
    finally:
        if db != None:
            db.close()

# FUNCTION to check if security question and both answer are correct in seller table#
def is_security_question_and_answer_correct_in_seller(email, securityQuestion, answer):
    print('is_security_question_and_answer_correct(securityQuestion, answer in seller)')
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        print("DATABASE IS CONNECTED")
        cursor = db.cursor()
        query = "SELECT securityQuestion, answer FROM seller WHERE email = %s"
        args = (email)
        cursor.execute(query, args)
        securityQuestion_answer = cursor.fetchone()
        print(securityQuestion_answer)
        if securityQuestion_answer[0] == securityQuestion and securityQuestion_answer[1] == answer:
            return True
        else:
            return False
    except Exception as e:
        print("ERRORRRR DB not connected in get password for seller"+str(e))
    finally:
        if db != None:
            db.close()

## FUNCTIONS TO CHECKS EMAILS AND STUFF EENNNDDDD Heeerrreeee #######
#################################################################################################################################

