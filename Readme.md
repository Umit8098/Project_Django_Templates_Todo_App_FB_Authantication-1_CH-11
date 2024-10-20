
#### Baştan proje kurulumu ->

```bash
- python -m venv env
- ./env/Scripts/activate
- pip install django
- python.exe -m pip install --upgrade pip
- pip freeze
- pip install python-decouple
- pip freeze > requirements.txt
```

```bash
- django-admin startproject main .
- py manage.py runserver
- py manage.py startapp todo
- py manage.py migrate
- py manage.py runserver
```

### Secure your project

#### .gitignore

Add standard .gitignore file to the project root directory. 

Do that before adding your files to staging area, else you will need extra work to unstage files to be able to ignore them.

<.gitignore> ->

```py
# Environments
.env
.venv
env/
venv/
```

#### python-decouple

- Create .env file on root directory. We will collect our variables in this file.

<.env> ->

```py
SECRET_KEY = django-insecure-9p72pxko$)cm=wwzt81kg*6u-%#j*iyxhens02^96bw&iq2idn
```

<settings.py> ->

```py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

- From now on you can send you project to the github, but double check that you added a .gitignore file which has .env on it.


- Run the server and see the initial setup:
 
```bash
py manage.py migrate
```

```bash
py manage.py runserver  # or;
python manage.py runserver  # or;
python3 manage.py runserver
```

///////////////////////////////////////////////
#### GİTHUB REPODAN clone bir projeyi ayağa kaldırma ->

```bash
- python -m venv env
- ./env/Scripts/activate
- pip install -r requirements.txt
- python.exe -m pip install --upgrade pip
- pip install python-decouple
- pip freeze > requirements.txt
```

- create .env and inside create SECRET_KEY 

```bash
- python manage.py migrate
- python manage.py runserver
```

///////////////////////////////////////////////

- Projeyi ve app imizi oluşturduk, .gitignore ve .env dosyalarımızı da oluşturup SECRET_KEY imizi ve env ımızı içerisine koyduk.
- app imizi settings.py daki INSTALLED_APPS e ekliyoruz.
  
```py
  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # myApps
    'todo',
]
```

- Önce url configurasyonumuzu yapıyoruz;
- ana urls.py ımıza app imizin urls.py ını include ediyoruz. Hemen sonra todo app imizin urls.py ını create ediyoruz.
  
main <urls.py> ->

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("todo.urls")),
]
```

- todo app imizin urls.py ını create edip içini yazıyoruz.
  
todo <urls.py> ->

```py
from django.urls import path

urlpatterns = [

]
```

- tabi burada ekrana göndereceğimiz template in view ini yazmamız gerekiyor;
- app in views.py ına gidiyoruz, ve basit bir HttpResponse döndürmek için önce impor edip sonra view de bir string ifade yazıyoruz. Html kodları da kullanılabilir.

todo <views.py> ->

```py
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1 style="text-align:center; color:blue;">Welcome</h1>')
```

- view imizin urls.py da path ini belirtiyoruz.

todo <urls.py> ->

```py
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

- server ımızı çalıştırıyoruz ve Welcome ifadesini css leri ile gördük.

- Önce todo app <models.py> da modelimizi tanımlıyoruz. VSCode da emoji kullanabiliyoruz. 
  Mac için -> CTRL+cmd+space üçüne aynı anada basılı tutuyoruz
  Win için -> Win+. 
Bunun için : ve ardından Win+. ile seçiyoruz.

todo <models.py> ->
```py
from django.db import models

status_choices = [
    ('C', 'Completed'),
    ('P', 'Pending'),
    ('I', 'In-Progress')
]

priority_choices = [
    ('1', '1️⃣'),
    ('2', '2️⃣'),
    ('3', '3️⃣'),
    ('4', '4️⃣'),
    ('5', '5️⃣'),
]

class Todo(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    status = models.CharField(max_length=2, choices=status_choices)
    priority = models.CharField(max_length=2, choices=priority_choices)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```

- Modelimizi oluşturduk. Fakat django ve db nin bundan haberi yok server ı durdurup makemigrations ve migrate yapıyoruz.

```bash
- py manage.py makemigrations
- py manage.py migrate
```

-  todo admin.py a gidip Todo modelimizi import ederek register ediyoruz,

todo <admin.py> ->

```py
from django.contrib import admin
from .models import Todo

# Register your models here.
admin.site.register(Todo)
```

- Hemen ardından admin site ı da ayağa kaldıralım. Admin panele login olabilmek için superuser oluşturuyoruz.

```bash
- py manage.py createsuperuser
- py manage.py runserver
```

- admin panele gidip Todo modelimize veri girişi yapıyoruz. Todo ekliyoruz, object create ediyoruz.

### Read

- views kısmına geçiyoruz, admin panelden kaydettiğimiz verileri (todo ları) ekrana basit bir şekilde yazdıralım (Read). Bunun için dataları db den çekmemiz lazım, Todo modelini import edip view imizde orm ile verileri çekip  bir değişkene atayıp onu da context içerisinde render edeceğimiz template e gönderiyoruz.

todo <view.py> ->
```py
from django.shortcuts import render
from .models import Todo

# Create your views here.

def home(request):
    todos = Todo.objects.all()
    context = {
        "todos" : todos
    }
    return render(request, 'todo/home.html', context)
```

- View i yazdık, template imizi oluşturuyoruz, app imizin altında 'templates' klasörü ve onun da altında app imizin ismiyle 'todo' klasörümüzü oluşturup içerisine template lerimizi yazıyoruz. Önce bir base.html hazırlayıp arkasından diğer template lerimizi mesela home.html oluşturup base.html i extends ediyoruz.
  
todo/templates/todo <base.html> ->

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Umit Todo App</title>
</head>
<body>
    
    {% block content %}
        
    {% endblock content %}
        
</body>
</html>
```

- context in içerisinde gönderdiğimiz verileri home template page inde çağırarak gösteriyoruz.

todo/templates/todo <home.html> ->

```html
{% extends 'todo/base.html' %}

{% block content %}
    
{{ todos }}

{% endblock content %}
```

- Bize query set olarak dönen verileri for döngüsüyle todolarımızı ul li tagleriyle tek tek yazdırıyoruz.
  
todo/templates/todo <home.html> ->

```html
{% extends 'todo/base.html' %}

{% block content %}
    
<ul>
    {% for todo in todos %}  
    <li>{{ todo }}</li>
    {% endfor %}
</ul>

{% endblock content %}
```

- Objeleri şuna göre ascending/descending olarak sırala;
todo/views.py
```py
def home(request):
    todos = Todo.objects.all().order_by('priority')
    ...
```


### Create

- Şimdi db deki verileri (todo) gördük, şimdi kullanıcıdan veri girişi yapmasını isteyeceğiz ki kendi todolarını oluştursun (Create). Kullanıcıdan veri isterken form kullanıyoruz. Bunun için önce bir form oluşturacağız. todo app imizin altında forms.py diye bir dosya oluşturuyoruz. Burada modelForm kullanacağız. Önce importlarımızı yapıyoruz. Burada model forms kullanacağımız için modelimizi de import ediyoruz.

todo <forms.py> ->

```py
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
```

- Oluşturduğumuz formu views den çağırıp oluşturduğumuz contex içerisinde template imize göndereceğiz.
  
todo <views.py> ->

```py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo
from .forms import TodoForm

...

def todo_create(request):
    form = TodoForm()
    context = {
        "form" : form
    }
    return render(request, 'todo/todo_add.html', context)

```

- Şimdi oluşturduğumuz view e bir template yazacağız.
  
todo/templates/todo <todo_add.html> ->

```html
{% extends 'todo/base.html' %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Add">
    </form>
{% endblock content %}
```

- Şimdi oluşturduğumuz todo_create view inin path ini  todo app imizin urls.py ında belirtiyoruz.

todo <urls.py> ->

```py
from django.urls import path
from .views import (
    home,
    todo_create,
)

urlpatterns = [
    path('', home, name='home'),
    path('add/', todo_create, name='add'),
]
```

- Formumuzu ekrana yansıttık ancak kullanıcı bu formu doldurup add butonuna tıkladığında herhangi birşey olmaz çünkü view inde bunun logic ini yazmadık. 
- Şimdi bu formda gelen bilgileri karşılamamız lazım. Şu anda Post methodu ile gelen veriyi handle etme işini yaptık.

todo <views.py> ->

```py
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.

def home(request):
    todos = Todo.objects.all()
    context = {
        "todos" : todos
    }
    return render(request, 'todo/home.html', context)

def todo_create(request):
    form = TodoForm()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {
        "form" : form,
    }
    return render(request, 'todo/todo_add.html', context)
```

- Artık todo ları;
 - listeleyebiliyoruz, 
 - create edebiliyoruz. 

- Ancak ayrı ayrı sayfalarda değil de aynı sayfada yapmak istiyoruz. home sayfasında hem listeleyip hem de todo eklemek istiyoruz. home view ine gidip kullanıcının doldurmasını istediğimiz formu form değişkenine tanımlayıp, context içinde template ine gönderiyoruz ve arkasından home template inde bu formu gösteriyoruz.

todo <views.py> ->

```py
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.

def home(request):
    todos = Todo.objects.all()
    form = TodoForm()
    context = {
        "todos" : todos,
        "form" : form,
    }
    return render(request, 'todo/home.html', context)

def todo_create(request):
    form = TodoForm()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo:home')
        
    context = {
        "form" : form,
    }
    return render(request, 'todo/todo_add.html', context)

```

- Arkasından home template ine gidip orada bu formu gösteriyoruz.


todo/templates/todo <home.html> ->

```html
{% extends 'todo/base.html' %}

{% block content %}

<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Add">
</form>

<ul>
    {% for todo in todos %}
    <li>{{ todo }}</li>
    {% endfor %}
</ul>

{% endblock content %}
```

- Bakıyoruz evet formumuz home.html template ine geldi. Ancak post methoduyla handle etmemiz lazım. home view imizde bizim post methoduyla formumuzu hendle edecek bir yapımız yok. Bunun için; 
  1- todo_create view indeki şu yapıyı ->  
        if request.method == 'POST':
            form = TodoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('todo:home')
      home view inde form değişkeninin hemen altına taşımalıyım.

  2- todo_create view indeki yapıyı bozmadan, home.html template imizdeki form un action="/add/" url ine istek atmasını sağlayabiliriz.

- Biz ikinci yolu tercih ettik.

todo/templates/todo <home.html> ->

```html
{% extends 'todo/base.html' %}

{% block content %}

<form action="/add/" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Add">
</form>

<ul>
    {% for todo in todos %}
    <li>{{ todo }}</li>
    {% endfor %}
</ul>

{% endblock content %}
```

- Artık todo_add.html template'ine ihtiyacımız kalmadı.
- Read (listeleme), 
- Create (oluşturma) işlemini yaptık. 

- İki işlemimiz kaldı, Update ve Delete. Fakat  bunlara geçmeden önce kafa dağıtacak birşeyler yapalım; 


### Static file, navbar

- 1 Static file larımızı eklemeyi göreceğiz,
- 2 bir de navbar ekleyeceğiz.

- 1 static lerimizi aynı template lerimiz gibi ekliyoruz;
 - todo altında kullanacağımız static lerimiz için, todo app imizin altında "static" klasörü, onun da altında app imizin ismi olan "todo" kalsörü nün içerisinde oluşturuyoruz. 
 - static/todo -> ayrı ayrı static fileslar için css klasörü, js klasörü, images klasörü oluşturuyoruz.

- 2 Navbar ekleyeceğiz. base.html e giderek tüm sayfalarımızda navbar olmasını istediğimizden base.html e html/css code larını ekliyoruz. block content in hemen üzerine ekliyoruz. Burada bootstrap kullandık (ayarlarını yapacağız!). image'ı copy/paste yaptık,image klasörümüze.
- Ayrıca statics lerin çalışabilmesi için base.html template'imizin en üstüne  {% load static %} tag ini ekliyoruz.
 
todo <base.html> ->

```html
{% load static %}

    <!-- navbar start -->
    <nav class="navbar navbar-expand-lg navbar navbar-white">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
            <img src="{% static 'todo/images/cw_logo.png' %}" alt="Hi!" width="45" height="45">Umit_Developer Todo App</a>
        </div>
    </nav>

```

#### bootstrap and css ekleme

##### bootstrap ekleme (tailwind cdn de kullanılabilir.)

- Şimdi bootstrap ekliyoruz; Bunun için 
  https://getbootstrap.com/      bootstrap sayfasından include via CDN olarak belirttiği 
  1 - CSS only link ini base.html imizin head kısmına, title ın üzerine ekliyoruz.
  2 - JavaScript Bundle with Popper scripts ini base.html imizin body nin en alt kısmına ekliyoruz.

todo <base.html> ->

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- CSS only -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">

    <title>Umit Todo App</title>
</head>
<body>

        <!-- navbar start -->
        <nav class="navbar navbar-expand-lg navbar navbar-white">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                <img src="{% static 'todo/images/cw_logo.png' %}" alt="Hi!" width="45" height="45">Umit Todo App</a>
            </div>
        </nav>
    
    {% block content %}
        
    {% endblock content %}
    
    <!-- JavaScript Bundle with Popper -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>

</body>
</html>
```

- server refresh, biraz daha düzenli hale geldi.

##### css ekleme

- Şimdi css ekleyelim. css klasörü oluşturmuştuk içerisine style.css dosyası oluşturduk ve navbar ımıza arka plan rengi ekleyeceğiz. 
- navbar ımızın class ının ismi navbar, direkt bunu kullanabiliriz.
- oluşturduğumuz style.css dosyasının linkini base.html de tanımlıyoruz. 
  <link rel="stylesheet" href="{% static 'todo/css/style.css' %}">

todo <style.css> ->

```css
.navbar {
    background-color: cadetblue;
}
```

- navbar daki "Umit_Developer Todo App" yazısı siyah güzel durmuyor, navbarclass ını navbar-white dan navbar-dark a çeviriyoruz. 
  
```html
        <!-- navbar start -->
        <nav class="navbar navbar-expand-lg navbar navbar-dark">
            <div class="container-fluid">
                <a class="navbar-brand" href="/">
                <img src="{% static 'todo/images/cw_logo.png' %}" alt="Hi!" width="45" height="45">Umit Todo App</a>
            </div>
        </nav>
```

- home sayfasında todo lar ile form kısmını yan yana yapmak istiyoruz, bunun için home.html'de aşağıdaki değişiklikleri yapıyoruz;

todo <home.html> ->

```html
{% extends 'todo/base.html' %} {% block content %}
<div class="container">
  <div>
    <form action="add/" method="post">
      {% csrf_token %} {{ form.as_p }}
      <input type="submit" value="Add" />
    </form>
  </div>
  <div>
    <ul>
      {% for todo in todos %}
      <li>{{ todo }}</li>
      {% endfor %}
    </ul>
  </div>
</div>
{% endblock content %}

```
- daha önce style.css ile verdiğim style ları kabul ettiği halde şimdi etmiyor. Böyle olabiliyor. style.css dosyasının ismini değiştirip verdiğimde kabul etti. Neyse devam... 

todo <style.css> ->

```css
.navbar {
    background-color: cadetblue;
}

.container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}
```


### Update

- app imizin views.py ına giderek update yapıyoruz,
- todo_update view i parametre olarak request ile bir de id alıyor çünkü hangi todo yu update edeceğimi bilmesi gerekiyor. id yi de parametre olarak gönderince hangi todo üzerinde çalışılacağını bildiriyoruz.
- sonra Todo object leri arasından id si request ile todo nun id sine eşit olanı bir todo değişkenine tanımlıyoruz.
- sonra bir form değişkeni oluşturup içerisine instance ı yukarıdaki todo değişkenine tanımladığımız veriler olacak şekilde TodoForm tanımlıyoruz. Yani form umuzu yukarıdaki çektiğimiz veriyle dolduruyoruz.
- sonra çektiğimiz bu todo ve form değişkenlerini context yapısı ile template imize gönderiyoruz.
  
todo <views.py> ->
```py
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.

def home(request):
    todos = Todo.objects.all()
    form = TodoForm()
    context = {
        "todos" : todos,
        "form" : form,
    }
    return render(request, 'todo/home.html', context)

def todo_create(request):
    form = TodoForm()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo:home')
        
    context = {
        "form" : form,
    }
    return render(request, 'todo/todo_add.html', context)


def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    context ={
        "todo": todo,
        "form": form,
    }
    return render(request, 'todo/todo_update.html', context)

```

- oluşturduğumuz todo_update view inin template ini oluşturalım;

todo <todo_update.html> ->

```html
{% extends 'todo/base.html' %}

{% block content %}
    <h2>Todo Update</h2>
    <form action="" method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Update">
    </form>
{% endblock content %}
    
```

- oluşturduğumuz todo_update template inin todo urls.py ında path ini oluşturalım;

todo <urls.py> ->

```py
from django.urls import path
from .views import (
    home,
    todo_create,
    todo_update,
)

urlpatterns = [
    path('', home, name='home'),
    path('add/', todo_create, name='add'),
    path('update/<int:id>', todo_update, name='update'),
]

```

- url satırında todo/update/1 yazarak istek atınca bizi update sayfasına 1 id li todo nun verileriyle birlikte gönderiyor.
- Ancak bunu url e elle yazmaktansa todo larımıza a tag i ile birer link vererek update template ine yönlendirebiliriz. 
- Şimdi home.html de todo larımızı a tag i ile update url ine link verelim. Böylece adres satırına kendimiz update/todo'nun id sini yazmak yerine todonun üzerinde tıklayınca bizi otomatik olarak update/todo id si olarak o like yönlendirecek.
      <li><a href="{% url 'update' todo.id %}">{{ todo }}</a></li>

todo <home.html> ->

```html
{% extends 'todo/base.html' %} {% block content %}
<div class="container">
  <div>
    <form action="add/" method="post">
      {% csrf_token %} {{ form.as_p }}
      <input type="submit" value="Add" />
    </form>
  </div>
  <div>
    <ul>
      {% for todo in todos %}
      <li><a href="{% url 'update' todo.id %}" target="_blank">{{ todo }}</a></li>
      {% endfor %}
    </ul>
  </div>
</div>
{% endblock content %}
```

- evet artık update template imizde ilgili todo nun bilgilerinin dolu olduğu formumuzu görüyoruz, fakat input buttonu ile formumuzu update edemiyoruz, çünkü view imizde post ile gelen request için ne yapılacağı belirtilmedi.
- Bunu şu şekilde belirtiyoruz ;
- Create den tek farkı; form içinde request.post ile birlikte instance=ilgili todo yu parametre olarak alması ->
```py
      if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
```

todo <views.py> ->
```py
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.

def home(request):
    todos = Todo.objects.all()
    form = TodoForm()
    context = {
        "todos" : todos,
        "form" : form,
    }
    return render(request, 'todo/home.html', context)

def todo_create(request):
    form = TodoForm()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo:home')
        
    context = {
        "form" : form,
    }
    return render(request, 'todo/todo_add.html', context)

def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo:home')
    
    context ={
        "todo": todo,
        "form": form,
    }
    return render(request, 'todo/todo_update.html', context)
```


#### html/css güncellemesi;

- artık update template ine gelen ilgili todo nun verilerinde değişiklik yapıp update yapabiliyoruz.

- Görünümü biraz iyileştirmek için home.html de todolarımızı tablo şeklinde göstermek için aşağıdaki değişiklikleri yapıyoruz;

todo <home.html> ->

```html
{% extends 'todo/base.html' %} {% block content %}
<div class="container">
  <div>
    <form action="add/" method="post">
      {% csrf_token %} {{ form.as_p }}
      <input type="submit" value="Add" />
    </form>
  </div>

  <div>
    <table>
      <thead>
        <tr>
          <th>No</th>
          <th>Title</th>
          <th>Update</th>
          <th>Delet</th>
        </tr>
      </thead>
      <tbody>
        {% for todo in todos %}
        <tr>
          <td>{{ forloop.counter }}</td>
          <td>{{ todo.title }}</td>
          <td><button><a href="{% url 'update' todo.id %}" target="_blank">Update</a></button></td>
          <td><button><a href="#">Delete</a></button></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock content %}
```

#### html/css güncellemesi (update.html)

- update page deki görüntüyü iyileştirmek adına todo_update.html de todolarımızı tablo şeklinde göstermek için aşağıdaki değişiklikleri yapıyoruz;

todo <todo_update.html> ->

```html
{% extends 'todo/base.html' %} {% block content %}
<div class="update">
  <div class="update1">
    <h2>Todo Update</h2>
    <form action="" method="post">
      {% csrf_token %} {{ form.as_p }}
      <input type="submit" value="Update" />
    </form>
  </div>
</div>

{% endblock content %}
    
```

- ve bu class  verdiğimiz divlere style.css de css veriyoruz.

<static/todo/style.css> ->

```css
.navbar {
    background-color: cadetblue;
}

.container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    
}

.update{
    display: flex;
    justify-content: space-evenly;
    /* border: 1px solid black; */
}
.update1{
    display:inline;
    /* border: 1px solid red; */
}

```
- Dikkat!!
- Fakat css'deki bu değişiklikler hemen algılanmıyor. css dosyasının ismini değiştirince (tabi base.html'de de yeni ismini kullanıyoruz) algılanıyor.


### Delete

- app imizin views.py ına giderek delete view ini yazıyoruz.
- todo_delete view i de parametre olarak request ile bir de id alıyor çünkü hangi todo yu delete edeceğimi bilmesi gerekiyor. id yi de parametre olarak gönderince hangi todo üzerinde çalışılacağını bildiriyoruz.
- sonra Todo object leri arasından id si request ile todo nun id sine eşit olanı bir todo değişkenine tanımlıyoruz.
- sonra çektiğimiz bu todo yu context yapısı ile template imize gönderiyoruz.
- view ini yazıyoruz;
  
```py
def todo_delete(request, id):
    todo = Todo.objects.get(id=id)
    
    context = {
        "todo": todo
    }
    return render(request, 'todo/todo_delete.html', context)
```

todo <views.py> ->
```py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo
from .forms import TodoForm

def home(request):
    todos = Todo.objects.all()
    form = TodoForm()
    context = {
        'todos': todos,
        'form': form,
    }
    return render(request, 'todo/home.html', context)

def todo_create(request):
    form = TodoForm()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {
        "form": form,
    }
    return render(request, 'todo/todo_add.html', context)

def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {
        "todo": todo,
        "form": form,
    }
    return render(request, 'todo/todo_update.html',context)

def todo_delete(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        "todo": todo
    }
    return render(request, 'todo/todo_delete.html', context)
```

- urls.py da path ini tanımlıyoruz;

todo <urls.py> ->

```py	
from django.urls import path
from .views import (
    home,
    todo_create,
    todo_update,
    todo_delete,
)

urlpatterns = [
    path('', home, name='home'),
    path('add/', todo_create, name='add'),
    path('update/<int:id>', todo_update, name='update'),
    path('delete/<int:id>', todo_delete, name='delete'),
]
```

- template ini oluşturyoruz;

todo <todo_delete.html> ->
```html
{% extends 'todo/base.html' %} 
{% block content %}
<form action="" method="post">
  {% csrf_token %} 
  Are you sure you want to delete <span>{{ todo }}</span> ?
  <input type="submit" value="Delete" />
</form>
{% endblock content %}
```

- url satırında todo/delete/1 yazarak istek atınca bizi delete sayfasına 1 id li todo nun verileriyle birlikte gönderiyor.

- Şimdi home.html de todo larımızı a tag i ile delete url ine link verelim. Böylece adres satırına kendimiz delete/todonun id sini yazmak yerine todonun üzerinde tıklayınca bizi otomatik olarak delete/todo id si olarak o like yönlendirecek.
      <li><a href="{% url 'delete' todo.id %}" target="_blank">{{ todo }}</a></li>

todo <home.html> ->
```html
{% extends 'todo/base.html' %} {% block content %}
<div class="container">

  <div>
    <form action="add/" method="post">
      {% csrf_token %} {{ form.as_p }}
      <input type="submit" value="Add" />
    </form>
  </div>

  <div>
    <table>
      <thead>
        <tr>
          <th>No</th>
          <th>Title</th>
          <th>Update</th>
          <th>Delet</th>
        </tr>
      </thead>
      <tbody>
        {% for todo in todos %}
        <tr>
          <td>{{ forloop.counter }}</td>
          <td>{{ todo.title }}</td>
          <td><button><a href="{% url 'update' todo.id %}" target="_blank">Update</a></button></td>
          <td><button><a href="{% url 'delete' todo.id %}" target="_blank">Delete</a></button></td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

</div>
{% endblock content %}
```

- evet artık delete template imizde ilgili todo yu görüyoruz, fakat input buttonu ile delete edemiyoruz, çünkü view imizde post ile gelen request için ne yapılacağı belirtilmedi.
- Bunu şu şekilde belirtiyoruz ;
      if request.method == 'POST':
        todo.delete()
        return redirect('home')

todo <views.py> ->
```py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo
from .forms import TodoForm

def home(request):
    todos = Todo.objects.all()
    form = TodoForm()
    context = {
        'todos': todos,
        'form': form,
    }
    return render(request, 'todo/home.html', context)

def todo_create(request):
    form = TodoForm()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {
        "form": form,
    }
    return render(request, 'todo/todo_add.html', context)

def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {
        "todo": todo,
        "form": form,
    }
    return render(request, 'todo/todo_update.html',context)

def todo_delete(request, id):
    todo = Todo.objects.get(id=id)
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
    context = {
        "todo": todo
    }
    return render(request, 'todo/todo_delete.html', context)
```

#### html/css güncellemesi (delete.html)

- artık delete template inde todo'yu silmek için delete button'una bamamız yeterli

- delete page deki görüntüyü iyileştirmek adına todo_delete.html de todolarımızı tablo şeklinde göstermek için aşağıdaki değişiklikleri yapıyoruz;

todo <todo_delete.html> ->

```html
{% extends 'todo/base.html' %} {% block content %}
<div class="delete">
    <div class="delete1">
      <h2>Todo Delete</h2>
      <form action="" method="POST">
        {% csrf_token %}
        Are you sure to delete <span>{{todo}}</span> ?
        <input type="submit" value="Delete">
    </form>
    </div>
  </div>

{% endblock content %}
    
```

- ve bu class  verdiğimiz divlere style.css de css veriyoruz.

<static/todo/style.css> ->

```css
.navbar {
    background-color: cadetblue;
}

.container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    
}

.update{
    display: flex;
    justify-content: space-evenly;
    /* border: 1px solid black; */
}
.update1{
    display:inline;
    /* border: 1px solid red; */
}

.delete{
    display: flex;
    justify-content: space-evenly;
    /* border: 1px solid black; */
}
.delete1{
    text-align: center;
    display:inline;
    /* border: 1px solid red; */
}

```
- Dikkat!!
- Fakat css'deki bu değişiklikler hemen algılanmıyor. css dosyasının ismini değiştirince (tabi base.html'de de yeni ismini kullanıyoruz) algılanıyor.



### Messages

- delete kısmı da bitti. Şimdi mesaj ekleyeceğiz;
- views.py a gidip messages ı import ediyoruz, create view ine form.save() den sonra, todo_update view ine form.save() den sonra, bir de delete view ine todo.delete() den sonraya ekliyoruz;

```py
from django.contrib import messages

    messages.success(request, 'Todo created successfully.')
    
    messages.success(request, 'Todo updated successfully')

    messages.warning(request, 'Todo deleted!')

```

- Şimdi buralara eklememiz yetmiyor, base.html e gidiyoruz, ve bu mesajların nerede görünmesini istiyorsak oraya (navbar ın altına content lerin üzerine) şu yapıyı ekliyoruz;

todo <base.html> ->

```htlm
    <!-- messages -->
    {% if messages %} 
        {% for message in messages %} 
            {% if message.tags == "warning" %}
                <div id="warning" class="message">{{ message }}</div>
            {% else %}
                <div id="success" class="message">{{ message }}</div>
            {% endif %} 
        {% endfor %} 
    {% endif %} 
```

- evet yazdık mesajlar çalışıyor. Şimdi onlara css vereceğiz.

<style.css> ->
```css
#warning {
    background-color: lightcoral;
    color: aliceblue;
    margin: auto;
    width: 40%;
    height: 30%;
    text-align: center;
}
#success {
    background-color: darkgreen;
    color: rgb(231, 200, 158);
    margin: auto;
    width: 40%;
    height: 30%;
    text-align: center;
}
```

### javascript code ekleme (timeout.js)

- mesaj geldikten sonra gitmiyor, belli bir süre sonra kaybolması için; js kalsöründe timeout.js dosyası oluşturup içerisine şu kodu yazıyoruz;

```js
let element = document.querySelector('.message')

setTimeout(function() {
    element.style.display = 'none';
}, 3000);
```

- hemen arkasından base.html de body nin en alt kısmında timeout.js i import ediyoruz.

todo <base.html> ->
```html
<script src="{% static 'todo/js/timeout.js' %}"></script>
```

- Tekrar server ımızı çalıştırıyoruz. Deniyoruz, çalıştığını görüyoruz.


##### Frontend style geliştirme (html/css)

- En son olarak home.html, update kısmı, ve son olarak css kısmını şu şekilde yazarak son haline getiriyoruz. -> 

todo <home.html> ->

```html	
{% extends 'todo/base.html' %}
{% block content %}
<div class="container pt-4">
  <div class="row mt-2 p-0">

    <div class="col-lg-4 mx-auto p-0 shadow">
      <div class="alert alert-warning text-center">
        <h2>Add ToDo</h2>
      </div>
    <div class="p-4">
      <form action="add/" method="POST">
          {% csrf_token%} {{form.as_p}}
          <hr>
          <input type="submit" value="ADD" class="btn btn-success">
      </form>
    </div>
  </div>

  <div class="col">
    <div class="border">
      {% if todos|length == 0 %}
      <div class="p-4">
        <br>
        <br>
        <div class="alert alert-danger text-center">
          <p class="" style="font-size: 30px;">ToDo Lists</p>
        </div>
        <br>
        <br>
      </div>
      {%else%}
      <div class="p-2">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>No</th>
              <th>Title</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Delete</th>
              <th>Update</th>
            </tr>
          </thead>
          <tbody>
            {% for todo in todos%}
              <tr>
                <td>{{forloop.counter}}</td>
                <td>{{todo.title}}</td>
                {% if todo.status == 'C'%}
                  <td>
                    ✅
                  </td>
                {% elif todo.status == 'I'%}
                  <td>
                    🚧
                  </td>
                {% elif todo.status == 'P'%}
                  <td>
                    💤
                  </td>
                {%endif%}
                <td>
                  {% if todo.priority == '1'%}
                    1️⃣
                  {%elif todo.priority == '2'%}
                    2️⃣
                  {%elif todo.priority == '3'%}
                    3️⃣
                  {%elif todo.priority == '4'%}
                    4️⃣
                  {%elif todo.priority == '5'%}
                    5️⃣
                  {%endif%}
                </td>
                <td>
                  <a href="{% url 'delete' todo.id %}" target="_blank" title="Delete" class="">🗑️</a> 
                </td>
                <td>
                  <a href="{% url 'update' todo.id %}" target="_blank"  class="">⚙️</a> 
                </td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {%endif%}
    </div>
  </div>
</div>
{% endblock content %}    
```


todo <update.html> ->

```html	
{% extends 'todo/base.html' %}
{% block content %}
<div class="container pt-4">
  <div class="col-lg-6 mx-auto p-0 shadow">

      <div class="alert alert-warning text-center">
          <h2>Update Todo</h2>
      </div>
      
      <div class="p-4 d-flex align-items-center">
          <form action="" method="post">
              {% csrf_token %}
              {{ form.as_p }}
              <input type="submit" value="Update" class="btn btn-success" />
              <a href="{% url 'home' %}"><input type="button" value="CANCEL" class="btn btn-primary"></a>
          </form>
      </div>
      
  </div>
</div> 
{% endblock content %}
```


todo <delete.html> ->

```html	
{% extends 'todo/base.html' %}

{% block content %}
<div class="container pt-4">
  <div class="col-lg-6 mx-auto p-0 shadow">
    <div class="alert alert-warning text-center">
      <h2>Delete Todo</h2>
    </div>
    <div class="p-4 d-flex align-items-center">
      <form action="" method="post">
        {% csrf_token %}
        Are you sure delete <span>{{ todo }}</span> ?
        <input type="submit" value="Delete" class="btn btn-danger" />
        <a href="{% url 'home' %}"><input type="button" value="CANCEL" class="btn btn-primary"></a>
      </form>
    </div>  
  </div>
</div>
{% endblock content %}
```	



<style.css> ->

```css	
.navbar {
    background-color: cadetblue;
}

.container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

.update{
    display: flex;
    justify-content: space-evenly;
    /* border: 1px solid black; */
}

.update1{
    display:inline;
    /* border: 1px solid red; */
}

span{
    background-color: yellow;
}

#warning {
    background-color: lightcoral;
    color: aliceblue;
    margin: auto;
    width: 40%;
    height: 30%;
    text-align: center;
}

#success {
    background-color: darkgreen;
    color: rgb(231, 200, 158);
    margin: auto;
    width: 40%;
    height: 30%;
    text-align: center;
}

body {
    background-image: url(https://cdn.pixabay.com/photo/2017/01/24/03/53/plant-2004483__480.jpg);
    background-size: cover;
    background-repeat: no-repeat;
}
textarea {
    max-width: 100%;
}
```


- Her nekadar kullanmıyor olsak da add template inin son hali;

todo <todo_add.html> ->

```html
{% extends 'todo/base.html' %} 
{% block content %}
<div class="container pt-4">
    <div class="col-lg-6 mx-auto p-0 shadow">
      <div class="alert alert-warning text-center">
        <h2>Add Todo</h2>
      </div>
  
      <div class="p-4 d-flex align-items-center">
        <form action="" method="post">
          {% csrf_token %} {{ form.as_p }}
          <input type="submit" value="Add" class="btn btn-success" />
          <a href="{% url 'home' %}"
            ><input type="button" value="CANCEL" class="btn btn-primary"
          /></a>
        </form>
      </div>
    </div>
  </div>
{% endblock content %}

```


### Authentication-1 ekleme;

- Authentication-1 -> pasword_change, password_reset...
- User modeli genişletiliyor.

- Bu Todo projesinin üzerine Authentication-1 ekleniyor. Devamı Readme_user.md ' de 
