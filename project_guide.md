📝 Django ToDo App - DevOps Deployment Project
A beginner-friendly full-stack DevOps project for deploying a Django-based ToDo app using:

EC2 (AWS)

Docker

Jenkins

Ansible

Kubernetes (Minikube)

CI/CD best practices

🌱 Prerequisites
AWS Account with access to EC2

GitHub account with the app code (fork or clone)

Basic terminal knowledge

PEM key for EC2 access

Django project (django-todo-app) ready on GitHub

🚀 PART 1: Launch and Setup EC2 Server
✅ Step 1: Launch EC2 Instance (Ubuntu 22.04)
Choose instance type: t2.micro or t3.medium (for Minikube)

Add inbound rules for: 22, 8000, 8001, 8080, 30000-32767

Download .pem key file

✅ Step 2: Connect to EC2

ssh -i your-key.pem ubuntu@your-ec2-public-ip
🧱 PART 2: Deploy Django App (Basic)
✅ Step 1: Clone the Django App
mkdir ~/project && cd ~/project
git clone https://github.com/your-username/django-todo-app.git
cd django-todo-app
✅ Step 2: Install Python & Virtual Env
sudo apt update
sudo apt install python3-pip python3-venv -y
✅ Step 3: Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate
✅ Step 4: Install Django
pip install django
django-admin --version
✅ Step 5: Run Django App
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
✅ Step 6: Update Security Group in AWS
Go to EC2 > Security Groups > Inbound rules

Add rule: TCP / 8000 / 0.0.0.0/0

Visit:
http://<your-ec2-ip>:8000

🔄 Run App in Background
nohup python manage.py runserver 0.0.0.0:8001 &
Output will be logged to nohup.out

Visit http://<your-ec2-ip>:8001

🛑 To Stop Server



lsof -i:8001
kill <PID>
🐳 PART 3: Dockerize the Django App
✅ Step 1: Install Docker



sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
✅ Step 2: Create Dockerfile
Dockerfile


# Dockerfile
FROM python:3.11

WORKDIR /app

 . .

RUN pip install django==3.2

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
✅ Step 3: Build Docker Image



sudo docker build -t todo-app .
✅ Step 4: Run Docker Container



sudo docker run -p 8001:8001 todo-app
# Or in background:
sudo docker run -d -p 8001:8001 todo-app
⚙️ PART 4: Jenkins Setup on EC2
✅ Step 1: Install Java and Jenkins



sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-17-jdk -y
java -version

# Add Jenkins repo
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list

# Install Jenkins
sudo apt update
sudo apt install jenkins -y
✅ Step 2: Start Jenkins



sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins
✅ Step 3: Open Jenkins Port (8080)
 inbound rule in EC2 security group to allow TCP 8080

✅ Step 4: Access Jenkins in Browser
cpp


http://<your-ec2-ip>:8080
Get initial admin password:




sudo cat /var/lib/jenkins/secrets/initialAdminPassword
🧪 PART 5: Jenkins + Docker Integration
✅ Step 1: Enable Docker for Jenkins



sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
sudo reboot
✅ Step 2: Add Jenkins Job (Freestyle)
Source Code Mgmt: GitHub repo

Build → Execute Shell:




#!/bin/
cd /var/lib/jenkins/workspace/django-todo-app
docker build -t todo-app .
docker rm -f todo-app-container || true
docker run -d -p 8001:8001 --name todo-app-container todo-app
⚙️ PART 6: Ansible Setup
✅ Step 1: Install Ansible on Master EC2



sudo apt update
sudo apt install ansible -y
✅ Step 2: Configure Inventory
ini


# ~/ansible/hosts
[servers]
server1 ansible_host=13.126.51.210
server2 ansible_host=13.203.101.195
server3 ansible_host=65.1.108.128

[all:vars]
ansible_python_interpreter=/usr/bin/python3
✅ Step 3: Add PEM Key & Test Connection



chmod 400 ~/.ssh/ansible-master.pem

ansible-inventory --list -y -i ~/ansible/hosts
ansible all -i ~/ansible/hosts -m ping --private-key=~/.ssh/ansible-master.pem
✅ Sample Playbooks
yaml


# create_file.yml
- name: Create a file
  hosts: all
  become: true
  tasks:
    - name: Create file.txt
      file:
        path: /home/ubuntu/file.txt
        state: touch
Run it:




ansible-playbook -i ~/ansible/hosts create_file.yml --private-key=~/.ssh/ansible-master.pem
☸️ PART 7: Kubernetes with Minikube on EC2
✅ Step 1: Install Docker & Minikube



# Docker
sudo apt update
sudo apt install -y ca-certificates curl gnupg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

minikube start --driver=docker
✅ Step 2: Install kubectl



sudo apt-get install -y apt-transport-https curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg \
  https://packages.cloud.google.com/apt/doc/apt-key.gpg

echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] \
  https://apt.kubernetes.io/ kubernetes-xenial main" | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list > /dev/null

sudo apt-get update
sudo apt-get install -y kubectl
✅ Step 3: Create Kubernetes Resources
yaml


# deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo
  template:
    metadata:
      labels:
        app: todo
    spec:
      containers:
      - name: todo-container
        image: anilvcr/todoapp:v1
        ports:
        - containerPort: 8001
yaml


# service.yml
apiVersion: v1
kind: Service
metadata:
  name: todo-service
spec:
  type: NodePort
  selector:
    app: todo
  ports:
    - port: 80
      targetPort: 8001
      nodePort: 30007
✅ Apply and Access



kubectl apply -f deployment.yml
kubectl apply -f service.yml
minikube service todo-service --url
📌 Final Notes
Open EC2 ports: 8000, 8001, 8080, 30000-32767

Secure credentials and avoid exposing .pem or tokens in public repos

Use .env files for environment configs

Use requirements.txt for dependency management

