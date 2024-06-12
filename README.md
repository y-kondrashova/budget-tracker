# budget-tracker

Django project for keeping track of expenses, income, and other
financial transactions in order to ensure that the budget is being
used efficiently and effectively

## Installation

```shell
git clone https://github.com/y-kondrashova/budget-tracker.git
cd budget-tracker
python3 -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Features

* Authentication functionality for User
* Managing budgets
* Managing transaction
* Managing transfers
