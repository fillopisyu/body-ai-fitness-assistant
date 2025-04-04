# profiles/forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'weight_kg', 'height_cm', 'goal']
        # widgets = {
        #     'goal': forms.Select(attrs={'class': 'form-select'}),
        # }
        # labels = {
        #     'age': 'Yaşınız',
        #     'weight_kg': 'Kilonuz (kg)',
        #     'height_cm': 'Boyunuz (cm)',
        #     'goal': 'Hedefiniz',
        # }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Form alanlarına Bootstrap sınıflarını uygula
        default_widget_class = 'form-control mb-2'
        select_widget_class = 'form-select mb-2'

        for field_name, field in self.fields.items():
            # Alanın widget türüne göre uygun sınıfı ata
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': select_widget_class})
            elif not isinstance(field.widget, forms.CheckboxInput): # Checkbox'ları hariç tut
                 field.widget.attrs.update({'class': default_widget_class})

        # Özel olarak hedef alanı için tekrar ayarla (yukarıdaki döngü Select'i de kapsayabilir ama bu garanti eder)
        # if 'goal' in self.fields:
        #      self.fields['goal'].widget.attrs.update({'class': select_widget_class})