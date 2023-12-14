# Chat App

Chat App is an python based client-server application where user can interact with each other.

Server will be listening for 3 type of message from user, `Join`, `Exit`, `Normal` message.
Each message will be relyed to all the other client connected to server at that moment.
Each user registers to server to start sending messaged on the platfrom.
All user connected to platfrom will get notification when new user joins or existing user exists platfrom.

## Dependencies

All the dependencies required to run this project are available in the [requirements.txt](https://github.com/chetna-ravat/chat-app/blob/main/requirements.txt) file.

## How to run the project

#### Create virtual environment
```shell
python3 -m venv env
```

#### Activate virtual environment
```shell
source env/bin/activate
```

#### Install required python dependencies from requirements file
```shell
pip install -r requirements.txt
```

### Start chat application

#### Start server
```shell
python3 server.py
```

#### Start client
```shell
python3 client.py
```
