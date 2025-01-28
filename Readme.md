<!-- Please update value in the {}  -->

<h1 align="center">Project_Django_Template_Todo_App</h1>


<div align="center">
  <h3>
    <a href="https://umit8105.pythonanywhere.com/">
      Live Demo
    </a> 
  </h3>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
  - [Kullanıcı Login](#kullanıcı-login)
  - [Todo App](#todo-app)
- [Built With](#built-with)
- [How To Use](#how-to-use)
  - [Test Kullanıcı Bilgileri](#test-kullanıcı-bilgileri)
- [About This Project](#about-this-project)
- [Key Features](#key-features)
- [Contact](#contact)

<!-- OVERVIEW -->

## Overview

### Kullanıcı Login
<!-- ![screenshot](project_screenshot/Todo_App_Temp-1.gif) -->
<img src="project_screenshot/Todo_App_Temp-1.gif" alt="Kullanıcı Login" width="400"/>
➡ Kullanıcıların giriş yaparak Todo... sağlayabileceği ekran.

---

### Todo App
<!-- ![screenshot](project_screenshot/Todo_App_Temp-2.gif) -->
<img src="project_screenshot/Todo_App_Temp-2.gif" alt="Todo App" width="400"/>
➡ Kullanıcıların Todo... ekran.

---


## Built With

<!-- This section should list any major frameworks that you built your project using. Here are a few examples.-->
Bu proje aşağıdaki araçlar ve kütüphaneler kullanılarak geliştirilmiştir:

- [Django Templates](https://docs.djangoproject.com/en/5.1/topics/templates/): Dinamik web sayfaları oluşturmak için.
- [Bootstrap5](https://getbootstrap.com/docs/5.0/getting-started/introduction/): Duyarlı ve modern bir kullanıcı arayüzü sağlamak için.
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/): Formları kolayca stilize etmek için.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/): Kullanıcı doğrulama ve yetkilendirme modülü.




## How To Use

<!-- This is an example, please update according to your application -->

To clone and run this application, you'll need [Git](https://github.com/Umit8098/Project_Django_Templates_Todo_App_FB_Authantication-1_CH-11)

When installing the required packages in the requirements.txt file, review the package differences for windows/macOS/Linux environments. 

Complete the installation by uncommenting the appropriate package.

---

requirements.txt dosyasındaki gerekli paketlerin kurulumu esnasında windows/macOS/Linux ortamları için paket farklılıklarını inceleyin. 

Uygun olan paketi yorumdan kurtararak kurulumu gerçekleştirin.

```bash
# Clone this repository
$ git clone https://github.com/Umit8098/Project_Django_Templates_Todo_App_FB_Authantication-1_CH-11.git

# Install dependencies
    $ python -m venv env
    $ python3 -m venv env (for macOs/linux OS)
    $ env/Scripts/activate (for win OS)
    $ source env/bin/activate (for macOs/linux OS)
    $ pip install -r requirements.txt
    $ python manage.py migrate (for win OS)
    $ python3 manage.py migrate (for macOs/linux OS)

# Create and Edit .env
# Add Your SECRET_KEY in .env file

"""
# example .env;

SECRET_KEY =123456789abcdefg...
"""

# Run the app
    $ python manage.py runserver
```

### Test Kullanıcı Bilgileri

Canlı demo için aşağıdaki test kullanıcı bilgilerini kullanabilirsiniz:
- **Kullanıcı Adı**: testuser
- **Şifre**: testpassword123
- **e-mail**: testuser@gmail.com
Bu kullanıcı sadece sipariş verme ve profil güncelleme işlemlerini gerçekleştirebilir.


## About This Project
- Todo Application.

<hr>

- Todo Application


## Key Features

- **Pizza Siparişi Yönetimi**: Kullanıcılar çeşitli boyut ve malzemelerle pizza siparişi verebilir.
- **Kullanıcı Yönetimi**: Kayıt, giriş, profil düzenleme ve şifre değiştirme işlemleri.
- **Sipariş Takibi**: Kullanıcılar verdikleri siparişleri görüntüleyebilir ve yönetebilir.
- **Kullanıcı Bildirimleri**: Başarılı işlemler sonrası kullanıcıya ekran mesajı ile geri bildirim sağlanır.


## Contact

<!-- - Website [your-website.com](https://{your-web-site-link}) -->
- **GitHub** [@Umit8098](https://github.com/Umit8098)

- **LinkedIn** [@umit-arat](https://linkedin.com/in/umit-arat/)
<!-- - Twitter [@your-twitter](https://{twitter.com/your-username}) -->
