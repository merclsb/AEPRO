# AEPRO

Trabajo fin de grado del Curso de Adaptación al grado de Ingenieria Informática

![Unir Logo](https://www.decointerior.es/wp-content/uploads/2015/01/logo-unir-e1423826671421.png)

# Pasos para la instalación

```
mkdir aepro && cd aepro/

virtualenv -p python3.4 .

source bin/activate

pip install -r requisitos.txt

cd src

./manage.py migrate

http://127.0.0.1:8000/

http://127.0.0.1:8000/admin

```
# Cosideraciones previas

```
Tener instalado: pidof

Bootsatrap DateTime Widget 
  Al importarlo (bootstrap3_datetime.widgets import DateTimePicker) genera un error, por lo que 
  hay que dirigirse a  #/$PATH/DateTime/lib/python3.4/site-packages/bootstrap3_datetime/widgets.py
  y modificar la importacion: #from django.forms.utils import flatatt

```

# La aplicación


![](https://image.ibb.co/jcyYbk/Screen_Shot_2017_08_30_at_14_27_57.png)

![](https://image.ibb.co/fpUbe5/Screen_Shot_2017_08_30_at_13_21_24.png)

![](https://image.ibb.co/iWT8wv/Screen_Shot_2017_09_02_at_11_15_42.png)

![](https://image.ibb.co/mt88wv/Screen_Shot_2017_09_02_at_10_42_58.png)
