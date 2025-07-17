# on aws server
first launch EC2 instance on aws
login into ec2 instance
create folder into ec2 instance mkdir project
cd project
git clone https://github.com/your-username/django-todo-app.git
cd django-todo-app

sudo apt update
sudo apt install python3-pip
# 1. Make sure python3-venv is installed
sudo apt install python3-venv -y

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Now install Django safely inside the venv
pip install django

# 5. Verify
django-admin --version

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
set inbound rule in aws ec2 instance to allow incoming traffic on port 8000
paste the ip address of ec2:8000 with http

nohup python manage.py runserver 0.0.0.0:8001 &
[1] 4699
nohup: ignoring input and appending output to 'nohup.out'

to stop the server
lsof -i:8000
kill pid of process running on port 8000

create docker file
install docker on ec2 instance
sudo apt  install docker.io


create Dockerfile

FROM python:3.11
RUN pip install django==3.2
COPY . . 
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

save it
sudo docker build . -t todo-app
sudo docker ps
sudo docker run -p 8001:8001 todo-app or id
sudo docker run -d -p 8001:8001 todo-app or id  #to run in background


# 📝 Django ToDo App

A simple and elegant web-based ToDo List application built using the Django framework. It allows users to create, mark as complete, and delete tasks.

---

## 🚀 Features

- Add new tasks
- Mark tasks as complete/incomplete
- Delete tasks
- Responsive layout using Bootstrap
- Modern UI with centered layout

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, FontAwesome
- **Database:** SQLite (default)

---

## ⚙️ Setup Instructions

Follow the steps below to run this project locally.

---

### 🔧 Prerequisites

- Python 3.7+ installed
- `pip` (Python package installer)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) *(optional but recommended)*

---

### 📦 Installation (Local Development)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/django-todo-app.git
cd django-todo-app

# 2. Create a virtual environment
python -m venv env

# 3. Activate the virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply database migrations
python manage.py migrate

# 6. Run the development server
python manage.py runserver
Open in your browser:
http://127.0.0.1:8000/

☁️ Deployment on AWS EC2
Step-by-step Guide:
# 1. Launch an EC2 instance (Ubuntu recommended)

# 2. SSH into the EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Create project directory
mkdir project
cd project

# 4. Clone the repository
git clone https://github.com/your-username/django-todo-app.git
cd django-todo-app

# 5. Update system packages
sudo apt update

# 6. Install pip and venv
sudo apt install python3-pip -y
sudo apt install python3-venv -y

# 7. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 8. Install Django inside the virtual environment
pip install django

# 9. Verify Django version
django-admin --version

# 10. Apply migrations
python manage.py migrate

# 11. Run Django server on public IP and port 8000
python manage.py runserver 0.0.0.0:8000
⚙️ Additional AWS Setup
Go to AWS EC2 Dashboard → Security Groups

Edit Inbound Rules to allow TCP traffic on port 8000

Access the app in browser using:

cpp
http://<your-ec2-public-ip>:8000/
🔄 To run server in background (production-style):
nohup python manage.py runserver 0.0.0.0:8001 &
This will:

Start server on port 8001

Output logs to nohup.out

Show background job ID like [1] 4699

🛑 To stop the server:
lsof -i:8000  # Find the PID of the process
kill <PID>    # Kill the process running on port 8000
🐳 Docker Deployment
1. Install Docker on EC2:
bash
Copy
Edit
sudo apt install docker.io -y
2. Create a Dockerfile in the project root:
dockerfile
FROM python:3.11

# Install Django
RUN pip install django==3.2

# Copy project files into container
COPY . .

# Run migrations
RUN python manage.py migrate

# Start server on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
3. Build Docker image:

sudo docker build . -t todo-app
4. Run the Docker container:

# Run in foreground
sudo docker run -p 8001:8001 todo-app

# OR run in background
sudo docker run -d -p 8001:8001 todo-app
5. Access the app:
Visit http://<your-ec2-public-ip>:8001/ in your browser.

📌 Notes
Ensure ports 8000 and 8001 are open in AWS Security Group

Use requirements.txt to manage dependencies (Django==3.2)

✅ To Do (Future Enhancements)
Add user authentication

Task due dates and reminders

Task categories and priorities

Docker Compose setup

## Install Jenkins
How to Install Jenkins on Ubuntu EC2
1. Connect to your EC2 instance
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
2. Update package index
sudo apt update
sudo apt upgrade -y
3. Install Java (Jenkins requires Java 17)
sudo apt install openjdk-17-jdk -y
Check Java version:
java -version

Make sure it outputs something like openjdk version "17.x"

4. Add Jenkins repository and key
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list

5. Update and install Jenkins
sudo apt update
sudo apt install jenkins -y
6. Start and enable Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins
Check Jenkins service status:
sudo systemctl status jenkins
7. Open port 8080 in your EC2 security group
Go to AWS EC2 Console → Security Groups → Select your instance’s security group.

Edit inbound rules.

Add a new rule:

Type: Custom TCP

Port range: 8080
Port range: 8001
Source: Anywhere (0.0.0.0/0) or your IP for security

8. Access Jenkins web interface
Open a browser and go to:
http://your-ec2-public-ip:8080
9. Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
Use this password to unlock Jenkins in the web UI.

sudo chown -R jenkins:jenkins /home/ubuntu/projects
sudo chmod -R 755 /home/ubuntu/projects
sudo mv /home/ubuntu/projects/python-django-devops_todo /var/lib/jenkins/workspace/
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
