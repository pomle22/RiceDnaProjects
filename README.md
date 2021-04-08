# README #
This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### Database migrations
Solution - 1
Remove pyc files from your migrations folder.
Solution - 2
Need to remove that reference from testBolt.0001_initial by editing migration file.
Solution - 3
Remove the new changes from the modals and run python manage.py migrate --fake
Now again modify your models with new changes
Run python manage.py makemigrations
And then again run python manage.py migrate

### cmd other use for django
find . -name "*.pyc" -exec rm -f {} \; #remove all .pyc

### setup apache wsgi 
https://www.tutorialspoint.com/django/django_apache_setup.htm

### cmd for framework Django  => https://docs.djangoproject.com/en/2.2/ref/django-admin/
django-admin <command> [options]
python manage.py <command> [options]
python manage.py startapp <app_name>
python manage.py createsuperuser
python manage.py runserver <ip:port>
python -m django <command> [options] 
pip install Django==2.2.3
### cmd for Deploy ###
lsof -t -i tcp:8000 | xargs kill -9
screen -ls
screen -dmSL <name_screen> python manage.py runserver <ip:port>

### install anaconda => https://docs.anaconda.com/anaconda/install/

### clean migrations => https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
in folder migrations need __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py makemigrations

### python anaconda
*** activate env before run project
*** use pip for install lib
*** use python for run cmd django
conda create -n <env_name> python=3.7.1 anaconda
conda activate <env_name>
pip install django==2.2.3
cd ..
### install lib
pip install -r requirements.txt
conda install -c bioconda mysqlclient

y
### database 
python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate

insert default database => /project/db_default/*

### mongo
db.getCollection('<collection_name>').totalIndexSize()
db.getCollection(‘<collection_name>’).stats()
db.getCollection('<collection_name>').getPlanCache().clear()
db.getCollection('<collection_name>').createIndex({<field>: <1=asc or -1=desc>,_id: <1=asc or -1=desc>})
db.getCollection('<collection_name>').getIndexes()
db.getCollection('<collection_name>').reIndex()




git pull git@bitbucket.org:joesoftheart/biobank.git dev
git push git@bitbucket.org:joesoftheart/biobank.git dev

### create suprt users
python manage.py createsuperuser

### django Mongo DB 
https://django-mongodb-engine.readthedocs.io/en/latest/topics/setup.html

### start web app 
 conda activate biobankenv
 cd /Users/athiphat/Desktop/biobank/src

### mail center
user : nationalbiobank@gmail.com
pass : Nationalbi0bankn

### start xampp
sudo /Applications/XAMPP/xamppfiles/bin/apachectl start

### Let encrypt
sudo yum install certbot python2-certbot-apache mod_ssl
sudo certbot --apache -d gaapinno.net

### set data server
date
ls -l /etc/localtime
timedatectl list-timezones | grep Asia
timedatectl set-timezone Asia/Bangkok


### Deploy mod_wsgi
yum install epel-release centos-release-scl
yum install python36 python36-devel httpd httpd-devel rh-python36-mod_wsgi
rpm -ql rh-python36-mod_wsgi
mv /opt/rh/httpd24/root/etc/httpd/conf.modules.d/10-rh-python36-wsgi.conf /etc/httpd/conf.modules.d/10-rh-python36-wsgi.conf
mv /opt/rh/httpd24/root/usr/lib64/httpd/modules/mod_rh-python36-wsgi.so /etc/httpd/modules/mod_rh-python36-wsgi.so
python3.6 -m venv thaimerrenv
source thaimerrenv/bin/activate
  
sudo getsebool httpd_can_network_connect_db
sudo setsebool -P httpd_can_network_connect_db on
sudo getsebool httpd_can_network_connect_db
  
systemctl restart httpd
restorecon -Rv /var/www
chown -R apache:apache /var/www/thaimerr_v2/
getenforce
sudo setenforce 0
getenforce
sudo vi /etc/selinux/config
reboot

create file /etc/httpd/sites-enabled/<project>.conf at permission 755
<VirtualHost *:80>
        ServerAdmin tonkha23@gmail.com
        ServerName gaapinno.net
        ServerAlias gaapinno.net
        RewriteEngine on
#       RewriteCond %{SERVER_NAME} =www.gaapinno.net [OR]
#       RewriteCond %{SERVER_NAME} =gaapinno.net
#       RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,QSA,R=permanent]
#       RewriteEngine On
        RewriteCond %{SERVER_PORT} !^443$
        RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
        DocumentRoot /var/www/

        Alias /static /var/www/gaap/static
        <Directory "/var/www/gaap/static">
                Options FollowSymLinks
                Order allow,deny
                Allow from all
                Require all granted
        </Directory>

        Alias /media /var/www/gaap/media
        <Directory "/var/www/gaap/media">
                Options FollowSymLinks
                Order allow,deny
                Allow from all
                Require all granted
        </Directory>
        ErrorLog logs/gaap_error.log
        CustomLog logs/gaap_access.log combined
        WSGIDaemonProcess gaapinno.net python-home=/var/www/gaapenv/lib/python3.6/site-packages python-path=/var/www/gaap

        WSGIProcessGroup gaapinno
        WSGIScriptAlias / /var/www/gaap/Settings/wsgi.py
        WSGIPassAuthorization On
        WSGIApplicationGroup %{GLOBAL}
        <Directory /var/www/gaap/Settings>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>
</VirtualHost>

     
 vi /etc/httpd/conf/httpd.conf
 insert line -> IncludeOptional sites-enabled/*.conf


// in ssl
<IfModule mod_ssl.c>
<VirtualHost _default_:443>
ServerName gaapinno.net

ServerSignature Off

RewriteEngine On
# Some rewrite rules in this file were disabled on your HTTPS site,
# because they have the potential to create redirection loops.

# RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI}

        Alias /static /var/www/gaap/static
        <Directory "/var/www/gaap/static">
                Options FollowSymLinks
                Order allow,deny
                Allow from all
                Require all granted
        </Directory>

        Alias /media /var/www/gaap/media
        <Directory "/var/www/gaap/media">
                Options FollowSymLinks
                Order allow,deny
                Allow from all
                Require all granted
        </Directory>
#        ErrorLog ${APACHE_LOG_DIR}/gaap_error.log
#        CustomLog ${APACHE_LOG_DIR}/gaap_access.log combined
#        WSGIDaemonProcess gaapinno.net python-home=/home/athiphat/web/gaapenv python-path=/var/www/gaap
         WSGIDaemonProcess gaapinno python-home=/var/www/gaapenv python-path=/var/www/gaap
         WSGIProcessGroup gaapinno
         WSGIScriptAlias / /var/www/gaap/Settings/wsgi.py
#ErrorLog /var/log/httpd/redirect.error.log
LogLevel warn
SSLCertificateFile /etc/letsencrypt/live/gaapinno.net/cert.pem
SSLCertificateKeyFile /etc/letsencrypt/live/gaapinno.net/privkey.pem
Include /etc/letsencrypt/options-ssl-apache.conf
SSLCertificateChainFile /etc/letsencrypt/live/gaapinno.net/chain.pem
</VirtualHost>
</IfModule>
 