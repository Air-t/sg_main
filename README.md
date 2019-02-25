# Exam app to create and evaluate exam sheets

Web application allows for creating and managing user accounts for students and 
owner(s). Based on user group participation - relevant API is accessible.

### Role owner
Owner can maker CRUD operations on exam sheets. Owner can evaluate students finished exam sheets and freely assign grades to questions within.

### Role student
Student should be able to participate in exam based on given permission. Only owner can grant permission to exams

 

## Installation

### Docker and Docker-compose
This application is ready to be deployed. Docker and Docker-compose scripts are prepared.
Docker-compose has two services within. Application build and postgresql server.
Please make sure that django setting.py database parameters are set properly.
There are no fixures provided, howewer the instance of owner will be created with project deployment.
This User will have granted permissions to access Exam section visible on navbar.

### Pure django
This application may be tested as django standalone application, however postgresql or any other database
service needs to be firstly set up. You can replace postgresql database with SQLight database to ease API testing.
Create owner instance:
```python
python manage.py create_owner <name> <password>
```

Setup virtual environment [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

Use at least Python 3.6.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all necessary libraries.

```bash
pip install -r requirements.txt
```


Look at input.csv and output.csv file to see how script handles data.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

Air-t
