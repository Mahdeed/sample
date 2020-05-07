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
    try:
        if isEmailExists_in_seller(email):
            return None
        else:
            db = sql.connect(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
            cursor = db.cursor()
            print("DATABASE IS CONNECTED")
            query = "INSERT INTO buyer(name, password, email, phoneNumber, address, securityQuestion, answer)VALUES(%s, %s, %s, %s, %s, %s, %s)"
            args = (name, password, email, phoneNumber, address, securityQuestion, answer)
            cursor.execute(query, args)
            print("Record inserted into the table 'buyer' ")
    except Exception as e:
        print("Error DB could not be connected")
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

#### FUNCTIONS TO 'INSERT' INTO DB "ENDDD" HEREEEE ####
#################################################################################################################################







#### FUNCTIONS TO GETT USEERRRR DATA STARTTT HEREEE ######
#################################################################################################################################

#Function to get data from the table 'buyer'
def get_buyer_data(email):
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
        print(data)
        print("Record obtained from the table 'buyer' ")
    except Exception as e:
        print("Error DB could not be connected")
    finally:
        db.commit()
        db.close()
        return "buyer", data


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
        db.commit()
        db.close()
        return "seller", data


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
    try:
        db = sql.connect(DATABASEIP, DB_USER, DB_PASSWORD, DATABASE)
        print("DATABASE IS CONNECTED")
        cursor = db.cursor()
        query = "SELECT email FROM seller where email = %s"
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
                db.commit()
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
                db.commit()
                db.close()
                return True






## FUNCTIONS TO CHECKS EMAILS AND STUFF EENNNDDDD Heeerrreeee #######
#################################################################################################################################
