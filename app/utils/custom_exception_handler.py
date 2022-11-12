from rest_framework.views import exception_handler
import http.client

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        #9b043af4161276899b8b08e6e56f5bf091c968a7
        if response.data.get('detail'):
            if "invalid token" in response.data['detail'].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 1
            elif "authentication credentials were not provided" in response.data['detail'].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 2
        elif response.data.get('non_field_errors'):        
            if "unable to authenticate with provided credentials" in response.data['non_field_errors'][0].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 3
        elif response.data.get('password'):        
            if "this field may not be blank" in response.data['password'][0].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 4
            elif "ensure this field has at least 5 characters" in response.data['password'][0].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 5
        elif response.data.get('email'):        
            if "this field may not be blank" in response.data['email'][0].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 6
            elif "enter a valid email address" in response.data['email'][0].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 7
        elif response.data.get('name'):        
            if "this field may not be blank" in response.data['name'][0].lower():
                response.data['status_code'] = response.status_code
                response.data['reason'] = http.client.responses.get(response.status_code)
                response.data['status'] = 8


    return response