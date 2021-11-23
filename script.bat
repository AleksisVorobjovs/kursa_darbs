@echo off
python config_test.py
python migrate_db.py
python main.py
