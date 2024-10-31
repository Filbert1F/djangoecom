from django import forms
from django.core.validators import RegexValidator
from store.models import Order
from .cart import Cart

class PayForm(forms.ModelForm):
	phone_regex = RegexValidator(
		regex=r'^0\d{11}$',
		message="Phone number must start with 0 and contain 12 digits total. Format: 000000000000"
	)
	phone = forms.CharField(validators=[phone_regex], required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
	address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))

	class Meta:
		model = Order
		fields = ('phone', 'address')

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)

		super(PayForm, self).__init__(*args, **kwargs)
		if self.request.user and hasattr(self.request.user, 'profile'):
			self.fields['phone'].initial = self.request.user.profile.phone

	def save(self, commit=True):
		instance = super().save(commit=False)
		instance.user = self.request.user
		cart = Cart(self.request)
		instance.total_price = cart.get_total_price()
		if commit:
			instance.save()
		return instance