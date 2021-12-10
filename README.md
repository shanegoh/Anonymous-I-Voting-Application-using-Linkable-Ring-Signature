# FYP-21-S4-09
Before Everything, make sure you downloaded your npm and node.js:
	NodeJs & NPM -> https://nodejs.org/en/

	Installation(Flask, Web3, virtualenv)
	https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/
	Change directory to backend, run the command below:
	-> pip install virtualenv
	-> pip install Flask
	-> pip install Flask-Web3
	-> pip install -r requirements.txt
	
	To Operate the system:
	(Front End)
	Change Directory to frontend folder(Separate command prompt)
	-> yarn install
	-> npm start
	
	(Back End)
	Change Directory to backend folder(Separate command prompt)
	-> virtualenv virtualEnv
	-> virtualEnv/Scripts/activate
	-> set FLASK_APP=flaskapp
	-> set FLASK_ENV=development
	-> flask run
	
	(Blockchain RPC)
	To start blockchain -> ganache-cli(Separate command prompt)
	OR
	Run your own Ganache interface
	
	
	Front-End
	client folder will be all the front end display
	@ client folder -> yarn upgrade
	
	
	Note:
	The folder name 'smartContract' consist of ReactJs front end which is named 'client'
	The smart contract solidity code is not yet implemented.

