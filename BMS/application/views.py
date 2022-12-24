from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy, reverse

from .forms import LoginForm, RegisterForm, BikeCreationForm
from .models import Bike

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('profile')

# for the logout view, only do the internal logout-routine and don't display anything
class LogoutView(auth_views.LogoutView):
    pass

class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class ProfileView(generic.TemplateView):
    template_name = "profile.html"

class IndexView(generic.TemplateView):
    template_name = "index.html"

class CreateBikeView(generic.FormView):
    form_class = BikeCreationForm
    success_url = "../createBike"
    template_name = "createBike.html"

class BikeListView(generic.TemplateView):
    template_name = "bikeList.html"

    extra_context = {"Bikes": Bike.objects.all()}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # extent the context with a "Bikes" section, that contains all bike instances
        context["Bikes"] = Bike.objects.all()

        return context
 

    