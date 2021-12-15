# FYP-21-S4-09
Before Everything, make sure you downloaded your npm and node.js(v16.13.1):
	NodeJs & NPM -> https://nodejs.org/en/
Make sure you installed pip and python version is 3.10.0

	https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

	(Front End)
	Change Directory to smartContract -> client folder(Separate command prompt)
	Installation
	-> yarn install
	
	Start front-end Server
	-> npm run start
	
	
	
	(Back End) 
	Change Directory to backend folder(Separate command prompt)
	Installation
	-> pip install virtualenv
	-> pip install Flask
	-> pip install Flask-Web3
	-> pip install -r requirements.txt
	-> virtualenv virtualEnv
	-> virtualEnv/Scripts/activate ( for windows )
	-> source virtualEnv/bin/activate ( for mac os )
	-> For other linux OS, please google online
	
	Start back-end Server
	-> set FLASK_APP=flaskapp
	-> set FLASK_ENV=development
	-> flask run
	
	(Blockchain RPC)
	To start blockchain -> ganache-cli(Separate command prompt)
	OR
	Run your own Ganache interface
	
	

	
	
	Note:
	The folder name 'smartContract' consist of ReactJs front end which is named 'client'
	The smart contract solidity code is not yet implemented.

