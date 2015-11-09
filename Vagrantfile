# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

    config.vm.define "controller" do |config|
        config.vm.box = "ubuntu/trusty64"
        config.vm.hostname = "controller"
        config.vm.network "private_network", ip: "10.0.0.2"
        config.vm.synced_folder '.', '/home/vagrant/kangaroo'
        config.vm.synced_folder '/etc/kangaroo', '/etc/kangaroo'        
        config.vm.network "forwarded_port", guest: 8080, host: 8080
        config.vm.provision "shell", inline: <<-SHELL

mkdir -p /etc/mysql/conf.d/
cat > /etc/mysql/conf.d/db.cnf <<EOL
[mysqld]
bind-address = 10.0.0.2
EOL

sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password password'
sudo apt-get -y install mysql-server
mysql --user=root --password=password -e "CREATE DATABASE kangaroo;"
mysql --user=root --password=password -e "GRANT ALL PRIVILEGES ON kangaroo.* TO 'kangaroo'@'10.0.0.3' IDENTIFIED BY 'password';"


apt-get -y install rabbitmq-server
#rabbitmq-plugins enable rabbitmq_management
rabbitmqctl delete_user guest

rabbitmqctl add_user kangaroo password
rabbitmqctl add_vhost kangaroo-app
rabbitmqctl set_permissions -p kangaroo-app kangaroo ".*" ".*" ".*"

service rabbitmq-server restart


apt-get install -y python-dev
curl -s https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python
pip install virtualenv

        SHELL

        config.vm.provision "shell", privileged: false, inline: <<-SHELL

virtualenv /home/vagrant/.ve/australia --prompt "(Australia)"
source /home/vagrant/.ve/australia/bin/activate
cd /home/vagrant/kangaroo/
python setup.py develop
        SHELL
    end

    config.vm.define "compute" do |config|
        config.vm.box = "ubuntu/trusty64"
        config.vm.hostname = "compute"
        config.vm.network "private_network", ip: "10.0.0.3"
        config.vm.synced_folder '.', '/home/vagrant/kangaroo'
        config.vm.synced_folder '/etc/kangaroo/', '/etc/kangaroo/'
        config.vm.synced_folder '/home/nmarchenko/img', '/home/vagrant/kangaroo/img'

        config.vm.provision "shell", inline: <<-SHELL
apt-get install -y python-dev bridge-utils kvm libvirt-bin libvirt-dev
cp /home/vagrant/kangaroo/img/trusty-server-cloudimg-amd64-disk1.img /var/lib/libvirt/images/
curl -s https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py | python
pip install virtualenv
        SHELL

        config.vm.provision "shell", privileged: false, inline: <<-SHELL
virtualenv /home/vagrant/.ve/australia --prompt "(Australia)"
source /home/vagrant/.ve/australia/bin/activate
cd /home/vagrant/kangaroo/
python setup.py develop
        SHELL

    end

end
