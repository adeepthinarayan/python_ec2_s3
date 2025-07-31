Use this in User Data:
=============
#!/bin/bash

apt update -y
apt install -y git python3-pip python3-venv

cd /opt
git clone https://github.com/adeepthinarayan/python_ec2_s3.git
cd python_ec2_s3

python3 -m venv venv
source venv/bin/activate

pip install flask

nohup venv/bin/python app.py > output.log 2>&1 &
