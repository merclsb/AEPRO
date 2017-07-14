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


# def view_profile(request, pk=None):
#     if pk:
#         user = User.objects.get(pk=pk)
#     else:
#         user = request.user
    
   
#     args = {'user': user,
#     		}
#     return render(request, 'accounts/view_profile.html', args)

# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)

#         if form.is_valid():
#             form.save()
#             return redirect(reverse('view_profile'))
#     else:
#         form = EditProfileForm(instance=request.user)
#         args = {'form': form}
#         return render(request, 'accounts/edit_profile.html', args)