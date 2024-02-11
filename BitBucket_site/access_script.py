# access_scripts.py
import requests
import json

def grant_access_BitBucket(username, app_password, workspace_slug, User_display_name, repo_slugs, permission):
    print('Helo')
    url = f"https://api.bitbucket.org/2.0/workspaces/{workspace_slug}/permissions"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.get(
        url,
        headers=headers,
        auth=(username, app_password)
    )
    members = json.loads(response.text)['values']
    
    user_uuid = None
    for member in members:
        if member['type'] == 'workspace_membership' and member['user']['display_name'] == User_display_name:
            user_uuid = member['user']['uuid']
            break

    if not user_uuid:
        print(f"Could not find user with display name '{User_display_name}'")
    else:
        for repo_slug in repo_slugs:
            url = f"https://api.bitbucket.org/2.0/repositories/{workspace_slug}/{repo_slug}/permissions-config/users/{user_uuid}"
            data = {"permission": permission}
            headers = {"Content-Type": "application/json"}
            auth = (username, app_password)
            response = requests.put(url, headers=headers, data=json.dumps(data), auth=auth)

            if response.status_code == 200:
                print(f"Successfully added user '{User_display_name}' to repository '{repo_slug}'")
            else:
                print(f"Failed to add user '{User_display_name}' to repository '{repo_slug}': {response.text}")