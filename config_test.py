import os
import mysql.connector
import sys

from datetime import datetime
from configparser import ConfigParser

print("Configuration file test")

# Testing if configuration file exists on disk in the current working directory
print("----------")
print("Checking if config file exists -->")
assert os.path.isfile("config.ini") == True
print("OK")
print("----------")

# Opening the configuration file
config = ConfigParser()
config.read('config.ini')

# Checking if all color related config options are present in the config file
print("Checking if config has NASA related options -->")
assert config.has_option('Color', 'bg') == True
assert config.has_option('Color', 'head') == True
assert config.has_option('Color', 'food') == True
assert config.has_option('Color', 'score') == True
assert config.has_option('Color', 'trail') == True
print("OK")
print("----------")

# Checking if all MYSQL related config options are present in the config file
print("Checking if config has MYSQL related options -->")
assert config.has_option('DB', 'host') == True
assert config.has_option('DB', 'db') == True
assert config.has_option('DB', 'user') == True
assert config.has_option('DB', 'password') == True
print("OK")
print("----------")

# Checking if possible to connect to nasa with the existing config options
print("Checking if colors are real with the given config options -->")
background = config.get('Color', 'bg')
head = config.get('Color', 'head')
food = config.get('Color', 'food')
score = config.get('Color', 'score')
trail = config.get('Color', 'trail')
colors = [background, head, food, score, trail]
for i in colors:
    rgb=i.split(",")
    for j in rgb:
        if(int(j)>=0 and int(j)<=255):
            continue
        else:
            print("Color doesn't exist make sure rgb value is >=0 and <=255")
            sys.exit()
print("OK")
print("----------")
# Checking if possible to connect to MySQL with the existing config options
print("Checking if it is possible to connect to MYSQL with the given config options -->")
mysql_config_mysql_host = config.get('DB', 'host')
mysql_config_mysql_db = config.get('DB', 'db')
mysql_config_mysql_user = config.get('DB', 'user')
mysql_config_mysql_pass = config.get('DB', 'password')
connection = mysql.connector.connect(host=mysql_config_mysql_host, database=mysql_config_mysql_db, user=mysql_config_mysql_user, password=mysql_config_mysql_pass)
assert connection.is_connected() == True
print("OK")
print("----------")

# Checking if log config files exist for log config
print("Checking if DB migration component log config file exists log_db.yaml -->")
assert os.path.isfile("log_db.yaml") == True
print("OK")
print("----------")
print("Checking if asteroid worker component log config file exists log_c.yaml -->")
assert os.path.isfile("log_c.yaml") == True
print("OK")
print("----------")
print("Checking if log destination directory exists -->")
assert os.path.isdir("logs") == True
print("OK")
print("----------")
print("Checking if migration source directory exists -->")
assert os.path.isdir("migrations") == True
print("OK")
print("----------")
print("Configuration file test DONE -> ALL OK")
print("----------------------------------------")