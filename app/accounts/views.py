from django.contrib.auth import login
from django.shortcuts import redirect, render

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Save the user object without committing to the database
            user.is_staff = True  # Set the user as a staff member
            user.save()  # Save the user object to the database
            login(request, user)  # Log the user in
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
