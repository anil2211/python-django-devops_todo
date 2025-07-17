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

# open port 8080
jenkins create node

cd /var/lib/jenkins/workspace/python-django-devops_todo
# Build Docker image
docker build -t todo-app1 .
# Run container on port 8080
docker run -d -p 8001:8001 --name todo-app-container1 todo-app1


# 🚀 Jenkins Setup and Docker-Based Deployment on Ubuntu EC2

This guide provides clear, step-by-step instructions to install Jenkins on an Ubuntu EC2 instance, configure it to run Docker-based builds, and deploy a Python/Django app using Jenkins.

---

## 🧰 Prerequisites

- AWS EC2 instance (Ubuntu 22.04 preferred)
- SSH access with `.pem` key
- Docker and Dockerfile in your project
- GitHub repo for your app (public or private)
- Basic understanding of terminal and Linux commands

---

## 🛠️ Step-by-Step Setup

### ✅ Step 1: Connect to Your EC2 Instance

```bash
ssh -i /path/to/your-key.pem ubuntu@your-ec2-public-ip
✅ Step 2: Update the System

sudo apt update
sudo apt upgrade -y
✅ Step 3: Install Java (Required for Jenkins)
sudo apt install openjdk-17-jdk -y
java -version
You should see something like:

openjdk version "17.x.x"
✅ Step 4: Add Jenkins Repository and Key

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | \
sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/ | \
sudo tee /etc/apt/sources.list.d/jenkins.list

✅ Step 5: Install Jenkins
sudo apt update
sudo apt install jenkins -y

✅ Step 6: Start and Enable Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins

✅ Step 7: Allow Jenkins Port in EC2 Security Group

Go to AWS Console → EC2 → Security Groups

Find the group attached to your instance

Click Edit Inbound Rules and add:

Type: Custom TCP

Port: 8080 (Jenkins)

Source: 0.0.0.0/0 (or restrict to your IP)

✅ Step 8: Access Jenkins in Browser
Open your browser:

http://your-ec2-public-ip:8080
✅ Step 9: Unlock Jenkins
On the Jenkins unlock screen, run this on your EC2 terminal:

sudo cat /var/lib/jenkins/secrets/initialAdminPassword
Copy the password into the web UI.

🐳 Docker + Jenkins Integration
✅ Step 10: Install Docker (if not already)
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
✅ Step 11: Give Jenkins Docker Access
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
Important: Reboot the instance after this to apply group changes:
sudo reboot
📦 Project Deployment via Jenkins
✅ Step 12: Prepare Your Project
Assuming your project is cloned to:
/home/ubuntu/projects/python-django-devops_todo/
Make sure the Dockerfile is in the root.

Change ownership and permissions:

sudo chown -R jenkins:jenkins /home/ubuntu/projects
sudo chmod -R 755 /home/ubuntu/projects
Move project into Jenkins workspace (optional but simplifies access):

sudo mv /home/ubuntu/projects/python-django-devops_todo /var/lib/jenkins/workspace/
✅ Step 13: Create a Jenkins Job
Open Jenkins Dashboard → New Item

Choose Freestyle Project

Name it: Todo-dev

Under Source Code Management, connect your GitHub repo (if desired)

In Build section, choose Execute Shell

Use this script:

#!/bin/bash
set -xe

cd /var/lib/jenkins/workspace/python-django-devops_todo

# Build Docker image
docker build -t todo-app .

# Stop and remove existing container (optional safety step)
docker rm -f todo-app-container || true

# Run Docker container
docker run -d -p 8001:8001 --name todo-app-container todo-app
✅ Port Reference
Port	Purpose
8080	Jenkins
8001	Django App


Make sure both ports are opened in your EC2 security group.

🎉 Final Test
Visit your deployed Django app at:
http://your-ec2-public-ip:8001

🧹 Optional: Clean Docker Resources
To remove old containers/images if needed:
docker ps -a           # list all containers
docker rm <container>  # remove container
docker rmi <image>     # remove images

connect with github generate the aacess token and add in jenkins

# Step 14: Configure Jenkins to use GitHub Personal Access Token
Open Jenkins Dashboard → Manage Jenkins → Configure System

# install docker compose
sudo apt install docker-compose -y
create docker-compose file
version : "3.3"
services: 
  web:
    build : .
    ports : 
      - "8001:8001"

docker-compose down
docker-compose up -d --force-recreate --no-deps --build web



## Ansible installation
# Install Ansible on Ubuntu 20.04
launch 1 master node
# launch 3 worker nodes
# install ansible on master node
sudo apt update
sudo apt install ansible -y

paste the pem key there
cd .ssh
sudo vim ansible_demo.pem


in master node to ssh into server node 
sudo chown ubuntu:ubuntu ~/.ssh/ansible-master.pem
chmod 400 ~/.ssh/ansible-master.pem

sudo ssh -i ~/.ssh/ansible_demo.pem ubuntu@65.1.148.171

logout

cat /etc/ansible/hosts
if no inventory file or host found the first create the folder ansible
mkdir ansible
cd ansible

vim hosts
ubuntu@ip-172-31-4-214:~/ansible$ 
ubuntu@ip-172-31-4-214:~/ansible$ cat hosts
[servers]
server1 ansible_host=13.126.51.210
server2 ansible_host=13.203.101.195
server3 ansible_host=65.1.108.128
[all:vars]
ansible_python_interpreter=/usr/bin/python3

to check weather invetory is correct or not
ansible-inventory --list -y -i  /home/ubuntu/ansible/hosts

to check connection
ansible all -i /home/ubuntu/ansible/hosts -m ping --private-key=~/.ssh/ansible-master.pem

to check ram space
ansible all -i /home/ubuntu/ansible/hosts -m shell -a "free -h" --private-key=~/.ssh/ansible-master.pem