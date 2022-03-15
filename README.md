# I-Voting Application Using Linkable Ring Signature

## Summary
Mimi is an online web-based internet voting platform implemented as a software as a service application that 
provides government officials to run elections and allows authorized participants to vote. 
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
This application is integrated with Auth0 Services and thus required to run this application. Auth0 is used for authentication and authorization for this application. Configurations includes setting up API keys, CORS settings, connection to database and many more.
You can view the working product here at https://mimis.social -> Valid till 20th March 2022.




#### Contact
For more information or assistance, you can reach me on [LinkedIn](https://www.linkedin.com/in/wenhangoh/).
