from mysql.connector import connect

db = connect(
    host="192.168.15.68",
    user="mydolladmin",
    passwd="polentinho",
    port = "3306",
    database="mydoll"
)

cursor = db.cursor()

