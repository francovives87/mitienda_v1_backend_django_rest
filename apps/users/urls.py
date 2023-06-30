from django.urls import path
from .views import (
    RegisterView,
    LoginAPIView,
    VerifyEmail,
    UserData,
    CreatePersonalDataView,
    UserPersonalDataView,
    UpdatePersonalDataView,
    CreateVisitor,
    GetVisitor,
    SetUserOnVisitor,
    GetVisitorByUser,
    VisitorManager,
    TestMail
)

urlpatterns = [
    path("api/v1.0/register/", RegisterView.as_view(), name="register"),
    path("api/v1.0/login/", LoginAPIView.as_view(), name="login"),
    path("api/v1.0/email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("api/v1.0/user/<int:id>", UserData.as_view(), name="UserData"),
    path(
        "api/v1.0/user/personal/",
        CreatePersonalDataView.as_view(),
        name="UserPersonalDataCreate",
    ),
    path(
        "api/v1.0/user/personal/<pk>",
        UserPersonalDataView.as_view(),
        name="UserPersonalData",
    ),
    path(
        "api/v1.0/user/personal/update/<pk>",
        UpdatePersonalDataView.as_view(),
        name="UserPersonalDataUpdate",
    ),
    path(
        "api/v1.0/user/personal/update/<pk>",
        UpdatePersonalDataView.as_view(),
        name="UserPersonalDataUpdate",
    ),
    path(
        "api/v1.0/user/visitor/create/",
        CreateVisitor.as_view(),
        name="CreateVisitor",
    ),
    path(
        "api/v1.0/user/visitor/<pk>",
        GetVisitor.as_view(),
        name="GetVisitor",
    ),
    path(
        "api/v1.0/user/visitor/set/<pk>",
        SetUserOnVisitor.as_view(),
        name="SetUserOnVisitor",
    ),

    path(
        "api/v1.0/user/visitor/get/",
        GetVisitorByUser.as_view(),
        name="GetVisitorByUser",
    ),

    path(
        "api/v1.0/user/visitor/manager/",
        VisitorManager.as_view(),
        name="VisitorManager",
    ),
#####test mail
path(
        "api/v1.0/email/test/",
        TestMail.as_view(),
        name="TestMail",
    ),

]
