from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.
# Add @login_required decorator to ensure user logged in
# DMcC 23/04/24 simplified user profile maintenance
@login_required
def user_profile(request):
    """ Displays the user's profile. """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'profiles/profile.html', {'form': form})

