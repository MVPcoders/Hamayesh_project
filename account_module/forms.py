from django import forms
from .models import User, Ticket
from django.core.exceptions import ValidationError


####  فرم ثبت نام ##
class SignupModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'}
    ))

    class Meta:
        model = User
        exclude = ['is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'username', 'is_online',
                   'user_permissions', 'groups']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام', 'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی', 'class': "form-control"}),
            'code_meli': forms.TextInput(attrs={'placeholder': 'کد ملی', 'class': "form-control icon-distance"}),
            'mobile': forms.TextInput(attrs={'placeholder': 'تلفن همراه', 'class': "form-control icon-distance"}),
            'land_line': forms.TextInput(attrs={'placeholder': 'تلفن ثابت', 'class': "form-control icon-distance"}),
            'email': forms.TextInput(attrs={'placeholder': 'ایمیل', 'class': "form-control icon-distance"}),
            'degree': forms.Select(attrs={'class': "form-control"}),
            'field_of_study': forms.TextInput(attrs={'placeholder': 'رشته تحصیلی', 'class': "form-control"}),
            'company': forms.TextInput(attrs={'placeholder': 'شرکت/سازمان', 'class': "form-control"}),
            'province': forms.TextInput(attrs={'placeholder': 'استان', 'class': "form-control"}),
            'city': forms.TextInput(attrs={'placeholder': 'شهر', 'class': "form-control"}),
            'address': forms.TextInput(attrs={'placeholder': 'آدرس', 'class': "form-control icon-distance"}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'کد پستی', 'class': "form-control icon-distance"}),
            'kind_of_signup': forms.Select(attrs={'class': "form-control"}),
            'password': forms.PasswordInput(attrs={'placeholder': 'رمز عبور', 'class': "form-control"}),
        }

        error_messages = {
            'first_name': {
                'required': 'نام خود را وارد کنید'
            },
            'last_name': {'required': 'نام خانوادگی خود را وارد کنید'},
            'code_meli': {'required': 'کد ملی خود را وارد کنید'},
            'mobile': {
                'required': 'تلفن همراه خود را وارد کنید'},
            'email': {
                'required': 'ایمیل خود را وارد کنید',
                'invalid': 'ایمیل وارد شده اشتباه است'},
            'degree': {'required': 'مدرک تحصیلی خود را وارد کنید'},
            'province': {'required': 'استان خود را وارد کنید'},
            'city': {'required': 'شهر خود را وارد کنید'},
            'address': {'required': 'آدرس خود را وارد کنید'},
            'postal_code': {'required': 'کد پستی خود را وارد کنید'},
            'kind_of_signup': {'required': 'نوع ثبت نام خود را وارد کنید'},
        }

    ####### اعتبار سنجی فیلد ها #####

    #### موبایل ##
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        user_mobile = User.objects.filter(mobile__iexact=mobile).exists()
        if not mobile.isdigit():
            raise ValidationError("فقط عدد وارد کنید")
        elif len(mobile) != 11:
            raise ValidationError(f'موبایل باید 11 رقم باشد طولش ({len(mobile)}) است ')
        elif user_mobile:
            raise ValidationError('تلفن همراه قبلاً استفاده شده')
        return mobile

    ### کد ملی ##
    def clean_code_meli(self):
        code_meli = self.cleaned_data.get('code_meli')
        if not code_meli.isdigit():
            raise ValidationError("فقط عدد وارد کنید")
        elif len(code_meli) != 10:
            raise ValidationError(f'کد ملی باید 10 رقم باشد طولش ({len(code_meli)}) است ')
        return code_meli

    #### کد پستی ##
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not postal_code.isdigit():
            raise ValidationError("فقط عدد وارد کنید")
        elif len(postal_code) != 10:
            raise ValidationError(f'کد پستی باید 10 رقم باشد طولش ({len(postal_code)}) است ')
        else:
            user_postal_code = User.objects.filter(postal_code__iexact=postal_code).exists()
            if user_postal_code:
                raise ValidationError('کد پستی قبلاً استفاده شده')
        return postal_code

    ### تلفن ثابت#
    def clean_land_line(self):
        land_line = self.cleaned_data.get('land_line')
        if land_line is not None:
            if not land_line.isdigit():
                raise ValidationError('فقط عدد وارد کنید')
            elif len(land_line) != 11:
                raise ValidationError(f'شماره تلفن ثابت باید 11 رقم باشد طولش ({len(land_line)}) است ')
            elif land_line:
                user_land_line = User.objects.filter(land_line__iexact=land_line).exists()
                if user_land_line:
                    raise ValidationError('تلفن ثابت قبلاً استفاده شده ')
            return land_line

    ### رمز عبور ##
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        return password

    #### تکرار رمز عبور ##
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('عدم مطابقت با رمز عبور')
        return confirm_password

    ### ایمیل ##
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('لطفاً ایمیل خود را وارد کنید')
        return email

    ### نام ##
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError('نام خود را وارد کنید')
        return first_name

    ### نام خانوادگی #
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError('نام خانوادگی خود را وارد کنید')
        return last_name

    ### مدرک تحصیلی#
    def clean_degree(self):
        degree = self.cleaned_data.get('degree')
        if degree is None:
            raise ValidationError('مدرک تحصیلی خود را انتخاب کنید')
        return degree

    ### نوع ثبت نام ##
    def clean_kind_of_signup(self):
        kind_of_signup = self.cleaned_data.get('kind_of_signup')
        if kind_of_signup is None:
            raise ValidationError('نوع ثبت نام را انتخاب کنید')
        return kind_of_signup


#### فرم ورود##
class LoginForm(forms.Form):
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control icon-distance',
            'placeholder': 'تلفن همراه'
        }),
        error_messages={
            'required': 'تلفن همراه خود را وارد کنید'
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        error_messages={
            'required': 'رمز عبور خود را وارد کنید'
        }
    )

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise ValidationError('فقط عدد وارد کنید')
        elif len(mobile) != 11:
            raise ValidationError('باید 11 رقم باشد')
        return mobile

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None:
            raise ValidationError("رمز عبور خود را وارد نمایید")
        return password

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'department', 'priority', 'message', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'mt-1 p-2 w-full border rounded focus:ring-2 focus:ring-blue-500'
            }),
            'department': forms.Select(attrs={
                'class': 'mt-1 p-2 w-full border rounded focus:ring-2 focus:ring-blue-500'
            }),
            'priority': forms.Select(attrs={
                'class': 'mt-1 p-2 w-full border rounded focus:ring-2 focus:ring-blue-500'
            }),
            'message': forms.Textarea(attrs={
                'class': 'mt-1 p-2 w-full border rounded focus:ring-2 focus:ring-blue-500',
                'rows': 5
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'mt-1 p-2 w-full border rounded focus:ring-2 focus:ring-blue-500'
            }),
        }