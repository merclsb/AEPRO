virtualenv -p python3.4 .

source bin/activate

pip install -r requisitos.txt

src/manage.py migrate