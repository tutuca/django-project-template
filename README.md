{{project_name}}
===============


Valiendonos de la prestación de django 1.4 para tomar un molde de proyecto, 
y con la intención de formalizar algunas prácticas que a esta altura son
rutinarias preparamos este molde.

Algunas prestaciones de este molde son:

- Incluye templates y estilos genericos.
- Incluye django debug toolbar, pagination.
- Configuraciones genericas para statics y media.
- Algunos chiches más.

Uso
---------------

Clone el paquete en algun lugar accesible:

    $ git clone git://github.com/Inventta/django-project-template.git

Cree y active un [entorno virtual](http://pypi.python.org/pypi/virtualenv) para el 
proyecto:

    $ cd ~/venvs/ # adapte este path a su preferencia
    $ virtualenv {{project_name}}
    $ source {{project_name}}/bin/activate

Modificar los parámetros de la base de datos

    #local_settings.py
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'fudepan',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
    }   

> En producción local_settings.py debería tener DEBUG=False
    
# Inicializar la base de datos.

Primero es necesario crear los esquemas y ejecutar las migraciones si hacen falta:
    
    $ ./manage.py migrate


De realizarse cambios en algún modelo ejecutar:

    $ ./manage.py makemigrations website

Reemplazar *website* con la aplicación que necesitamos migrar

En este punto tenemos nuestra instancia lista para correr el servidor de 
desarrollo:

    $ ./manage.py runserver

# Assets státicos.

Ahora queda generar los recursos de estilos, imágenes, íconos y scripts.
Para esto integramos [grunt](http://gruntjs.com/) y [bower](http://bower.io/).

Descargar las herramientas necesarias:

    $ npm install  

> a la fecha, grunt no incluye la interfaz de linea de comandos por defecto y 
> necesita ser instalado separado.
> para esto invocar:
    $ npm install -g grunt-cli
> utilizar *sudo* en caso que sea necesario

Instalar las bibliotecas utilizadas

    $ bower install

Ejecutar las tareas de grunt:

    $ grunt

Por defecto grunt funciona en modo `watch`, esto es: queda observando los archivos importantes de manera de re-ejecutar las tareas pertinentes.

Si sólo necesitamos `compilar` los recursos estáticos, invocar:

    $ grunt build

Ésto genera una carpeta `static/` en la raiz del proyecto, que podemos desplegar en nuestro servidor.

> Nota: Este texto y la nota de licencia están incluidos en el molde y se 
> aplicarán a todos los proyectos que cree con este método.
> Recomendamos con énfasis modificar estos textos para adaptarlos a su entorno.


Noticia de licencia
---------------
© 2015 
{{project_name}} es software libre de Matías Iturburu, Martín Onetti y Francisco Herrero,
distribuido bajo la licencia BSD. Una copia 
de esta licencia se incluye en el archivo COPYING.
Instale las dependencias necesarias:
