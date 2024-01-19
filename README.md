start server: uvicorn app.main:app --reload

uvicorn app.main:app --host 127.0.0.1 --port 1010

pip install -r requirements.txt

pip3 freeze > requirements.txt  # Python3
pip freeze > requirements.txt  # Python2