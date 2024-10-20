
### Todo_App üzerine user app ekleme;

Project_Django_Templates_Todo_App_CH-11 'üzerine authentication-1 ekliyoruz.

- FB views ile yazılmış Todo_App üzerine user app ekleme;

- base.html'de yeni bir navbar oluşturuyoruz;

- Önce Todo app'imizin navbar'ına bir condition yazalım ve eğer user authenticate ise şunları göstersin, değil ise şunları şeklinde linkler koyalım.
- authenticate ise  ->  logout, password_change, 


- authenticate değil ise  ->  register, login, password_reset (forgot my password), 


todo/base.html
```py
    <!-- navbar start -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <!-- Sol tarafa logo ve başlık -->
            <a class="navbar-brand" href="/">
                <img src="{% static 'todo/images/cw_logo.png' %}" alt="Hi!" width="45" height="45">
                Umit_Developer Todo App
            </a>
            
            <!-- Navbar'ı mobilde açılabilir yapmak için buton -->
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
    
            <!-- Sağ tarafa link butonları -->
            {% if user.is_authenticated %}
            <div class="collapse navbar-collapse" id="navbarNav">
                
                <ul class="navbar-nav me-auto">
                    
                    {% if request.user.is_superuser %}
                    
                    <li class="nav-item">
                        <a class="nav-link btn btn-outline-secondary ms-2" href="/admin" target="_blank">Admin Panel</a>
                    </li>                  
                    
                    {% endif %}

                </ul>

                <ul class="navbar-nav ms-auto">
                    
                    <li class="nav-item">
                        <a class="nav-link text-warning" href="#">welcome {{ user.username }}</a>
                    </li>
                    
                    <li class="nav-item">
                        <a href="#" class="nav-link btn btn-outline-secondary me-2" onclick="document.getElementById('logout-form').submit();">
                            Logout
                        </a>
                    
                        <form id="logout-form" method="POST" action="{% url 'logout' %}" style="display: none;">
                            {% csrf_token %}
                        </form>
                    </li>   
                       
                    <li class="nav-item">
                        <a class="nav-link btn btn-outline-secondary me-2" href="#">Password Change</a>
                    </li>
                </ul>
            </div>
            {% else %}
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link btn btn-outline-secondary me-2" href="{% url 'register' %}">Register</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-outline-secondary me-2" href="{% url 'login' %}">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-outline-secondary" href="#">Forgot my password</a>
                    </li>
                </ul>
            </div>
            {% endif %}

        </div>
    </nav>
```


- Kullanıcı register olup login olacak. Tekrar login olduğunda da oluşturmuş olduğu todo'lar görünecek. Başkalarının todo'larını göremeyecek, başkaları da onunkileri göremeyecek.

- INSTALLED_APPS'deki 'django.contrib.auth' app'inin urls'ini alıp, kendi projenin urls'ine koyarsan default urls'lerine erişim sağlayabiliriz.

main/urls.py
```py
...
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]
```

- http://127.0.0.1:8000/accounts/  endpointine giderek bize vermiş olduğu endpointleri gördük. Ancak bunlara gitmek istediğimizde bize 'template yok' hatası veriyor.

- django, kayıt olmuş kullanıcılar için login/logout/password işlemlerini yapıyor.

- Burada bakıyoruz ki registration endpoint'i yok. Yani django default olarak url'den kullanıcı kaydı almıyor.
- Bunu biz manuel olarak, yani registration view ve template'i oluşturarak kendimiz url'den kullanıcı kaydı alacağız.
- Bunun için bir users app'i oluşturup, register için bir view yazıp onu da url'den tetikleyerek bir template'e yönlendireceğiz.

- Şimdi biz bu template'leri oluşturacağız.
- Bunları oluştururken klasör yapısı ve template name yapısına dikkate edeceğiz. Bizden istedği gibi yapılandırıp, isimlendireceğiz.

- Tüm bu işlemler için yeni bir app (users) oluşturuyoruz.

```bash
- py manage.py startapp users
```

settings.py
```py
INSTALLED_APPS = [
    ...
    'django.contrib.auth',
    ...
    # myApps
    'todo',
    'users',
]
```

- urls configurations yapalım;

main/urls.py
```py
...
urlpatterns = [
    ...
    path('users/', include('users.urls')),
]
```


- users app'inin içinde urls.py create edelim;

users/urls.py
```py
from django.urls import path, include
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]
```


- users app'imizin içinde templates/registration  klasörlerimizi oluşturuyoruz.
    templates/registration


#### login

- login template'ini oluşturalım (template name önemli, bizden istediği şekilde bir isim olması gerekiyor.);

users/templates/registration/login.html
```html
{% extends 'todo/base.html' %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Login">
    </form>
{% endblock content %}
```

- test ettik, 
    http://127.0.0.1:8000/accounts/login/

  endpointine istek attığımız zaman karşımıza bizim yazdığımız login template'i geldi.
Bu template sayesinde username ve password ile giriş yapabildik.

- Ancak django default olarak login olduğumuzda bizi profile/ sayfasına yönlendiriyor. 
- Bunun önüne geçmek için settings.py'da nereye gitmesini istiyorsak belirtiyoruz;

settings.py
```py
# LOGIN_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "home"
# LOGIN_REDIRECT_URL = "todo:home"
```
  


#### register

- Şimdi gelelim register işlemini yapmaya
- views.py'a gidip register view'i yazalım;

- views.py'da register view'inde temel olarak iki işlem var;
  - 1. Gelen istek get ise boş bir register formu göndermek,
  - 2. Gelen istek post ise ve formun içinde bilgiler varsa, formdaki bilgileri alıp db'ye kaydetmek.

- Eğer request post ise kullanıcıya gönderdiğimiz default UserCreationForm(request.POST) içindeki doldurulmuş verilerle birlikte yakalayıp,
  - eğer form valid ise save et!
  
        def register(request):
          if request.method == 'POST':
              form = UserCreationForm(request.POST)
              if form.is_valid():
                 form.save()
  
  - formu (içindeki user verileri ile) kaydettik.
  - şimdi bu kullanıcıyı authenticate (login) et. Bunun için formun içinden username ve password'ü (password1 veya password2 şeklinde alınıyor.) almamız lazım.
     
           username = form.cleaned_data['username']
           password = form.cleaned_data['password1']

  - aldığımız usernam ve password'ü, authenticate() methoduna/fonksiyonuna parametre olarak göndererek user'ı authenticate ediyoruz. 
   
           from django.contrib.auth import authenticate
    
           user = authenticate(username=username, password=password)
  
  - Kullanıcımız artık authenticate olmuş durumda. Şimdi onu login ediyoruz;

           from django.contrib.auth import login
    
           login(request, user)
  - sonunda da kullanıcıyı todo:home page'e yönlendir.
  
- Ancak eğer request post değil ise yani get ise o zaman ona sadece formu boş UserCreationForm() döndür. register.html'i döndür.

    else:
        form = UserCreationForm()



users/views.py
```py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
    
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

```

- register template'imizi, users/templates/registartion/ yasısının altında create edelim;

users/templates/registartion/register.html
```html
{% extends 'todo/base.html' %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Login">
    </form>
{% endblock content %}
```

- test ettik çalışıyor.


#### logout

- logout yapabilmemiz için; 
  - login olmuş olmamız,
  - form içinde csrf token ile post isteği atmamız gerekiyor.
  - Şu şekilde yapıyoruz;

- navbardaki logout linki -> 

todo/base.html
```html
...
<!-- navbar -->
    <li class="nav-item">
        <form method="POST" action="{% url 'logout' %}">
            {% csrf_token %}
            <button type="submit" class="nav-link btn btn-outline-secondary me-2" style="border: none; background: none;">
                Logout
            </button>
        </form>
    </li>
```

- Ancak django default olarak logout olduğumuzda bizi profile/ sayfasına yönlendiriyor. 
- Bunun önüne geçmek için settings.py'da nereye gitmesini istiyorsak belirtiyoruz;

settings.py
```py
# LOGOUT_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "home"
# LOGOUT_REDIRECT_URL = "todo:home"
```


#### default User modelini genişletelim, profile ekleyelim;

#### genişletilmiş User modeline göre register için form-view-template 

#### register (genişletilmiş user modeli ile)
- users/models.py'da UserProfile(models.Model) oluşturup default User modeli ile OneToOne ilişkilendiriyoruz.

users/models.py
```py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'profile_pics/')
    bio = models.TimeField()
    
    def __str__(self):
        return self.user.username
```


- modelimizde image field kullandığımız için pillow yüklememiz gerekiyor.

```bash
- pip install Pillow
- pip freeze > requirements.txt
```

- modelimizde image field kullandığımız için mediaların yolunu settings.py'da ve de main/urls.py'da belirtmemiz gerekiyor.

settings.py
```py
# Media dosyaları için ayarlar
MEDIA_URL = '/media/'  # Tarayıcıdan erişim için URL
MEDIA_ROOT = BASE_DIR / 'media'  # Yüklenen dosyaların depolanacağı yer
```

main/urls.py
```py
...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
]

if settings.DEBUG:  # Yalnızca development modda çalışacak
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- DİKKAT! -> media file olarak image kullanıldığı için view'de form içinde parametre olarak request.FILES ve de template'te form içinde enctype="multipart/form-data" kullanmak unutulmamalı.

- yeni bir model oluşturduğumuz için migrations, migrate yapalım;

```bash
- py manage.py makemigrations
- py manage.py migrate
```

- modelimize admin panelden erişebilmek için admin.py'da register edelim;
  
admin.py
```py
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)
```

- Hazırladığımız bu modele göre user bilgilerini kullanıcıdan alacağımız formu hazırlayalım;

- register için bir UserProfile modeli yazıp, bu model ile biri default User ve diğeri extra fieldlardan oluşan iki form hazırlayıp, view'de logic'ini kurup, urls'de endpointini yazıp, kullanacağız.

- users/forms.py create ediyoruz.
- ilk formumuzu yazıyoruz;
- Bu formun user fieldını kullanmıyoruz, user'ı views'de ekleyeceğiz.
- Burada sadece yeni oluşturacağımız user'ın userProfile'ını belirlemek.
- Eğer formun user field'ını kullansaydık, mevcut olan userlar arasından seçim yaptırmak zorunda kalacaktık.

        class UserProfileForm(forms.ModelForm):
            class Meta:
                model = UserProfile
                fields = ('profile_pic', 'bio')

- ikinci formumuzu da yazalım;
- Kullanıcı register olurken email verisi de girsin istiyoruz.
- Bunun için hazır UserCreationForm'u inherit edip, email ekleyip register olurken bu formu kullanacağız.  
- Bu ikinci formumuz UserForm()'u UserCreationForm'dan inherit ederek yazıyoruz. 
- Burada ekstra olarak user'dan email bilgisi de isteyeceğiz. (Normalde default olarak username ve password istiyor.)
        
        class UserForm(UserCreationForm):
            class Meta:
                model = User
                fields = ('username', 'email',)



users/forms.py
```py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'bio')
        # exclude = ('user',) 
        # Bu formun user fieldını kullanmıyoruz, user'ı views'de ekleyeceğiz.
        # Burada sadece yeni oluşturacağımız user'ın userProfile'ını belirlemek.
        # Eğer formun user field'ını kullansaydık, mevcut olan userlar arasından
        # seçim yaptırmak zorunda kalacaktık.


# Kullanıcıdan email verisi de isteyelim:
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)
        # password otomatik olarak istiyor, o yüzden belirtmiyoruz.
```

- modelimizi ve formlarımız yazdık, şimdi bu formlara göre register view'imizi yazalım;

- Önceki yani default model ve UserCreation ile oluşturduğumuz register view'imizi yoruma alalım. Yeni register view'imizi yazalım;

users/views.py
```py
...
from .forms import (
    UserProfileForm, 
    UserForm,
)

## Genişletilmiş User modeli ile register: UserCreationForm()'un genişletilerek email eklenmiş hali ile oluşturduğumuz view (username, email, password)
def register(request):
    form_user = UserForm()
    form_profile = UserProfileForm()
    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_profile = UserProfileForm(request.POST, request.FILES) # dosyaları almak için
        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            
            return redirect('home')
    
    context = {
        'form_user': form_user,
        'form_profile': form_profile
    }
    return render(request, 'registration/register.html', context)
```
 

- endpointimiz zaten hazırdı;

```py
from django.urls import path, include
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]
```

- template'imizde de değişiklik yapıyoruz;

users/templates/registration/register.html
```html
{% extends 'todo/base.html' %}

{% block content %}

<h1>Registration Page</h1>

    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form_user.as_p }}
        {{ form_profile.as_p }}
        <input type="submit" value="Register">
    </form>

{% endblock content %}
```
#### Buradan sonraki login ve logout kendi yazdığımız, login ve logout 'tur. 
#### Yukarıdakiler ise accounts/ endpointinin bize sağladığı view ve endpointleri kullanarak sadece login için template, logout için ise navbar'da post ile csrf token ile istek attığımız submit button 'dır.

#### login (kendi yazdığımız login, genişletilmiş user modeli ile)

- Biz daha önce login için view yazmamış, sadece default template_name ile template oluşturmuştuk. 
- Hatta url bile belirlememiş, default accounts/login endpointini kullanmıştık.

- Şimdi views.py'da login view'i yazıyoruz,
- default form olan AuthenticationForm()' u import edip, kullanıyoruz,
    from django.contrib.auth.forms import (
          AuthenticationForm,
    )

- parametre olarak request, data=request.POST or None veriyoruz.

    form = AuthenticationForm(request, data=request.POST or None)

- eğer form valid ise; form'un içinden user'ı al;
  - burada  AuthenticationForm(request, data=request.POST or None)  içinden user'ı .get_user() ile aldık.

- sonra login, redirect...

users/views.py
```py
from django.contrib.auth.forms import (
    ...
    AuthenticationForm,
)

...
def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    return render(request, 'registration/login.html', {'form':form})
```


- template'ini yazalım,
- var olan login.html'i güncelleyelim;

users/templates/registration/login.html
```html 
{% extends 'todo/base.html' %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Login">
    </form>
{% endblock content %}
``` 


- urls'ini yazalım, 

users/urls.py
```py
...
from .views import (
    register,
    user_login,
)

urlpatterns = [
    ...    
    path('login/', user_login, name='user_login'),
]
```

- navbardaki link'in href'ini de {% url 'user_login' %} olarak url'deki name'iyle değiştiriyoruz.


#### logout (kendi yazdığımız logout)

- bunun için view'e uğramadan urls.py'da default view'ini import ederek kullanacağız.

users/urls.py
```py
...
from django.contrib.auth.views import LogoutView

urlpatterns = [
    ...
    path('logouts/', LogoutView.as_view(), name='user_logout'),
]
```

- navbardaki link'in href'ini de {% url 'user_logout' %} olarak url'deki name'iyle değiştiriyoruz.


- Artık accounts/  endpointinin değil de kendi yazdığımız login, logout view, template ve endpointlerini kullanıyoruz.
- register'ı zaten biz yazmıştık. 


### Todo bölümünde her user kendi todo'larını görsün, create, update, delete etsin;

- todo app'imizdeki Todo modelimiz/tablomuz 'un bir user field'ı yok.
- Todo modelimize user field'ı ekleyerek, default User modeli ile ManyToOne (ForeignKey) bir ilişki kuracağız.

- blank=True dememizin nedeni; user'ı formda değil de view'de ekleyeceğimiz için, formu doldururken userdan user bilgisi istemesin diye.

todo/models.py
```py
...
from django.contrib.auth.models import User

class Todo(models.Model):
    ...
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    ...
```

- TodoForm'da user field'ını formda gösterme, biz o fieldı views'de ekleyeceğiz diyoruz.

todo/forms.py
```py
...

class TodoForm(forms.ModelForm):
    class Meta:
        ...
        exclude = ('user',)
```

```bash
- py manage.py makemigrations
- py manage.py migrate
```

#### List

- todo/views.py'da home view'inde boş bir liste tanımlıyoruz ve bu listenin içini bir condition ile authenticate olmuş user ise şöyle dolduracağız, authenticate değil ise böyle dolduracağız;
  
    todos = []
    if request.user.is_authenticated():
        todos = Todo.objects.flter(user=request.user)

- eğer user authenticate ise, kendi todolarını göster!

todo/views.py
```py
def home(request):
    todos = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            todos = Todo.objects.all().order_by('priority')
        else:
            todos = Todo.objects.filter(user=request.user).order_by('priority')
    form = TodoForm()
    context = {
        "todos" : todos,
        "form" : form,
    } 
    return render(request, 'todo/home.html', context)
```

- test ettik, şimdilik admin panelden todolardan birinin user'ını admin olarak değiştirdik ve home page'de sadece adminin kendisinin todolarını gördük.
- Bundan sonra create view'de todo create edilirken user'ı ekleyeceğimiz için bu iş otomatik olacak.

- Ayrıca user.is_superuser ise tüm todoları görsün,
- Bir de template'te o todoların kimlere ait olduğunu gösteren bir de sütun olsun diye template'de de bir değişiklik yapıyoruz.

todo/home.html
```html
...
    <th>Update</th>
    
    {% if user.is_superuser %}
    <th>Todo Owner</th>
    {% endif %}
...

    <td>
      <a href="{% url 'update' todo.id %}" target="_blank"  class="text-decoration-none">⚙️</a> 
    </td>
    {% if user.is_superuser %}
    <td>
      {{ todo.user }}
    </td>
    {% endif %}
...
```


#### @login_required() decorator kullanımı;

- Login olmayan user create, update, delete view lerini kullanamasın diye  @login_required() decorator kullanıyoruz. Tabi import da ediyoruz.
    from django.contrib.auth.decorators import login_required

    @login_required()

- İçine parametre olarak da (login_url = 'user_login') veriyoruz ki; eğer view'i kullanmak isterse login page'imize yönlendirelim diye.

    @login_required(login_url = 'user_login')

todo/views.py
```py
...
from django.contrib.auth.decorators import login_required

...

@login_required(login_url = 'user_login')
def todo_create(request):
    form = TodoForm()
    
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo created successfully.')

            return redirect('home')
    
    context = {
        "form" : form
    }
    return render(request, 'todo/todo_add.html', context)
```

- test ediyoruz, login olmadan bir todo create etmeye çalışınca bizi login sayfasına yönlendiriyor.

- Bu decorator'ü update ve delete viewlerinde de kullanıyoruz. 

todo/views.py
```py
...
@login_required(login_url = 'user_login')
def todo_update(request, id):

...

@login_required(login_url = 'user_login')
def todo_delete(request, id):

```


#### Create

- todo_create view'de form.is_valid()'den sonra formu save ediyor. 
- Biz burada araya girip;
  - formu bir değişkene tanımlıyoruz, ve commite=False ile bekletiyoruz,
  - hemen sonra  todo.user = request.user ile todo'ya request.user'ı tanımlayıp,
  - formdan gelen todo'yu user'ını da ekleyerek kaydediyoruz. todo.save()

todo/views.py
```py
...
def todo_create(request):
    form = TodoForm()
    
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            
            messages.success(request, 'Todo created successfully.')

            return redirect('home')
    
    context = {
        "form" : form
    }
    return render(request, 'todo/todo_add.html', context)
```

- test ediyoruz, çalıştı.


##### Password_Change, Password_Change_Done

- password_change.html  oluşturacağız, django password_change için kendi administration sayfasında (accounts/password_change) kendi hazır template ine yönlendiriyor. 
- Biz bu template e yönlenmek istemiyoruz. Kendi template imizi koyup render etmek istiyoruz. 
- Ancak bu form ve view bizim için hazır biz sadece template ini kendimize göre değiştireceğiz.

- Biz password_change.html oluşturacağız, urls.py da 
```py
  from django.contrib.auth import views as auth_views
```   
import edip PasswordChangeView i çağırıp .as_view(template_name="registration/password_change.html")    şeklinde as_view içerisine kendi yazdığımız template i koyarak overrire edeceğiz. 
- Normalde bunun default u neymiş dokümandan bakarsak; default unun password_change_form.html olduğunu görürüz. Burada onu değiştiriyoruz. 
- Aslında bu işlemleri de yapmayabiliriz, sadece bir template (dokümanda geçen ismiyle yani register/password_change_form.html) ekleyerek de bu işlemleri yapabiliriz ancak önce bunu bi görelim sonra bu customization u yapmadan da bu password_change view ini gösterebiliriz ona da bakacağız.


- 1. Yöntem; urls.py da path ve import ettiğimiz PasswordChangeView'i kullanarak kendi custom "password_change" ve "password_change_done" template'imizi yazmak;
- Biz password_change için bir view yazmadık, urls.py da görüldüğü gibi auth.views deki PasswordChangeView ini alıp, onu customize ettik, as_view içerisindeki template name parametresini değiştirmişiz. (default olarak register/password_change_form.html olması gereken template ismini register/password_change.html olarak customize ettik.)

- Özetle djangonun bize otomatik default olarak verdiği password_change view inde customization yapmak istiyoruz, bunun default template ini değiştirmek istiyoruz ki bizi kendi template imize yönlendirsin.

- Burada kendimiz "password_change/" şeklinde custom bir end point belirleyebiliyoruz. Bu end pointe istek geldiğinde beni djangonun vermiş olduğu auth_views.PasswordChangeView ine yönlendir demişiz ama as_view in içerisine şunu yazarak -> template_name="registration/password_change.html" djangonun kullandığı default template yerine benim hazırladığım registration içerisindeki password_change.html i kullan demişiz. 

- Djangonun verdiği bütün view leri bu şekilde customize edebiliriz.

users/urls.py
```py
...
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"), name="password_change"),
]
```

- Şimdi registration içerisinde custom "password_change.html" oluşturuyoruz.

users/templates/registration/password_change.html
```html
<h1>Password Change</h1>

<form action="" method="post">

    {% csrf_token %}

    {{ form.as_p }}

    <input type="submit" value="Update">
    
</form>
```

- Evet artık biz djangonun bize vermiş olduğu "password_change" sayfasının (accounts/password_change/) yerine kendi template imizi render ediyoruz. Bu sayfaya erişebilmek için tabiki login olmamız gerekir. Eğer logout isek otomatik olarak login sayfasına yönlendiriyor.

- test ediyouz, "password_change/" ile password ümüzü değiştirebiliyoruz. Ancak hemen sonra django bizi "accounts/password_change/done/" isimli bir sayfaya yönlendirdi. Ancak biz zaten buraya yönlenmesini değil de kendi sayfamıza yönlendirilsin istiyoruz. 

- Peki bunu nasıl yapacağız? 
- registration klasörü altında dokümanda da belirtildiği isim "password_change_done.html" ile template oluşturursak eğer, password_change 'den sonra bizim oluşturduğumuz template render edilecektir. 

users/templates/registration/password_change_done.html
```html
<h1>Password change successful</h1>
<p>Your password was changed.</p>
<a href="{% url 'home' %}"><input type="submit" value="Home"></a>
```

- test ettik ama yine django kendi default password_change_done.html template'ini göstermeye çalışıyor, bizim customize ettiğimizi göstermiyor. Neden?
- django template'leri yukarıda itibaren okumaya başlıyor ve bizim yazdığımız custom template'ten önce aynı isimde kendi default template'ini bulunca onu render etmeye çalışıyor. Sıralamada geride kalıyoruz, settings.py da INSTALLED_APPS kısımında admin app'i en yukarıda olduğundan bu sorunla karşılaşıyoruz.  Bunu nasıl aşacağız?
- settings.py'da INSTALLED_APPS'de kendi user_app'imizi admin app'inin üzerine taşırsak aynı isimdeki template'lerden bizim yazdığımızı render edecektir. 

settings.py
```py
INSTALLED_APPS = [
    # myApps
    'users',
    ...,
]
```

- test ettik çalıştı.

- 2. Yöntem; urls.py da path ve import ettiğimiz PasswordChangeView'i kullanmadan kendi custom "password_change" ve "password_change_done" template'imizi yazmak;
- Ya da sadece dokümanda geçtiği şekliyle yani;
 - "register/password_change_form.html" olarak registration klasörü altında bir html oluşturursak,
 - "register/password_change_done.html" olarak registration klasörü altında bir html oluşturursak,
 - Burada önemli olan husus template isimlerini değiştiremeyiz, dokümanda belirtildiği gibi kullanmalıyız.
 - yine, INSTALLED_APPS'deki user app'imizi, admin app'inin üzerine taşırsak,
 - urls.py'da PasswordChangeView'i render ederek template_name'ini değiştrmeye gerek kalmadan da 
 - kendi template'lerimizin render edilmesini sağlayabiliriz.


- Bundan sonra biz template'leri override ederken 2. yöntem üzerinden gideceğiz, 
- çünkü daha kolay, 
- app'imiz en üstte ve sadece kendi custom template'lerimize isim verirken djangonun default template'leriyle aynı isimde olmalarına dikkat edeceğiz o kadar.


##### Password Reset
- password_reset kullanabilmesi için user'ın aktif olması, login olmuş olması gerekir.
- django "/accounts/password_reset/" url'i ile bize default bir page sunuyor. Fakat biz bunu customize edeceğiz kendi page'imizi oluşturacağız.
- Biz app'imizi admin'in önüne aldığımız için, default template'in name'i (password_reset_form.html) ile aynı name'de olan kendi template'imizi oluşturup, djangonun bizimkini render etmesini sağlıyoruz.
- dokümanda yazdığı gibi default template name inde  "password_reset_form.html" oluşturuyoruz.

users/templates/registration/password_reset_form.html
```html
<h1>Password Reset</h1>

<form action="" method="post">

    {% csrf_token %}

    {{ form.as_p }}

    <input type="submit" value="Reset">
    
    <input type="hidden" value="{{ next }}" name="next">

</form>

```

- test ediyoruz, evet çalıştı. "/accounts/password_reset/" url'inden artık bizim custom template'imiz render ediliyor.

- Bundan sonra biz buraya mail adresimizi girdiğimiz zaman bize bir tane mail gönderecek, burada djangonun development için arkada set ettiği console backend diye bir email backend i var. Consolda bize email in bir dummy'sini gösteriyor.
  
###### Adjust a mail backend for development (Console backend):
    Geliştirme için bir posta arka ucunu ayarlayın

- Çalışan projede SMTP ayarları yapılarak gerçek zamanlı e-posta gönderimi ile sağlanıyor. Ancak development ortamında bu şekilde çalışılıyor.
 
(Instead of sending out real emails the console backend just writes the emails that would be sent to the standard output. By default, the console backend writes to stdout. You can use a different stream-like object by providing the stream keyword argument when constructing the connection.)

Konsol arka ucu, gerçek e-postalar göndermek yerine, standart çıktıya gönderilecek e-postaları yazar. Varsayılan olarak, konsol arka ucu stdout'a yazar. Bağlantıyı oluştururken akış anahtar sözcüğü argümanını sağlayarak akışa benzer farklı bir nesne kullanabilirsiniz.

(To specify this backend, put the following in your settings:)
Bu arka ucu belirtmek için settings.py a aşağıdakileri koyun:

```py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

- dokümandan console backend e gidiyoruz;
  
https://docs.djangoproject.com/en/4.1/topics/email/

şu ayarı settings.py a yazmamız gerekiyor:

<settings.py> ->

```py
# for password_reset email dummy;
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

```

- Bir de önemli olan husus password reset yapacak user ın kayıtlı e-mail inin olması gerekiyor. 

###### password_reset_done
- Artık "password_reset" template inde e postayı girip reset'e tıkladığımızda bizi yönlendirdiği sayfayı da dokümandan template ismi ile registration klasörü altında oluşturup kendi template imizi yazıyoruz;
  
users/templates/registration/password_reset_done.html
```html
<h1>Password reset sent</h1>
<p>We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.</p>

<p>If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder.</p>
```

###### password_reset_confirm
- consol umuza gelen dummy email ine tıkladığımızda default olarak gelen sayfayı da yine kendimizin oluşturduğu sayfaya yönlendirmek için default name i olan password_reset_confirm.html ile kendi template imizi yazıyoruz.
  
users/templates/registration/password_reset_confirm.html
```html
<h1>Password Reset Confirm Enter new password</h1>
<p>Please enter your new password twice so we can verify you typed it in correctly.</p>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Change my password">
</form>
```

###### password_reset_complete 
- password ümüzü yeniledikten sonra gelen sayfa ise default olarak password_reset_complete.html ve biz onun yerine aynı isimle kendimiz oluşturup aşağıdaki kodları yazıyoruz.
- login page'e yönlendiriyoruz.

users/templates/registration/password_reset_complete.html
```html
<h1>Password reset complete</h1>
<p>Your password has been set. You may go ahead and log in now.</p>
<a href="{% url 'login' %}">Login</a> 
```




#### modelde is_done (tamamlandı) fieldı ekleyip, template'te gösterip, durumunu değiştiren bir view yazıp, tamamlanan todoların sayısını gösterme;

- modele is_done (tamamlandı) fieldı ekliyoruz;
- template'imizde status field'ından önce bir sütun oluşturup oraya yerleştiriyoruz.

todo/templates/todo/home.html
```html
...
  <th>Is_Done?</th>
...
  {% if todo.is_done == True %}
        <td>
          ✅
        </td>
      {% else %}
        <td>
          💤
        </td>
      {% endif %}
...
```

- Bu fieldın durumunu mouse ile tıklandığında değiştirelim
- views.py'da bir view yazalım;

todo/views.py
```py
def is_completed(request, id):
    todo = Todo.objects.get(id=id)
    if request.user == todo.user:
        todo.is_done = not(todo.is_done)
        messages.success(request, 'Todo is done successfully')
    else:
        messages.warning(request, 'Not authorized for this Todo!')
    todo.save()
    return redirect('home')
    
```

- bu view'i tetikleyen urls.py'da endpoint yazalım;

todo/urls.py
```py
from .views import (
  ...
  is_completed,
)
urlpatterns = [
    ...
    path('isdone/<int:id>', is_completed, name='done'),
    ...
]
```

- home.html'de is_done field'ımızın gösterildiği kısma a tag'i ile link veriyoruz,

todo/tepmlates/todo/home.html
```html
    ...
                {% if todo.is_done == True %}
                  <td>
                    <a href="{% url 'done' todo.id %}">✅</a>
                  </td>
                {% else %}
                  <td>
                    <a href="{% url 'done' todo.id %}">💤</a>
                  </td>
                {% endif %}
    ...
```

- test ettik, çalışıyor. Mouse ile tıkladığımızda durumu değişiyor.


#### priority'si şundan büyük olanların sayısını gösterelim;

- views.py' da todo'lar ile birlikte context içinde hesaplanan priority_count'u da gönderiyoruz, template'te yakalayıp gösteriyoruz.


#### tamamlanan (Is-Done) todoların sayını gösterelim;

- views.py' da todo'lar ile birlikte context içinde hesaplanan done_count'u da gönderiyoruz, template'te yakalayıp gösteriyoruz.

todo/templates/todo/home.html
```html
    <div class="col-lg-10 mx-auto p-0 pt-1 mt-1 shadow text-end alert alert-info text-secondary fw-bolder fs-6 fst-italic">
      <div class="p-1 m-2 pb-0">
        <p>Priority'si 2'den büyük olan Todo'ların sayısı : <span class="alert alert-danger p-1">{{ priority_count }} / {{todos | length}}</span></p>
      </div>
      <div class="p-1 m-2 pb-0">
        <p>Tamamlanan Todo'ların sayısı : <span class="alert alert-danger p-1">{{ done_count }} / {{todos | length}}</span></p>
      </div>
    </div>
```





###### crispy_forms & bootstrap5

```bash
- pip install django-crispy-forms
- pip install crispy-bootstrap5
- pip freeze > requirements.txt
```

settings.py
```py
  INSTALLED_APPS = [
    ...
    # myApps
    'users',
    'myapp',
    # 3rd_party_package
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
```

- register template'imizde kullanacağımız formlar düzgün görünsün diye de crispy paketini template'te kullanalım.


register.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-12">

            <h2 class="mt-3 text-center custom-border-radius">Registration Form</h2>

            {% if request.user.is_authenticated %}
                    
            <h3 class="mt-3 text-center">Thanks for registering.</h3>
                    
            {% else %}
                    
            <h3 class="mt-3 text-center custom-border-radius">Fill out the form please!</h3>
            

            <form action="" method="post" enctype="multipart/form-data" class="bg-secondary text-light mt-3 mb-5 p-2 custom-border-radius">
                {% csrf_token %}
                {{ form_user | crispy}}
                {{ form_profile | crispy}}
                <p class="text-center">
                    <button type="submit" class="btn btn-primary">Register</button>
                </p>               
            </form>
            
            {% endif %}
        </div>
    </div>
</div>

{% endblock content %}
```


login.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col">
            <h3 class="text-center custom-border-radius">Please Login</h3>

            <form action="" method="post" class="bg-secondary text-light mt-3 mb-5 p-2 custom-border-radius">
                {% csrf_token %}
                {{ form | crispy }}
                <p class="text-center">
                    <button type="submit" class="btn btn-danger">Login</button>
                </p>
            </form>

        </div>
    </div>
</div>

{% endblock content %}
```


password_change.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col">
            <h3 class="text-center custom-border-radius">Password Change</h3>
            <form action="" method="post" class="bg-secondary text-light mt-3 mb-5 p-2 custom-border-radius">

                {% csrf_token %}

                {{ form | crispy }}

                <p class="text-center">
                    <button type="submit" class="btn btn-danger">Update</button>
                </p>
            
            </form>
        </div>
    </div>
</div>
{% endblock content %}
```



password_change_done.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col bg-secondary mt-3 mb-5 p-2 custom-border-radius text-center">

            <h3 class="text-center custom-border-radius">Password change successful</h3>

            <p class="lead bg-light p-3 rounded fw-bold fs-5">Your password was changed.</p>

            <a href="{% url 'home' %}" class="btn btn-danger btn-lg mt-3">Home</a>

        </div>
    </div>
</div>

{% endblock content %}
```

password_reset_form.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col">
            <h3 class="text-center custom-border-radius">Password Reset</h3>

            <form action="" method="post" class="bg-secondary text-light mt-3 mb-5 p-2 custom-border-radius">
            
                {% csrf_token %}
                {{ form | crispy }}

                <p class="text-center">
                    <input type="submit" value="Reset" class="btn btn-danger">
                </p>
                <input type="hidden" value="{{ next }}" name="next">
            
            </form>
        </div>
    </div>
</div>
{% endblock content %}
```


password_reset_done.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="col-md-8 col-lg-6 row justify-content-center">
        <h3 class="text-center custom-border-radius">Password reset sent.</h3>
        
        <div class="col bg-secondary mt-3 mb-5 p-2 custom-border-radius">

            <p class="lead bg-success rounded m-2 p-2 fw-bold fs-5 text-white border border-info">We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.</p>

            <p class="lead bg-success rounded m-2 mt-3 p-2 fw-bold fs-5 text-white border border-info">If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder.</p>

        </div>
    </div>
</div>

{% endblock content %}
```


password_reset_confirm.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col">
            <h3 class="text-center custom-border-radius">Password Reset Confirm Enter new password</h3>

<p class="lead bg-success rounded mt-3 p-2 fw-bold fs-5 text-white border border-info">Please enter your new password twice so we can verify you typed it in correctly.</p>

<form action="" method="post" class="bg-secondary text-light mt-3 mb-5 p-2 custom-border-radius">
    {% csrf_token %}
    {{ form | crispy }}
    <p class="text-center">
        <input type="submit" value="Change my password" class="btn btn-danger">
    </p>
</form>

{% endblock content %}
```

password_reset_complete.html
```html
{% extends 'todo/base.html' %}

{% block content %}

{% load crispy_forms_tags %}

<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col bg-secondary mt-3 mb-5 p-2 custom-border-radius text-center">

            <h3 class="text-center custom-border-radius">Password reset complete</h3>

            <p class="lead bg-success rounded m-2 mt-3 p-2 fw-bold fs-5 text-white border border-info">Your password has been set. You may go ahead and log in now.</p>

            <a href="{% url 'user_login' %}" class="btn btn-danger btn-lg mt-2">Login</a>
        </div>
    </div>
</div>

{% endblock content %}
```


##### Kullanıcı resmini navbarda göstermek;

- Kullanıcı profil resmini navbar.html dosyasında göstermek için, bu dosyaya kullanıcı bilgilerini geçmemiz gerekecek. 
- base.html dosyası üzerinden navbar.html'a gerekli kullanıcı bilgilerini

- 1. View'da Kullanıcı Bilgilerini Sağlamak
İlk olarak, kullanıcı profil bilgilerini todo app'imizin views.py'ında render edeceğimiz template'in view'inde  view'da elde edip template'e geçireceğiz. Burada eğer db'de bununla ilgili veri yoksa hata vermemesi için try/except blokları kullanıyoruz. Eğer ana sayfanızda veya ilgili bir view'da kullanıcı bilgilerini geçiriyorsanız, kullanıcı profilini context'e eklemeniz gerekir.

todo/wiews.py
```py
#! profile_pic. için
from users.models import UserProfile

def home(request):
    ...
    profile = None #! profile_pic. için
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ...
            #! profile_pic. için
            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                profile = None  # veya uygun bir default değer

        else:
            ...
            #! profile_pic. için
            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                profile = None  # veya uygun bir default değer
    
    context = {
        ...,
        'profile': profile,
    }
    
    return render(request, 'index.html', context)
```

- 2. base.html Dosyasına navbar.html'da Kullanıcı Bilgilerini Geçirme;
- eğer navbar.html isminde bir dosyamız var ve base.html'de include ediyorsak ->

- base.html dosyanızda, navbar.html'ı include ettiğinizde kullanıcı bilgilerini de geçirmelisiniz. Bunu şu şekilde yapabilirsiniz:

base.html
```html
...

 {% include 'navbar.html' with profile=profile %}

...

```

- 3. navbar.html Dosyasında Profil Resmini Gösterme
navbar.html dosyasında profile değişkenini kullanarak profil resmini gösterebilirsiniz.

navbar.html
```html
{% comment %} profile_pic. için {% endcomment %}
 <a class="nav-link" href="">
     {% if profile.profile_pic %}
         <img src="{{ profile.profile_pic.url }}" alt="Profil Resmi" class="rounded-circle" style="width: 40px; height: 40px;">
     {% else %}
         <img src="{% static 'users/images/avatar.png' %}" alt="Varsayılan Profil Resmi" class="rounded-circle" style="width: 40px; height: 40px;">
     {% endif %}
 </a>
```



### pythonanywhere deployment

- Projeyi github a push layın. reponun görünürlüğünü Public olarak ayarlayın. (push larken dbsqlite3'yi ve media'yı da pushluyorum. Db boş olmasın diye.)
- pythonanywhere sign up oluyoruz.
- pythonanywhere free account içinde sadece 1 app konulabiliyor. Birden çok app konulacaksa, birden fazla e-mail ile birden fazla free account oluşturulup ve herbir free account a 1 app konulabilir.
- pythonanywhere default olarak olarak sql3 db sunuyor. free account ta postgresql için para ödemek gerekiyor.
  
- repoda bir değişiklik olduğunda deploy edilmiş app a değişiklikler otomatik yansımıyor. (pipline) Değişiklikleri repoya pushladıktan sonra, pythonanywhere e gidip, terminalden yapılan değişiklikler tekrardan çekilip!!, app i reload etmek gerekiyor.

- pythonanywhere -> dashboard -> New console -> $Bash yeni sekmede açıyoruz.
- pythonanywhere deki bash terminalde;
- rm -rf ....   ile eskilerini siliyoruz. (README.txt kalıyor.)
```bash
rm -rf klkf.txt
```

- github taki deploye edeceğimiz reponun url ini kopyalıyoruz (clonelar gibi)
- pythonanywhere deki bash terminale;

```bash
git clone https://github.com/Umit8098/Project_Django_Rest_Framework_Rent_A_Car_App_CH-12.git
```

- project imizi pythonanywhere clonladık.
- terminalde ls komutuyla dosyaları görüyoruz,
- projemizin içine, manage.py dosyasıyla aynı seviyeye geliyoruz (cd komutuyla), yani ls komutunu çalıştırdığımızda manage.py ı görmemiz lazım.

- Türkiyede cloud platformlar çok kullanılmıyor, genelde Dedicated Server lar üzerinden işlemler yapılıyor. Tüm proje o server içerisinde oluyor. Servera girip, projeyi clonlama işlemi yapılıyor, veya pipeline kuruluyor (localde bir değişiklik yapıldı, github a pushlandı, merge oldu, development server ından bu değişikliğin algılanıp canlıda değişiklik yapılması...). Bunun için github hook ları var, bu hooklar ile işlem yapılıyor.  Bir değişiklik olduğunda github hookları takip ediliyor, değişiklik olduğunda trigger ediyor, o trigger ile server ınızda otomatik git pull yapıyor, değişiklikleri çekiyor, projeyi yeni şekliyle ayağa kaldırıyor.

- Localde iken yapmamız gereken işlemlerin aynısını yapıyoruz;
    - virtual environment oluşturuyoruz,
    - bazı eski versiyonlarda python 2. versiyonu gelebiliyor. Önce "python --version" ile kontrol edilip, eğer 2. versiyon geliyorsa "python3 --version" ile bir daha kontrol edip bu sefer 3. versiyonun geldiğini görüp, "python3 -m venv env" ile virtual environment oluşturuyoruz.
    - "source env/bin/activate" komutu ile env yi aktif hale getiriyoruz.(Bu ortam linux ortamı olduğu için windows kullanıcıları da ancak bu komutla env aktif hale getirebilir.)
    - projenin dependency lerini (bağımlılıklarını) kuruyoruz.

```bash
- python --version
- python3 --version
- python3 -m venv env  # python -m venv env 
- source env/bin/activate
- pip install -r requirements.txt
```

  - pythonanywhere -> dashboard -> Web -> Add a new web app -> next -> Manual configuration (including virtualenvs) -> Python 3.10 (python versionu) -> next
        All done! Your web app is now set up. Details below. 
        (Hepsi tamam! Web uygulamanız artık kuruldu. Detaylar aşağıda.)
  - Artık app kuruldu ve app ile ilgili bir dashboard sundu bize. Burada manuel configurations lar yapacağız. 
        Bu site 28 Temmuz 2024 Pazar günü devre dışı bırakılacaktır. Buradan 3 ay daha app i çalıştırmak için bir button var.

- Şimdi yapacağımız işlemler -> 
  - Code:
        Source code: -> source codumuzu koyduğumuz yeri yazacağız.
        Working directory: -> source code ile aynı oluyor, bu directory de çalışacaksın diyoruz.  
        WSGI configuration file: -> manuel olarak update edeceğiz.
  - Virtualenv:
        Enter path to a virtualenv, if desired -> env nin nerede olduğunu göstereceğiz, yolunu vereceğiz.


- Source code: -> bash terminalde app in olduğu klasör içerisinde iken, "pwd" yazıp klasörün yolunu görebiliyoruz.
        /home/umit8105/Project_Django_Templates_Todo_App_FB_Authantication-1_CH-11
- Working directory: -> Source code kısmına yazdığımız yolu buraya da yazıyoruz.
        /home/umit8105/Project_Django_Templates_Todo_App_FB_Authantication-1_CH-11
- WSGI configuration file: Manuel configuration yaptığımız için bu WSGY (Web Server Gateway Interface) configuration u da kendimiz yapacağız. django application ile server arasındaki iletişimi sağlayan gateway. Bunda ayarlar yapmalıyız. sağ tıklayıp new tab ile yeni pencerede açıyoruz, Default olarak farmeworklerin ayar template leri var. 74-89 satırları arasında django kısmı var. Bunun haricindeki herşeyi siliyoruz, sadece django ile ilgili kısım kalıyor. İlk iki satır hariç yorumdan kurtarıyoruz.

```py
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/umit8098/mysite/mysite/settings.py'
# and your manage.py is is at '/home/umit8098/mysite/manage.py'
path = '/home/umit8098/mysite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

```

- path kısmında bize manage.py ın yolunu vermemizi istiyor. Aslında source code umuzun olduğu path, biraz önce "pwd" ile almıştık, "/home/umit8103/Project_Django_Rest_Framework_Stock_App_CH-13". Bunu path değişkenine tanımlıyoruz. Yani manage.py ımız bu klasörün içinde bunu söylüyoruz.

```py
path = '/home/umit8104/Project_Django_Rest_Framework_Rent_A_Car_App_CH-12'
```

- os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'  -> settings klasörümüzün bulunduğu yeri belirtiyoruz. Bizim settings klasörümüz core in altında. buraya 'core.settings' yazıyoruz.

```py
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
```


- save ediyoruz.

- Virtualenv: env yolunu vermemiz lazım. Tekrar console a geri dönüyoruz, 
  - env nin olduğu dizne gidiyoruz. (ls yaptığımızda env yi görüyoruz.) 
  - "cd env/" ile env nin dizinine giriyoruz. 
  - pwd yazıp env nin path'ini yani yolunu kopyalıyoruz.
  - kopyaladığımız path i Virtualenv kısmındaki bölüme yazıp tik e tıklıyoruz. env miz de hazır.

```py
/home/umit8104/Project_Django_Rest_Framework_Rent_A_Car_App_CH-12/env
```


- Genel olarak ayarlarımız tamam ama birkaç ayar daha kaldı.
  - SECRET_KEY, DEBUG, ENV_NAME, DJANGO_LOG_LEVEL=INFO (bu projeye özel)
  - Bunları ayarlayacağımız yer Source code kısmındaki Go to directory. sağ tıklayarak yeni sekmede açıyoruz,
  - projemizde bu verileri tuttuğumuz yer .env file ı idi. Açılan sekmede Files kısmına .env yazıp New File oluşturuyoruz. bize .env isminde yeni bir file oluşturdu. manage.py, requirements.txt ile aynı seviyede.
  - Eğer dev, prod şeklinde env mizi ayırmadıysak sadece .env deki değişkenleri tanımlamamız yeterli.
  - Ancak env miz dev ve prod olarak ayrılmış ise -> 
    - SECRET_KEY tanımladık, 
    - DEBUG=True  (Önce True yazıyoruz, hataları görebilmek için. daha sonra False a çekebiliriz.)
    - settings klasörünün __init__.py daki env değişkeninin ismine ne verdiysek onu alıp .env file ında değişken ismi olarak kullanıyoruz. ENV_NAME
    - ENV_NAME=development  
        - prod ayarlarımızda db olarak postgresql var. bizim dev ayarlarını kullanmamız daha iyi. 
        - Ayrıca dev ayarlarını kullanırken de; debug.toolbar sadece localhost ta çalışıyor. Bu yüzden debug.toolbar ayarları ile development çalıştırılırsa hata verecektir. Bu hatayı almamak için dev.py daki debug.toolbar ayarlarını yoruma alıyoruz.
    - Bir de DJANGO_LOG_LEVEL=INFO ayarımız vardı onu da .env file ımıza ekliyoruz.

settings/dev.py
```py
from .base import *

# THIRD_PARTY_APPS = ["debug_toolbar"]

DEBUG = config("DEBUG")

# INSTALLED_APPS += THIRD_PARTY_APPS

# THIRD_PARTY_MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# MIDDLEWARE += THIRD_PARTY_MIDDLEWARE

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]
```


- .env dosyamızın en son hali -> 

.env
```py
SECRET_KEY=o_zoo)sc$ef3bbctpryhi7pz!i)@)%s!ffg_zsxd^n+z+h5=7i
DEBUG=True
ENV_NAME=development
DJANGO_LOG_LEVEL=INFO
```

- bash console a gidip db mizdeki tablolarımız oluşturacağız.
- (Biz projemizi github'a pushlarken db.sqlite3' yi de pushlamıştık. Yani db miz var. Eğer db'siz olarak github'a pushlayıp, oradan pythonanywhere'e deploye ediyorsak o zaman migrate ve superuser yapmamız gerekiyor.) 
- bash console da manage.py file ının bulunduğu dizine gidip db miz deki tablolarımızı oluşturuyoruz, superuser oluşturuyoruz,

```bash
python manage.py migrate
python manage.py createsuperuser
```

- dashboard a gidip Reload butonuna tıklıyoruz. Tüm değişiklikleri algılayacaktır. Daha sonra hemen bir üstte verdiği link ile projemizi pythonanywhere de yeni sekmede çalıştırıyoruz. 
- Bazen ALLOWED_HOSTS hatası veriyor. pythonanywher'e yüklediğimiz projenin settings.py'ına gidip ALLOWED_HOSTS = ['*'] şeklinde update/save ediyoruz ve tekrardan reload ediyoruz.
- admin panele giriyoruz,
- statics ler olmadan, css ler olmadan sayfamız geldi. 
- statics lerin görünmemesinin sebebi; django admin panel bir application ve bunun static file ları env içerisinde duruyor. Bunu localhost ta çalıştırdığımız zaman sıkıntı yaşamıyoruz ama canlı servera aldığımız zaman static root diye bir directory belirtmemiz gerekiyor. Static root, bütün environment ta olan static file ları veya application içerisinde varsa static file larımızı (css, javascript, image)  bunların hepsini tek bir klasör altında topluyor ve canlıdayken oradan çekiyor. Bu static ayarı nı yapmamız gerekiyor. Nasıl yapacağız;
- dashboard -> Source code -> Go to directory -> main -> settings -> base.py  içine STATİC_URL = 'static' altına STATIC_ROOT = BASE_DIR / 'static' yazıyoruz.

settings/base.py
```py
STATİC_URL = 'static'
STATIC_ROOT = BASE_DIR / 'static'
```

- base directory altında static isminde bir klasör oluştur, tüm static file ları bu static folder içerisinde topla demek için şu komutu (collectstatic) bash console da çalıştırıyoruz;

```bash
python manage.py collectstatic
```
- bu komut çalıştırıldıktan sonra; 197 adet static file kopyalandı ve belirttiğimiz folder altında toplandı.
" 162 static files copied to '/home/umit8104/Project_Django_Rest_Framework_Rent_A_Car_App_CH-12/static'. "

- Şimdi dashboarda gidip, web kısmında Static files: kısmında URL altında URL ini (/static/),  ve Directory altında path ini giriyoruz. (path ini zaten bize vermişti -> 197 static files cop..... kısmının sonunda. (/home/umit8098/Project_Django_Rest_Framework_Stock_App/core/static))
- girdikten sonra ✔ işareti ile kaydetmeliyiz.
  
```py
/static/
/home/umit8098/Project_Django_Rest_Framework_Stock_App/core/static
```

- Bu işlemi yaptıktan sonra değişikliklerin algılanması için tekrardan Reload butonuna tıklıyoruz. Artık sayfalarımızın statics leri de geliyor.

 - Şuanda backend projesi deploye edildi. Eğer bu backend için bir frontend yazılmış ise deploye edilmiş projenin endpointlerine istek atması gerekir. Mesela frontend kısmı React ile yazılmışsa istek atılacak endpointler düzenlenip netlify'a deploye edilip, oradan çalıştırılması daha uygun olur. 