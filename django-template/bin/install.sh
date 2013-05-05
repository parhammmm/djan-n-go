#!/bin/bash
sudo apt-get install --assume-yes python-software-properties python g++ make git
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
sudo npm install -g yuglify

sudo apt-get upgrade

sudo curl http://python-distribute.org/distribute_setup.py | python
sudo curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python

sudo pip install virtualenv

cd ..

virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt

python manage.py syncdb
python manage.py migrate

sudo chown $USER development.db
