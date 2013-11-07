=====================================================
Dujour Back-End Repository
=====================================================

Update the server and setup the basic security system
------------------------------------------------------
Update the server::

    sudo apt-get update
    sudo apt-get dist-upgrade -y

Add new user and setup the security system which prevents someone trying the password::

    sudo adduser dbtsai
    # Add my account into adm and admin groups
    sudo vim /etc/group 
    sudo apt-get install ssh denyhosts vim 
    # Modify the configuration 
    vim /etc/denyhosts.conf  
    # Change PermitRootLogin to no in order to prevent to login by root
    # Change PasswordAuthentication to yes in order to login using password
    vim /etc/ssh/sshd_config 


Installation
------------
Install the server environments using ``apt-get`` in ubuntu::

    sudo apt-get install  nginx-extras python-pip python-mysqldb libxml2-dev python-dev python-imaging \
                          python-pylibmc apparmor-utils git unzip postfix p7zip-full whois dnsutils mutt \
                           php5-fpm php5-mysql python-pylibmc \
                           mysql-server mysql-client    

    # Add bash shell for www-data, and change home folder of www-data to /home/www-data
    sudo vim /etc/passwd
    sudo su www-data
    ssh-keygen

Setup MySQL database::

    sudo service mysql stop
    sudo mkdir /home/www-data
    sudo mkdir /home/www-data/sites
    sudo chown -R  www-data:www-data /home/www-data
    sudo mkdir /home/www-data/mysql_db
    sudo cp -R /var/lib/mysql/* /home/www-data/mysql_db/
    sudo chown -R mysql:mysql /home/www-data/mysql_db
    sudo chmod 700 /home/www-data/mysql_db

    # Change datadir to /home/www-data/mysql_db   
    sudo vim /etc/mysql/my.cnf

    # Since apparmor doesn't allow MySQL running outside the default folder,
    # we have to change the configuration file of apparmor.     
    # Change /etc/apparmor.d/abstractions/mysql from
    # /var/lib/mysql/mysql.sock rw,
    #    to
    # /home/www-data/mysql_db/mysql.sock rw,
    sudo vim /etc/apparmor.d/abstractions/mysql
    sudo aa-complain mysql
    sudo service mysql start

Setup PHP5-fpm and phpMyAdmin::

    sudo su www-data
    mkdir /home/www-data/sites/database.dujour.im
    mkdir /home/www-data/sites/database.dujour.im/public_html
    # Download the phpMyAdmin and unzip it in public_html
    exit
    sudo vim /etc/nginx/sites-available/database.dujour.im 
    # Add the folloing configuration
    server {
        listen   80;
        server_name  database.dujour.im;
	
        access_log  /var/log/nginx/database.dujour.im.access.log;
        error_log   /var/log/nginx/database.dujour.im.error.log debug;
        rewrite_log  on;
        
        root /home/www-data/sites/database.dujour.im/public_html;

        index  index.php index.html index.htm;

        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        location ~ \.php$ {
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            include fastcgi_params;
        }

    }
    
    sudo ln -s /etc/nginx/sites-available/database.dujour.im /etc/nginx/sites-enabled/database.dujour.im
    sudo /etc/init.d/nginx restart
    sudo /etc/init.d/php5-fpm restart

Setup the memcached::
    
    sudo apt-get install memcached
    vim /etc/memcached.conf
    # change the memory size to 1024MB
    service memcached restart
    # testing if the memcached is running
    telnet localhost 11211
    
Setup the back-end::

    sudo pip install uwsgi
    sudo su www-data
    mkdir /home/www-data/sites/api.dujour.im
    cd /home/www-data/sites/api.dujour.im
    git clone git@github.com:dujour/back-end.git
    # Create a database dujour and do syncdb
    python manage.py syncdb
    vim /etc/nginx/sites-available/api.dujour.im
    ln -s /etc/nginx/sites-available/api.dujour.im /etc/nginx/sites-enabled/api.dujour.im
    touch /var/log/uwsgi.log
    chown www-data:www-data /var/log/uwsgi.log
    /etc/init.d/uwsgi restart

Setup the front-end::

    mkdir /home/www-data/sites/www.dujour.im
    
    # You can get the www.dujour.im from the front-end repo
    vim /etc/nginx/sites-available/www.dujour.im
    ln -s /etc/nginx/sites-available/www.dujour.im /etc/nginx/sites-enabled/www.dujour.im
    
    
    
