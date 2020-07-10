# DevOps Take Home Interview

Hello and thank you for interviewing with Firefly!

## What you'll be doing

This repository contains the code for two Flask web apps which power a simple appointment booking service.

Each of the web apps live in subdiretories of this repository:

- The `engine` subdirectory is a CRUD app which manages appointments and exposes an RPC API
- The `webserver` subdirectory is a front-end web app which communicates with the `engine` app

For this interview, we'd like you to setup two servers, using the tech stack of your choice, to get our appointment booking service up and running.

## A few things we'd like to see

1) The web apps should be containerized
2) The web apps should be hosted independently of eachother
3) The server running the `engine` app should not be publicly accessible; only the server running the `webserver` app should be able to reach it

## Tips

You should not have to make any changes to the web apps themselves, but a skim through server.py at the root of each app will be helpful.

To run the servers locally:

```
pip3 install -r requirements.txt
python3 server.py
```

## Resources

- [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
