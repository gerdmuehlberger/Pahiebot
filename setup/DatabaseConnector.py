import mysql.connector
from mysql.connector import errorcode


class DatabaseConnector:


    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database





    #############################################
    ### CREATE NEW USER IN SPECIFIED DATABASE ###
    #############################################
    def insert_user(self, user_id):
        query = "INSERT INTO users VALUES (%s)"
        args = (user_id,)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor()
            cursor.execute(query, args)
            databaseConnectionObject.commit()
            cursor.close()
            databaseConnectionObject.close()

        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Could not connect to Database. Invalid user credentials.")

            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Could not connect to Database. Database does not exist")

            else:
                print(f"Could not execute \"insert_user\" function. Error: {e}")





    #################################################
    ### FIND SPECIFIED USER IN SPECIFIED DATABASE ###
    #################################################
    def find_user(self, user_id):
        query = "SELECT * FROM users WHERE uid=%s"
        args = (user_id,)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            if len(rows) > 0:
                # if user already exists in db return False
                return True
            else:
                # if user does not exist in db return False
                return False

        except Exception as e:
            print(f"Could not execute \"find_user\" function. Error: {e}")





    ###############################################################
    ### ADD A FAVOURITED SOUNDFILE TO THE USER_SOUNDFILES TABLE ###
    ###############################################################
    #
    # Note: the argument "incrementor" serves as a counter for how many fields the user has already stored in his favourites.
    #
    def insert_user_soundfile(self, user_id, soundfile_id, soundkeyword, incrementor):

        query = "INSERT INTO user_soundfiles VALUES (%s, %s, %s, %s)"
        args = (user_id, soundfile_id, soundkeyword, incrementor)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor()
            cursor.execute(query, args)
            databaseConnectionObject.commit()
            cursor.close()
            databaseConnectionObject.close()

        except Exception as e:
            print(f"Could not execute \"insert_user_soundfile\" function. Error: {e}")





    ##################################################################
    ### DELETE A FAVOURITED SOUNDFILE TO THE USER_SOUNDFILES TABLE ###
    ##################################################################
    def delete_user_soundfile(self, user_id, soundkeyword):
        query = "DELETE FROM user_soundfiles WHERE user_id=%s AND soundkeyword=%s"
        args = (user_id, soundkeyword)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor()
            cursor.execute(query, args)
            databaseConnectionObject.commit()
            cursor.close()
            databaseConnectionObject.close()

        except Exception as e:
            print(f"Could not execute \"delete_user_soundfile\" function. Error: {e}")





    ######################################################
    ### FIND SPECIFIED SOUNDFILE IN SPECIFIED DATABASE ###
    ######################################################
    def find_soundfile(self, soundfilename):
        query = "SELECT * FROM soundfiles WHERE file_name=%s"
        args = (soundfilename,)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            if len(rows) > 0:
                # if soundfile exists in db return True
                return True
            else:
                # if user does not exist in db return False
                return False

        except Exception as e:
            print(f"Could not execute \"find_soundfile\" function. Error: {e}")





    ###################################################################
    ### RETURN ID OF SPECIFIED SOUNDFILE NAME IN SPECIFIED DATABASE ###
    ###################################################################
    def get_soundfile_id(self, soundfilename):
        query = "SELECT * FROM soundfiles WHERE file_name=%s"
        args = (soundfilename,)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            if len(rows) > 0:
                # if soundfile exists return its id
                soundfile_id = rows[0][0]

                return soundfile_id
            else:
                # if soundfile does not exist return -1 to indicate an error
                return -1

        except Exception as e:
            print(f"Could not execute \"get_soundfile_id\" function. Error: {e}")





    ################################################################
    ### RETURN AMOUNT OF AVAILABLE SOUNDFILES FOR SPECIFIED USER ###
    ################################################################
    def get_amount_of_user_soundfiles(self, user_id):
        query = "SELECT * FROM user_soundfiles WHERE user_id=%s"
        args = (user_id,)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            return len(rows)

        except Exception as e:
            print(f"Could not execute \"get_amount_of_user_soundfiles\" function. Error: {e}")





    ################################################
    ### CHECK IF KEYWORD ALREADY EXISTS FOR USER ###
    ################################################
    def find_keyword_for_user(self, user_id, hotkeyword):
        query = "SELECT * FROM user_soundfiles WHERE user_id=%s AND soundkeyword=%s"
        args = (user_id, hotkeyword)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            if len(rows) > 0:
                # if a keyword exists for a user return True
                return True
            else:
                # if the keyword does not exist return False
                return False

        except Exception as e:
            print(f"Could not execute \"find_keyword_for_user\" function. Error: {e}")





    ########################################
    ### RETRIEVE USER FAVOURITES FROM DB ###
    ########################################
    def find_favourites_for_user(self, user_id):
        query = 'SELECT user_soundfiles.soundkeyword, soundfiles.file_name, soundfiles.file_category FROM user_soundfiles INNER JOIN soundfiles ON user_soundfiles.soundfile_id = soundfiles.file_id WHERE user_soundfiles.user_id=%s;'
        args = (user_id,)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            return rows

        except Exception as e:
            print(f"Could not execute \"find_favourites_for_user\" function. Error: {e}")





    ##################################################
    ### RETRIEVE SOUNDFILE ASSOCIATED WITH KEYWORD ###
    ##################################################
    def get_soundfilename_associated_with_keyword(self, user_id, hotkeyword):
        query = 'SELECT soundfiles.file_name, soundfiles.file_category FROM user_soundfiles INNER JOIN soundfiles ON user_soundfiles.soundfile_id=soundfiles.file_id WHERE user_soundfiles.user_id=%s AND user_soundfiles.soundkeyword=%s;'
        args = (user_id, hotkeyword)

        try:
            databaseConnectionObject = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)
            cursor = databaseConnectionObject.cursor(buffered=True)
            cursor.execute(query, args)
            rows = cursor.fetchall()
            cursor.close()
            databaseConnectionObject.close()

            return rows

        except Exception as e:
            print(f"Could not execute \"get_soundfilename_associated_with_keyword\" function. Error: {e}")