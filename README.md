# ConnectLearn
<img height="36px" src="https://forthebadge.com/images/badges/made-with-python.svg">&nbsp;<img height = "36px" src = "https://forthebadge.com/images/badges/open-source.svg">&nbsp;<img height="26px" src="https://img.shields.io/badge/For-Teachers%20And%20Students-red.svg">

<p>
    ConnectLearn is an easy to use and deploy Open-Source Project meant to make it easier for the right students to find the right teachers online.
</p>

## Deploy

### With Docker

- <code>git clone https://github.com/0x0elliot/connectlearn/</code>
- <code>cd connectlearn/src </code> and definitely change <a href = "https://github.com/0x0elliot/connectlearn/blob/75044a17fe8d9dc9c84f7b24b0a68a9c101c3c05/src/app.py#L22">Secret key's</a> value to something random before putting it to production!
- Set up <code>src/.env</code> to add your SMTP email and Password.
- <code>sudo docker-compose up</code>
- Visit <a href = "http://0.0.0.0:8000/">0.0.0.0:8000</a> on your browser.

If you don't have docker and docker-compose installed, Try <a href = "https://docs.docker.com/engine/install/ubuntu/">Docker Installation</a> and <code>sudo apt install docker-compose</code>

### Build Locally

- Repeat the first three steps

```bash
$ pip3 install -r requirements.txt
$ export FLASK_APP=src
$ chmod +x ./src/init_db.sh
$ ./src/init_db.sh
$ chmod +x ./docker-entrypoint.sh
$ ./docker-entrypoint.sh
```
- Visit <a href = "http://0.0.0.0:8000/">0.0.0.0:8000</a> on your browser.

## Aim:

This project has reached a point where I need to define a proper aim for it. I have noticed that there might be a market for very niché genres and topics that people might want to connect teachers and students better in. I want this project to be a tool they can use for just that! We will try our best to move forward in such a direction that it is more easily customisable and flexible.

![image](https://user-images.githubusercontent.com/60684641/132923014-5a2ca4a1-e99f-46bd-b8cd-07adaa123653.png)

## Features:

- <b>Login/Register/Sign Out functionality</b>
![image](https://user-images.githubusercontent.com/60684641/132923245-ad4601c9-af0c-4ae4-bad5-e1f1e43339b9.png)

- <b>User Profile Management Along with Profile Picture Uploading Functionality For Teachers + Image Cropping</b>
![image](https://user-images.githubusercontent.com/60684641/132923312-db66b230-d96f-4d4e-a400-3561ef617516.png)

- <b>Main page where students can search for teachers accordingly and filter them by Cost, Language, Most Recent/Oldest, Username, Teacher Description etc.</b>
![image](https://user-images.githubusercontent.com/60684641/132923459-f5ad155d-23ea-48c3-8c22-2682544190a0.png)

- <b>Teacher profiles students can visit with a separate description for their profile that is different than the one that appears in listing page/search results.</b>
![image](https://user-images.githubusercontent.com/60684641/132923584-c8a59ac5-872d-4951-9496-0a265afea989.png)

- <b>Contact button using which the student's message is sent to the teacher through email. Only 1 button usage/User is allowed for the students. The student can check a box which also sends in their phone number in the email.</b>
![image](https://user-images.githubusercontent.com/60684641/132923674-7e47ac91-8278-42df-9480-0ea8bbf13dc8.png)
