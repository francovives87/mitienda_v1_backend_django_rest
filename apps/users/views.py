from django.shortcuts import render
from .renderers import UserRenderer
from rest_framework import generics, status, views, permissions
from .serializers import (
    RegisterSerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserDataSerializer,
    UserDataPersonalSerializer,
    VisitorSerializer,
    SetUserOnVisitorSerializer,
    GetVisitorByUserSerializer,
    VisitorManagerSerializer,
)
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from .models import User, UserPersonalData, Visitor
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail, EmailMessage  # funcion para enviar emails
from django.contrib.sites.shortcuts import get_current_site
from .permissions import IsHe
from django.conf import settings


class TestMail(APIView):
    def get(self, request):
        # send mail
        ##envio de email
        codigo='123'
        user="franco"
        user_email='franco_vives@hotmail.com'
        current_site = 'mitienda.app'    
        asunto = 'Confirmacion de Email'
        absurl = 'https://'+current_site+"/api/v1.0/email-verify/?codigo="+str(codigo)+"&coderef="+str(user)
        mensaje = 'Bienvenido/a a mitienda.app! \n Gracias por registrarse. \n Haga click en el siguiente enlace para verificar su correo electronico: \n' + absurl
        email_remitente = settings.EMAIL_HOST_USER
        #
        send_mail(asunto,mensaje,email_remitente,[user_email])
        #redirigiar a pantalla de validacion de codigo
        return Response({"msj": "ok"}, status=HTTP_200_OK)


# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    """ renderer_classes = (UserRenderer) """

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        codigo = user.codregistro
        ##envio de email
        current_site = get_current_site(request).domain
        url = 'https://mitienda.app/main/account/login/'        
        asunto = 'Confirmacion de Email'
        absurl = url+"?codigo="+str(codigo)+"&coderef="+str(user.id)
        mensaje = 'Bienvenido/a a mitienda.app! \n Gracias por registrarse. \n Haga click en el siguiente enlace para verificar su correo electronico: \n' + absurl
        email_remitente = settings.EMAIL_HOST_USER
        #
        send_mail(asunto,mensaje,email_remitente,[user.email])
        #redirigiar a pantalla de validacion de codigo

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        codigo = request.GET.get("codigo")
        user_id = request.GET.get("coderef")
        check = User.objects.filter(id=user_id, codregistro=codigo)
        if check:
            check.update(is_verified=True)
            return Response(
                {"message": "Usuario verificado con exito!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Algo salio mal"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserData(RetrieveAPIView):
    serializer_class = UserDataSerializer
    permission_classes = (permissions.IsAuthenticated, IsHe)
    lookup_field = "id"

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        return User.objects.filter(id=id)


class UserPersonalDataView(ListAPIView):
    serializer_class = UserDataPersonalSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk", None)
        return UserPersonalData.objects.filter(user=pk,).order_by(
            "-created"
        )[:1]


class CreatePersonalDataView(CreateAPIView):
    serializer_class = UserDataPersonalSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UpdatePersonalDataView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDataPersonalSerializer
    queryset = UserPersonalData.objects.all()


class CreateVisitor(CreateAPIView):
    serializer_class = VisitorSerializer


class GetVisitor(RetrieveAPIView):
    serializer_class = VisitorSerializer
    queryset = Visitor.objects.all()


class SetUserOnVisitor(UpdateAPIView):
    serializer_class = SetUserOnVisitorSerializer
    queryset = Visitor.objects.all()


class GetVisitorByUser(ListAPIView):
    serializer_class = GetVisitorByUserSerializer

    def get_queryset(self):
        user = self.request.query_params.get("user", "")
        return Visitor.objects.filter(user=user).order_by("-created")


class VisitorManager(APIView):
    serializer_class = VisitorManagerSerializer

    def post(self, request, *args, **kwargs):

        serializer = VisitorManagerSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        visitor_request = int(serializer.validated_data["visitor"])

        print(visitor_request)

        resp = {"status": None, "visitor": None}

        existe_visitor = Visitor.objects.filter(id=visitor_request)

        if existe_visitor.exists():
            resp = {"status": "exists", "visitor": visitor_request}
            return Response(resp, status=HTTP_200_OK)
        else:
            create_visitor = Visitor.objects.create()
            print("create_visitor")
            print(create_visitor.id)
            resp = {"status": "created", "visitor": int(create_visitor.id)}
            return Response(resp, status=HTTP_200_OK)
