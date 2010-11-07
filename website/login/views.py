from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from common.models import Customer

def login_signup(request):
    errors = {}

    # User cannot signup if they are already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    # Display the registration page
    if request.method == "GET":
        t = loader.get_template("login/signup.html")
        c = RequestContext(request)
        return HttpResponse(t.render(c))

    # Verify and sanitize input
    username = request.POST.get("username")
    #TODO: Verify alphan umeric and 5+ letters
    if len(username) < 5:
        errors["user"] = "Username must be at least 5 characters long"
    elif len(username) > 36:
        errors["user"] = "Username must be 36 characters or less"
    elif Customer.objects.filter(username=username):
        errors["user"] = "Username already taken"

    email = request.POST.get("email")
    #TODO: Use regex validation
    if len(email) < 5:
        errors["email"] = "Invalid email address"
    elif Customer.objects.filter(email=email):
        errors["email"] = "Email already taken"

    password = request.POST.get("password")
    if len(password) < 5:
        errors["pass"] = "Password too short"
    elif len(password) > 5 and password != request.POST.get("confirm"):
        # Passwords did not match
        errors["pass"] = "Passwords do not match"

    # Validation errors
    if errors:
        t = loader.get_template("login/signup.html")
        c = RequestContext(request, locals())
        return HttpResponse(t.render(c))

    # Create the user
    user = Customer.objects.create_user(username=username, email=email, password=password)
    user.save()

    # Log them in?
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        #TODO: Display welcome message
        return HttpResponseRedirect("/")

    # User not active or problem creating user
    return HttpResponseRedirect("/signup")

