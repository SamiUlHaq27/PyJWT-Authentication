from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime
import jwt

encoder = 'my_secret_31241'
time_format = '%d%m%Y%H%M%S'

@api_view(["POST"])
def create_user(request):
    username:str = request.POST.get("username", None)
    password:str = request.POST.get("password", None)
    first_name:str = request.POST.get("first_name", None)
    last_name:str = request.POST.get("last_name", None)
    email:str = request.POST.get("email", None)
    
    print({
        "username":username,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "password":password
        })
    
    if(not username):
        return Response({
            'message':'username is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if(len(User.objects.filter(username=username))):
        return Response({
            'message':'username has been already taken',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    if(not password):
        return Response({
            'message':'password is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif(len(password)<8):
        return Response({
            'message':'password must be atleast 8 characters long',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        pass
        
    if(not email):
        return Response({
            'message':'email is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif(not (email.count('@') > 0 and email.endswith('.com'))):
        return Response({
            'message':'please provide correct email or do not include it in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        pass
    
    if(not last_name):
        return Response({
            'message':'last_name is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    if(not first_name):
        return Response({
            'message':'first_name is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    
    try:
        user = User()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)
        user.save()
    except Exception as e:
        print(e)
        return Response({
            'message':'Error occured'
            
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response({
        "name":username,
        "first_name":first_name,
        "last_name":last_name,
        "email":email,
        "password":password
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def authorize(request):
    username:str = request.POST.get("username", None)
    password:str = request.POST.get("password", None)
    
    if(not username):
        return Response({
            'message':'username is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    if(not password):
        return Response({
            'message':'password is not present in request',
            
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    user = authenticate(username=username, password=password)
    
    if(not user):
        return Response({
            'message':'incorrect name or password',
            
            }, status=status.HTTP_401_UNAUTHORIZED)
        
    return Response({
        'message':'authentication successfull',
        'token':jwt.encode({
            "id":user.id,
            "un":user.username,
            "cat":datetime.datetime.now().strftime(time_format)
            }, encoder, algorithm='HS256')
    }, status=status.HTTP_202_ACCEPTED)

def verify(token):
    
    if(not token):
        raise Exception('Authorization credentials are not provided')
        
    try:
        data = jwt.decode(token, encoder, algorithms=["HS256"])
    except Exception as e:
        raise Exception("Error occured")
    
    time_passed = datetime.datetime.now() - datetime.datetime.strptime(data['cat'], time_format)
    
    if(time_passed.seconds > 1800):
        raise Exception("Token expired")
    
    return data

@api_view(['GET'])
def getData(request):
    token = request.GET.get('token', False)
    print(token)
    try:
        verify(token)
    except Exception as e:
        return Response({
            'message':e.__str__()
        }, status=status.HTTP_401_UNAUTHORIZED)
        
    return Response({'message':'Data successfull'}, status=status.HTTP_202_ACCEPTED)