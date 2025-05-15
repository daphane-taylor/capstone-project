from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import SignupForm, UpdateProfileForm
from .models import Profile
from django.urls import reverse_lazy

class SignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        passw = form.cleaned_data.get('password')
        user.set_password(passw)
        user.save()

        # Create an empty profile for the user
        Profile.objects.create(user=user)

        return super().form_valid(form)


class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, self.template_name, {'error_message': error_message})
    

class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'accounts/update_profile.html'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('home') # should be view profile

    def get_object(self):
        # return only the logged in user's profile
        profile = Profile.objects.get(user=self.request.user)
        return profile
    
    
class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_queryset(self):
        # Allow viewing any profile, but use prefetch_related for efficiency
        return Profile.objects.all().prefetch_related('user')


    
def logout_view(request):
    logout(request)
    return redirect('login')