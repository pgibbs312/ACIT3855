import mysql.connector 

 
db_conn = mysql.connector.connect(host="localhost", user="root", 
password="Pg000001", database="game") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
                  DROP TABLE game_score, users 
                  ''') 
 
db_conn.commit() 
db_conn.close() 