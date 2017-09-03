from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import(
	EditProfileForm,
	)

def profile(request):

	if request.method == 'GET':
		formulario = EditProfileForm(instance=request.user)
	else:
		formulario = EditProfileForm(request.POST, instance=request.user)
		if formulario.is_valid():
			formulario.save()
			#update_session_auth_hash(request,formulario.user)
			return redirect(reverse('profile'))
	return render(request, 'accounts/profile.html', {'formulario':formulario})

