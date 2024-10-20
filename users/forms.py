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