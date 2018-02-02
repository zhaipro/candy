#!sh
# Geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
tar -x geckodriver -zf geckodriver-v0.19.1-linux64.tar.gz -O > /usr/bin/geckodriver
chmod +x /usr/bin/geckodriver
rm geckodriver-v0.19.1-linux64.tar.gz

apt-add-repository ppa:mozillateam/firefox-next
apt-get update
apt-get install firefox
