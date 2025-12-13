# api/views.py
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django_otp import user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice

@api_view(['POST'])
def login_with_2fa(request):
    username = request.data.get('username')
    password = request.data.get('password')
    otp = request.data.get('otp')  # code Google Authenticator

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Nom d’utilisateur ou mot de passe invalide'}, status=400)

    # Vérifier si l’utilisateur a un device TOTP
    if not user_has_device(user):
        return Response({'error': '2FA non configuré pour cet utilisateur'}, status=400)

    # Vérifier le code OTP
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    if not device.verify_token(otp):
        return Response({'error': 'Code OTP invalide'}, status=400)

    # Créer ou récupérer le token DRF
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})



# api/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Renvoie les informations de l'utilisateur connecté.
    """
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
    }
    return Response(data)



