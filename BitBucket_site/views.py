from django.shortcuts import render, redirect
from .forms import AccessRequestForm
from . import access_script
import requests
import base64
from django.contrib.auth import get_user
#from BitBucket_site.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from .models import Repository, AccessRequest
#from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login 
from django.urls import reverse
#from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from .forms import RegistrationForm
from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth import get_user_model
#from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth.backends import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
#from .task import send_approval_request
#from .task import send_request
from .models import Manager
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import AccessRequest, ApprovalRequest, Repository, Manager
from .task import send_request_email 
User = get_user_model()




BITBUCKET_BASE_URL = "https://api.bitbucket.org/2.0"
BITBUCKET_USERNAME = "Rahul_sharma_12345"  # Your Bitbucket username
BITBUCKET_APP_PASSWORD = "ATBBBEbugWzKmDh6MGEcGq2LBTU601F16C33"  # Your Bitbcket app password
WORKSPACE = "rahul-workspace"  # Your Bitbucket workspace

def get_basic_auth_header():
    credentials = f"{BITBUCKET_USERNAME}:{BITBUCKET_APP_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

def get_repositories():
    url = f"{BITBUCKET_BASE_URL}/repositories?workspace={WORKSPACE}&role=member"
    all_repositories = []

    while url:
        response = requests.get(url, headers=get_basic_auth_header())
        
        if response.status_code == 200:
            repositories_page = response.json()
            all_repositories.extend(repositories_page["values"])
            url = repositories_page.get("next")  # Get the URL for the next page
        else:
            raise Exception(f"Failed to fetch repositories: {response.status_code}")
    return all_repositories



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'welcome to GFG world'
            message = f'Hi {user.first_name}, thank you for registering in BitBucket_site.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['rahhul.business@gmail.com' ]
            send_mail( subject, message, email_from, recipient_list )  # Save the User instance
            Email_address= form.cleaned_data['email'] 

            #UserProfile.objects.create(user=user, username=bitbucket_username) 
            #UserProfile.objects.create(user=user, username=bitbucket_username)  
            
            login(request, user)  # Automatically log in the new user
            return redirect('index')  # Redirect to home page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})





def user_login(request,user):
    if request.method == 'POST':
        # Handle user login form submission
        Email_address = request.POST.get('Email_address')
        password = request.POST.get('password')
        
        user = authenticate(request,  Email_address =Email_address, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Handle invalid credentials
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'registration/login.html')

#def user_login(request, user):
    # Log in the user and set session data
    login(request, user)
    request.session['username'] = user.username

@login_required
def index(request):
    Email_address = request.session.get('Email_address')

   # if not bitbucket_username:
        #return redirect('login')
    
    repositories = get_repositories()
    all_repositories_data = []
    search_query = request.GET.get('search', '')  # Get the search query from the URL parameter

    # Iterate through fetched repositories and save them to the database
    for repo in repositories:
        repo_name = repo['name']
        repo_slug = repo['slug']
        
        # Check if the repository already exists in the database
        repository, created = Repository.objects.get_or_create(
            repo_slug=repo_slug,
            defaults={'name': repo_name}
        )
        
        # You can also update the name if the repository already exists but the name has changed
        if not created and repository.name != repo_name:
            repository.name = repo_name
            repository.save()

        # Check if the repository name matches the search query
        if search_query.lower() in repo_name.lower():
            repo_data = {
                'name': repo_name,
                'repo_slug': repo_slug
            }
            all_repositories_data.append(repo_data)
    
    return render(request, 'index.html', {'all_repositories_data': all_repositories_data, 'search_query': search_query, 'Email address': Email_address})
def request_access(request):
    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            try:
                user, created = User.objects.get_or_create(Email_address=request.user.Email_address)
            
                access_request = form.save(commit=False)
                access_request.user = request.user
                acess_request.User_display_name= user.first_name
                access_request.save()
                print("Access request saved:", access_request)
            except Exception as e:
                print("Error saving access request:", e)
            return redirect('index')
    else:
        form = AccessRequestForm()
    
    return render(request, 'access_request.html', {'form': form})



def repository_detail(request, repo_slug):
    # Fetch detailed information about the repository using repo_slug
    repository_info = {
        'name': repo_slug,
    }
    return render(request, 'repository_detail.html', {'repository_info': repository_info})

def access_request_list(request):
    access_requests = AccessRequest.objects.all()
    print("Access requests:", access_requests)  # Add this line
    return render(request, 'access_request_list.html', {'access_requests': access_requests})
def some_view(request):
    if not user_is_authenticated:
        return redirect(reverse('login'))  # Redirect to the 'login' view
    else:
        return redirect(reverse('index'))

#@login_required
#def request_access_form(request, repo_slug):
    user = request.user
    try:
        repository = Repository.objects.get(repo_slug=repo_slug)
    except Repository.DoesNotExist:
        return redirect('index')  # Redirect or display an error message
    
    access_type = request.POST.get('access_type')  # Get the access_type value from POST data
    
    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        print(form)
        if form.is_valid():
            access_request = form.save(commit=False)
            access_request.repository = repository
            access_request.user = user
            access_request.access_type = access_type  # Set the access_type
            access_request.save()
            return redirect('index')
    else:
        form = AccessRequestForm(initial={'access_type': 'read'})  # Set default value for access_type

    context = {
        'form': form,
        'repository': repository,
        'access_type': access_type,
    }
    return render(request, 'access_request.html', context)
#@login_required
#def request_access_form(request, repo_slug):
    try:
        repository = Repository.objects.get(repo_slug=repo_slug)
    except Repository.DoesNotExist:
        return redirect('index')  # Redirect or display an error message

    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            access_request = form.save(commit=False)
            access_request.repository = repository
            access_request.user = request.user
            access_request.save()

            # Get the Bitbucket username of the logged-in user
            bitbucket_username = get_bitbucket_username(request.user)

            # Call the grant_access function with appropriate parameters
            grant_access(bitbucket_username, repo_slug, access_request.access_type)

            return redirect('index')
    else:
        initial_data = {
            'user': request.user,
            'repository': repository,
        }
        form = AccessRequestForm(initial=initial_data)

    context = {
        'form': form,
        'repository': repository,
    }
    return render(request, 'access_request.html', context)

def get_bitbucket_Email_address(user):
    return user.Email_address


#@login_required
#def grant_access(bitbucket_username, repo_slug, access_type):
    if request.method == 'POST':
        user = request.user
        repo_slug = request.POST.get('repository')  # Get repo_slug from the form
        access_type = request.POST.get('access_type')  # Get access_type from the form

        # Check if the user has a corresponding access request
        access_request = AccessRequest.objects.filter(user=user, repository__repo_slug=repo_slug).first()

        if access_request:
            # Call your script function to grant access
            success = access_script(user.username, repo_slug, access_type)

            if success:
                # Update the access request status or log the success
                access_request.access_granted = True
                access_request.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Access grant failed'})

    # Redirect to a relevant page in case of GET request or access grant failure
    return redirect('index')



def update_display_names_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            Email_address = row['Email address']  # Assuming 'email' is the column header for email ids
            display_name = row['Public name']  # Assuming 'display_name' is the column header for display names
            
            # Query the auth_user table for the user with the given email
            try:
                user = User.objects.get(email=Email_address)
                user.first_name = display_name  # Update the display name
                user.save()
                print(f"Updated display name for {Email_address} to {display_name}")
            except User.DoesNotExist:
                print(f"User with email {Email_address} not found")




# Provide the path to your export_list.csv file
csv_file_path = 'C:\export_list.csv.csv'
update_display_names_from_csv(csv_file_path)


# ... (imports)

def request_access_form(request, repo_slug):
    try:
        repository = Repository.objects.get(repo_slug=repo_slug)
    except Repository.DoesNotExist:
        return redirect('index')  # Redirect or display an error message

    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            access_request = form.save(commit=False)
            access_request.repository = repository
            access_request.user = request.user

            # Access the selected manager from the form
            selected_manager_id = request.POST.get('manager')
            print(selected_manager_id)  # Get the manager ID from the form POST data

            if selected_manager_id:
                try:
                    selected_manager = Manager.objects.get(id=selected_manager_id)
                    access_request.manager = selected_manager  # Set the manager for the access request
                    access_request.save()

                    # Send an email to the selected manager
                    #send_mail(
                       # "Access Request",
                       # f"{access_request.user.first_name} has requested {access_request.access_type} access to {access_request.repository}",
                      #  "bitbuckettest361@gmail.com",
                       # [selected_manager.email],  # Send the request to the selected manager's email
                       # fail_silently=False,
                   # )
                    #print(selected_manager.email)
                    print(access_request.access_type)
                    # Call the send_access_request Celery task with appropriate parameters
                    send_request_email(
                        requester_id=request.user.id,
                        manager_id=selected_manager_id,
                        repository_id=repository.id,
                        access_type=access_request.access_type,
                        message="Your message here",
                        request_type="access" 
                         # Change this to "approval" if it's an approval request
                    )

                    return redirect('index')
                except Manager.DoesNotExist:
                    return HttpResponse("Selected manager does not exist.", status=400)
    else:
        initial_data = {
            'user': request.user,
            'repository': repository,
        }
        form = AccessRequestForm(initial=initial_data)

    managers = Manager.objects.all()  # Retrieve all Manager objects
    context = {
        'form': form,
        'repository': repository,
        'managers': managers,
    }
    return render(request, 'access_request.html', context)
#def create_access_request(request, repository_id):
    repository = get_object_or_404(Repository, pk=repository_id)
    if request.method == 'POST':
        access_type = request.POST['access_type']
        manager_id = request.POST['manager']  # Get the manager ID from the form
        user_display_name = request.POST['user_display_name']
        
        # Create an access request
        access_request = AccessRequest.objects.create(
            user=request.user,  # Assuming the user is authenticated
            repository=repository,
            access_type=access_type,
            manager_id=manager_id,  # Assign the manager ID
            User_display_name=user_display_name,
        )
        
        # Send an email notification to the manager
        send_request_email.apply_async(
            (request.user.id, manager_id, repository.id, access_type, 'access'),
            countdown=10  # Delay in seconds before sending the email
        )
        
        messages.success(request, 'Access request sent successfully.')
        return redirect('repository_detail', repository_id=repository_id)
    
    managers = Manager.objects.all()
    return render(request, 'access_request_form.html', {'repository': repository, 'managers': managers})

# View for approving or denying an access request
def approve_or_deny(request, access_request_id, decision):
    access_request = get_object_or_404(AccessRequest, pk=access_request_id)
    if request.method == 'POST':
        # Handle the approval or denial logic here
        if decision == 'approve':
            print('delta')
            access_request.status = 'Approved'
            access_request.save()
            print(access_request)
            #print(AccessRequest)
            grant_access(request, access_request.repository.repo_slug, access_request.access_type)
            messages.success(request, 'Access request approved.')
        elif decision == 'deny':
            print('theta')
            access_request.status = 'Denied'
            access_request.save()
            messages.success(request, 'Access request denied.')
        return redirect('index')  # Redirect to a list of access requests
    
    return render(request, 'approve_deny_request.html', {'access_request': access_request})


# ... (other code)


def grant_access(request, repo_slug, access_type):
    
    access_request = AccessRequest.objects.filter( repository__repo_slug=repo_slug).first()
    if not access_request:
        return JsonResponse({'success': False, 'message': 'Access request not found'})
    print(request.user.first_name)
    
    # Assuming you have the necessary credentials and parameters
    username = 'Rahul_sharma_12345'  # Bitbucket admin username
    app_password = 'ATBBBEbugWzKmDh6MGEcGq2LBTU601F16C33'  # Bitbucket app password
    workspace_slug = 'rahul-workspace'  # Workspace slug
    User_display_name = request.user.first_name
    print(User_display_name)
   

    # Assuming Bitbucket username and display_name are the same
    repo_slugs = [repo_slug]
    permission = access_type  

    # Call the function from access_script
    success = access_script.grant_access_BitBucket(username, app_password, workspace_slug, User_display_name, repo_slugs, permission)

    if success:
        # Update the access request status or log the success
        access_request = AccessRequest.objects.filter(user=user, repository__repo_slug=repo_slug).first()
        if access_request:
            access_request.access_granted = True
            access_request.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Access grant failed'})

    # Redirect to a relevant page in case of access grant failure
    return JsonResponse({'success': False, 'message': 'Access grant failed'})
def logout_view(request):
    # Clear the user session
    request.session.clear()
    logout(request)
    return redirect('login')







def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            Email_address = form.cleaned_data['username']  # Use 'username' field for email
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=Email_address, password=password)  # Use 'Email_address' as username
            
            if user is not None:
                login(request, user)
                return redirect('index')
                send_mail(
                    "email",
                    "login",
                    "bitbuckettest361@gmail.com",
                    ["bitbuckettest361@gmail.com"],
                    fail_silently=False,
                )
                
            else:
                error_message = 'Invalid credentials'
                return render(request, 'registration/login.html', {'form': form, 'error': error_message})
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'registration/login.html', context)

            



