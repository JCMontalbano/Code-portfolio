! systemctl is-active --quiet elasticsearch && sudo service elasticsearch start #check and turn on elasticsearch service
systemctl is-active --quiet elasticsearch && echo Service is running 
curl localhost:9200
python3 cricket.py
