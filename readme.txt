Setting up the system
=====================

some details to the Django deployment documentation https://docs.djangoproject.com/en/2.2/howto/deployment/
the system was developed with Django 2.2.1

1. clone the Github repository https://github.com/cbernscherer/OeBVServices
2. Install python 3.7
3. Create a virtual environment with python 3.7 And activate it
4. Change to the directory where you cloned the repository
5. list the directory. You need to change to the directory where requirements.txt is located
6. pip install -r requirements.txt will install all needed packages
7. Create a database
8. In the Django Admin interface generate three groups, OeBVAdmins, ClubAdmins and Players

All components are open source, so don't rely on backward compatibility.
The versions can be found in requirements.txt