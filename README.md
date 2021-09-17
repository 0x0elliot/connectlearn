# Open Source EdTech Student-Teacher Project
<p>
    This project exists to make it easier for students and teachers to connect.
</p>

![image](https://user-images.githubusercontent.com/60684641/132923014-5a2ca4a1-e99f-46bd-b8cd-07adaa123653.png)

### How to deploy (For now)

- <code>python3 connectlearn/mainwebapp/create_db.test.py</code> This will create the database file.
- Close create_db.test.py and then run <code>python3 connectlearn/mainwebapp/app.py</code> (I will write a Dockerfile and automate this as soon as possible!)

### Features:

- <b>Change .env file in mainwebapp folder to include your SMTP server details.</b>
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