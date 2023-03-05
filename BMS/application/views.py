from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group


from .forms import LoginForm, RegisterForm, BikeCreationForm, BorrowingCreationForm, ChangeUserForm
from .models import Bike, Borrowing, User


class IndexView(generic.TemplateView):
    template_name = "index.html"


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('profile')


class LogoutView(auth_views.LogoutView):
    # for the logout view, only do the internal logout-routine and don't display anything
    # it will redirect to the login view
    pass


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # assign each new user to student group
        user = form.save()
        user.groups.add(Group.objects.get(name='student'))
        #user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy("login")

    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add all borrowings of current user to context
        context["borrowings"] = Borrowing.objects.filter(borrower__id=self.request.user.pk).order_by("start_time")

        return context


class UserListView(PermissionRequiredMixin, generic.TemplateView):
    permission_required = "application.view_user"

    template_name = "userList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # extent the context with a "Users" section, that contains all users
        context["Users"] = User.objects.all()

        return context


class ChangeUserView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = "application.change_user"

    template_name = "changeUser.html"
    form_class = ChangeUserForm
    model = User

    success_url = reverse_lazy("user-view")

    # custom form saving function
    def form_valid(self, form):
        something_changed = False

        user = User.objects.get(pk=self.kwargs["pk"])

        # if group is given by the form, assign new group to user and overwrite previous groups
        if form.cleaned_data["groups"] is not None:
            user.groups.clear()
            user.groups.add(form.cleaned_data["groups"])
            something_changed = True            
        
        # if there's a new name, update the user
        if form.cleaned_data["first_name"] != user.first_name or form.cleaned_data["first_name"] is not None:
            user.first_name = form.cleaned_data["first_name"]
            something_changed = True
        
        # if something changed, save the new user
        if something_changed:
            user.save()

        # lasty, redirect to the success_url
        return HttpResponseRedirect(self.get_success_url())

    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = User.objects.filter(pk=self.kwargs["pk"])
        return context


class CreateBikeView(PermissionRequiredMixin, generic.CreateView):
    permission_required = "application.add_bike" # I'm using the standart django permission types

    form_class = BikeCreationForm
    success_url = reverse_lazy("createBike")
    template_name = "createBike.html"


class BorrowBikeView(PermissionRequiredMixin, generic.FormView):
    permission_required = "application.add_borrowing"

    # create a new bike borrowing
    form_class = BorrowingCreationForm
    success_url = reverse_lazy("bikeList")
    template_name = "createBorrowing.html"

    def form_valid(self, form):
        # the form only has endtime, so just make a borrowing when its submitted successfully

        Borrowing.objects.create(
            borrower=self.request.user, 
            borrowed_bike=Bike.objects.get(pk=self.kwargs["bikepk"]), 
            start_time=timezone.now(),
            end_time=form.cleaned_data["end_time"]
        )

        return HttpResponseRedirect(self.get_success_url())


class BikeListView(PermissionRequiredMixin, generic.TemplateView):
    permission_required = "application.view_bike"

    template_name = "bikeList.html"  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # extent the context with a "Bikes" section, that contains all bike instances
        context["Bikes"] = Bike.objects.all()
        context["Borrowings"] = Borrowing.objects.all().order_by("-end_time")

        return context

