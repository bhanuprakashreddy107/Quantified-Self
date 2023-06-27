In order to run the project ,

Open a terminal or VScode(preferred) and go to base directory of the folder.
Using cd [folder name].

Install and enable virtual environment.

Now run command "pip install -r requirements.txt" on your terminal which will install all the requirements needed to run the project

Then Run "npm install" to install node modules.

"Whenever you're opening a new terminal  , Don't forget to directory to base directory of the folder.

Now Take a new terminal and run the command "python3 main.py".

Now take another terminal and run the command "npm run dev".

In order to run redis ,run the command : "redis-server" in a new terminal.

In order to run celery workers,
Run these commands in two different terminals:

"celery -A main.celery worker -l info"

"celery -A main.celery beat --max-interval 1 -l info".


Now Open link "http://localhost:5173" in a browser to see the website.
