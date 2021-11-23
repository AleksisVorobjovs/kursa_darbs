@echo off
IF exist logs ( echo logs exists ) ELSE ( mkdir logs && echo logs created)
python config_test.py
python migrate_db.py
python main.py
pause