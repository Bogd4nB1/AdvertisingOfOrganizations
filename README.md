Сайт для размещения услуг компаний разного вида деятельности. Реализован функционал CRUD. 
Стэк: Python, Html&Css, JS, Django, SQLite
Действия для запуска в CMD:
1. mkdir Org
2. cd Org
3. git clone git@github.com:Bogd4nB1/AdvertisingOfOrganizations.git
4. python -m venv venv
5. venv\Scripts\activate
6. cd AdvertisingOfOrganizations
7. pip install -r requirements.txt
8. python manage.py makemigrations
9. python manage.py migrate
10. python manage.py createsuperuser
11. python manage.py runserver
