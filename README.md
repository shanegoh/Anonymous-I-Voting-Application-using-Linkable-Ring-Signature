# I-Voting Application Using Linkable Ring Signature
## The instructions below are for localhost.
### Make sure you have downloaded your npm and node.js(v16.13.1):
	NodeJs & NPM -> https://nodejs.org/en/
	Make sure you installed pip and python version is 3.10.0.
	As for the error occured when installing requirements, install visual studio, select Desktop development with C++
`
(Front End)
Change Directory to frontend folder(Separate command prompt)
Installation
yarn install or npm install
`
	
	Start front-end Server
	-> npm start
	
	
	(Back End) 
	Change Directory to backend folder(Separate command prompt)
	Installation
	-> pip install virtualenv
	-> pip install Flask
	-> pip install -r requirements.txt
	-> virtualenv virtualEnv
	-> virtualEnv/Scripts/activate ( for windows )
	-> source virtualEnv/bin/activate ( for linux )
	
	
	Start back-end Server
	-> set FLASK_APP=flaskapp
	-> set FLASK_ENV=development
	-> flask run

	Warning!
	This application is integrated with Auth0 Services. Auth0 provides 22 days of free trial.
	https://mimis.social is valid till 20th March 2022.
