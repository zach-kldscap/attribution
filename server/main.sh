sudo nginx -s stop
sudo nginx -c /home/zach_dingels/projects/attribution/server/nginx.conf
# ngxtop -l /var/log/nginx/access.log
gunicorn -c gunicorn.conf.py -b :8080 wsgi:app
