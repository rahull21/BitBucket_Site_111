from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from .models import User
from .models import Manager
from .models import Repository
from .models import AccessRequest
from django.http import HttpRequest
from django.contrib.sites.shortcuts import get_current_site





@shared_task
def send_request_email(requester_id, manager_id, repository_id, access_type, request_type, message):
    try:
        requester = User.objects.get(pk=requester_id)
        manager = Manager.objects.get(pk=manager_id)
        repository = Repository.objects.get(pk=repository_id)

        if request_type == "access":
            # Create the access request
            access_request = AccessRequest.objects.create(
                user=requester,
                manager=manager,
                repository=repository,
                access_type=access_type,
            )
            request = HttpRequest()
            request.META['HTTP_HOST'] = get_current_site(None).domain
            print(get_current_site(None).domain)

            # Generate the approve and deny URLs
            approve_url = request.build_absolute_uri(reverse('approve_or_deny', args=[access_request.id, 'approve']))
            deny_url = reverse('approve_or_deny', args=[access_request.id, 'deny'])
            #print(approve_url)
            #print(denial_request_url)
            #grant_access(requester, repo_slug, access_type, requester.first_name)
            # Create an HTML message for the email
            subject = "Access Request"
            html_message = render_to_string('access_request_email.html', {
                'requester': requester,
                'repository': repository,
                'access_type': access_type,
                'approve_url': approve_url,
                

            })
            plain_message = strip_tags(html_message)  # Create a plain text version of the HTML content

            from_email = "bitbuckettest361@gmail.com"  # Change this to your email address
            to_email = manager.email

            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
    
    except Exception as e:
        print(f"Failed to send {request_type} request: {str(e)}")
