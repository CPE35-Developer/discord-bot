sudo apt install -y npm
sudo npm install forever -g
sudo apt install -y ffmpeg
wget https://anaconda.org/anaconda-adam/adam-installer/4.4.0/download/adam-installer-4.4.0-Linux-x86_64.sh
bash adam-installer-4.4.0-Linux-x86_64.sh -b -p ~/adam
echo -e '\n# Anaconda Adam\nexport PATH=~/adam/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

sudo apt install -y python3-pip

