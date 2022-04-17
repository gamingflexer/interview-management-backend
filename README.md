# interview-management

Flask Backend
==================================

# SetUp and Run

## Fork, Clone and Remote

To run the project successfully, you need to create .**env** file using .envsample file

## Installation

After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt

## Running the Flask Server

Step 1: Change the current directory to Flask-backend
```sh
(venv) $ cd interview-management-backend
```

Step 2: Set up FLASK_APP
(For Linux or Mac)
```sh
(venv) $ `export FLASK_APP=api`
```

(For Windows)
```sh
(venv) $ `set FLASK_APP=api`
```

Step 3: Now, Upgrade the Migrated Database, using the following command
```sh
(venv) $ flask db upgrade
```

Step 4:Start the backend server
To run the server use the following command:
```sh
(venv) $ flask run
```


# API Endpoints List

```
Endpoint                   Methods       Rule
-------------------------  ------------  ---------------------------------------

```

**Note** : You can find the updated list of API endpoints using the following command
```sh
(venv) $ flask routes
```
