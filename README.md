# I-Voting Application Using Linkable Ring Signature

## Summary
Mimi is an online web-based internet voting platform implemented as a software as a service application that 
provides Singapore Government officials to run elections and allows authorized participants to vote. 
It is designed using the Linkable Ring Signature protocol.


## Instructions
1. **Make sure you have downloaded your npm and node.js(v16.13.1)**

2. NodeJs & NPM from https://nodejs.org/en/

3. **Make sure you installed pip and python version is 3.10.0.**
  >As for the error occured when installing python requirements, install visual studio, select Desktop development with C++.


### Installation for frontend
**Change Directory to frontend folder in a separate command prompt/terminal. Run the command:**
```
yarn install or npm install
```

### Installation for backend
**Change Directory to backend folder in separate command prompt/terminal. Then, run the commands:**
```
pip install virtualenv
pip install Flask
pip install -r requirements.txt
virtualenv virtualEnv
virtualEnv/Scripts/activate ( for windows )
source virtualEnv/bin/activate ( for linux )
```

### Start Local Server
**To start the frontend server, run the command:**
```
npm start
```
**To start backend server, run the commands:**
```
set FLASK_APP=flaskapp
set FLASK_ENV=development
flask run
```


### Warning!
This application is integrated with Auth0 Services for authentication and authorization thus required to function together with the application. Configurations includes setting up virtual environment server, python virtual environment, connection to database, security and many more.
You can view the working product here at https://mimis.social -> Valid till 20th March 2022.

### Contact
For more information or assistance, feel free to reach me on [LinkedIn](https://www.linkedin.com/in/wenhangoh/).

### Disclaimer
This is a Final Year Project in University of Wollongong. Duration: 09/21 - 03/22.
