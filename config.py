import os

print("MYSQLHOST =", os.environ.get("MYSQLHOST"))
print("MYSQLPORT =", os.environ.get("MYSQLPORT"))
print("MYSQLUSER =", os.environ.get("MYSQLUSER"))
print("MYSQLDATABASE =", os.environ.get("MYSQLDATABASE"))

HOST = os.environ.get("MYSQLHOST")
USER = os.environ.get("MYSQLUSER")
PASSWORD = os.environ.get("MYSQLPASSWORD")
DATABASE = os.environ.get("MYSQLDATABASE")
DB_PORT = int(os.environ.get("MYSQLPORT", "3306"))