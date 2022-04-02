import mysql.connector

mydb = mysql.connector.connect(
    host="pg-acit3855-kafka.eastus.cloudapp.azure.com",
    user="root",
    password="Pg000001"
)

c = mydb.cursor()
c.execute("use game")
c.execute('''
        CREATE TABLE game_score (
            id INTEGER AUTO_INCREMENT,
            trans_id VARCHAR(250) NOT NULL,
            score_id INTEGER NOT NULL,
            date VARCHAR(250) NOT NULL,
            runTime VARCHAR(100) NOT NULL,
            score INTEGER NOT NULL,
            userName VARCHAR(100) NOT NULL,
            PRIMARY KEY (id))
        ''')
c.execute('''
    CREATE TABLE users(
        id INTEGER AUTO_INCREMENT,
        trans_id VARCHAR(250) NOT NULL,
        user_id INTEGER NOT NULL,
        email VARCHAR(100) NOT NULL,
        name VARCHAR(100) NOT NULL,
        password Varchar(100) NOT NULL,
        phoneNumber Varchar(250) NOT NULL,
        timeStamp VARCHAR(100) NOT NULL,
        PRIMARY KEY (id))
''')
mydb.commit()
mydb.close()