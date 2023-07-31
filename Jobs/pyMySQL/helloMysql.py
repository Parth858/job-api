import uuid
import mysql.connector
from mysql.connector import errorcode

class MySQL:

    def __init__(self, username="hi-man", password="p4rk.r0n1n", database=None):
        self.user = username
        self.password = password
        self.host = "127.0.0.1"
        self.database = database if database else None
        self.connected = False
        self.tables = {}

        ## Connect with mysql using connect() constructor
        # Implementation of command `mysql -u username -p "databasename"`
        try:
            self.mysql = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cursor = self.mysql.cursor()
        except mysql.connector.Error as err:
            print(err)
            exit(1)
        
        # Connect with the database
        try:
            self.mysql.database = self.database
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Something went Wrong! Access denied")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Wrong database information provided! Database={self.database}")
            choice = input("Do you want to created a new database named {} [Y/N]".format(self.database))
            if choice.lower() == 'y':
                self._create_database()
            else:
                print("No DB in use currently")
            
    def _create_database(self):
        if not self.database:
            raise Exception("Database information not provided")
        try:
            self.cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.database))
            print("Database has been created!")
            self.connected = True
            self._use_database()
        except mysql.connector.Error as err:
            print(err)
            exit(1)

    def _use_database(self):
        if not (self.connected or self.database):
            print("Database not connected yet")
            return
        self.cursor.execute(f"USE {self.database}")


    def create(self):
        """This method creates tables
        job and user, as created by parth
        """
        self.tables["Jobapp_company"] = (
            "CREATE TABLE IF NOT EXISTS Jobapp_company ("
                "company_id VARCHAR(36) PRIMARY KEY,"
                "name VARCHAR(50) NOT NULL,"
                "location TEXT(255) NOT NULL,"
                "about TEXT(500) DEFAULT 'None'"
            ")"
        )
        self.tables['Jobapp_job'] = (
            "CREATE TABLE IF NOT EXISTS Jobapp_job ("
                "job_id VARCHAR(36) PRIMARY KEY,"
                "job_role VARCHAR(50) NOT NULL,"
                "company_id VARCHAR(36) NOT NULL,"
                "description TEXT DEFAULT 'None',"
                "location TEXT(200) DEFAULT 'None',"
                "post_date DATE NOT NULL,"
                "posted BOOLEAN NOT NULL,"
                "experience INTEGER NOT NULL,"
                "created_at TIMESTAMP DEFAULT current_timestamp(),"
                "updated_at TIMESTAMP DEFAULT current_timestamp() ON UPDATE current_timestamp(),"
                "INDEX index_Jobapp_company (company_id),"
                "FOREIGN KEY (company_id)"
                "REFERENCES Jobapp_company(company_id)"
                "ON DELETE CASCADE"
            ")"
        )
        self.tables['Jobapp_user'] = (
            "CREATE TABLE IF NOT EXISTS Jobapp_user ("
                "user_id VARCHAR(36) NOT NULL PRIMARY KEY,"
                "name VARCHAR(30) DEFAULT 'None',"
                "email VARCHAR(30) DEFAULT 'None',"
                "address TEXT(200) DEFAULT 'None',"
                "phone VARCHAR(15) DEFAULT 'None',"
                "about TEXT DEFAULT 'None',"
                "resume VARCHAR(100) DEFAULT 'None',"
                "profile_picture VARCHAR(100) DEFAULT 'None',"
                "job_id VARCHAR(36) NOT NULL,"
                "company_id VARCHAR(36) NOT NULL,"
                "FOREIGN KEY (job_id)"
                "REFERENCES Jobapp_job(job_id)"
                "ON DELETE CASCADE,"
                "FOREIGN KEY (company_id)"
                "REFERENCES Jobapp_company(company_id)"
                "ON DELETE CASCADE"
            ")"
        )

        # run the create table commands
        for tablename, tabledescription in self.tables.items():
            try:
                self.cursor.execute(tabledescription)
                print(f"Table '{tablename}' has been created successfully")
            except Exception as err:
                raise Exception(err)
    
    def insert(self):
        """
        Syntax: 
        insert into <tablename> (columnN, ...)
        VALUES(val1, val2...)
        """
        insert_query = (
            "INSERT INTO Jobapp_company (company_id, location, about, name)"
            "VALUES (%s, %s, %s, %s)"
        )

        values = (
            f"{uuid.uuid4()}",
            "Null community",
            "Pune",
            "We are just a community"
        )

        try:
            self.cursor.execute(insert_query, values)
        except Exception as err:
            raise Exception(err)
        else:
            self.mysql.commit() # This commit the data into the database
        