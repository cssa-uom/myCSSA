
from django.urls import path, re_path, include
from myCSSAhub import views as Views
from FinanceAPI import urls as FinanceUrls
from OrganisationMgr import  urls as OrgMgrUrls

app_name = "myCSSAhub"
urlpatterns = [
    path('home/', Views.home, name="home"),
    path('userinfo/', Views.userInfo, name="userInfo"),
    path('message/', Views.message, name="message"),
    path('login/', Views.LoginPage.as_view(), name="hub_login"),
    path('notification/notifications_list/', Views.notifications_list, name="notifications_list"),
    path('notification/notifications_form/', Views.NotificationForm.as_view(), name="notifications_form"),
    path('notification/notifications_display/', Views.notifications_display, name="notifications_display"),
    path('logout/', Views.logout_page , name='hub_logout'),
    path('register/', Views.register_guide , name='hub_reg'),
    path('regform/', Views.NewUserSignUpView.as_view() , name='hub_regform'),
    path('userinfo/create/', Views.UserProfileCreateView.as_view(), name='hub_userinfo_create'),
]

## Admin system app directory
urlpatterns += [
    path('finance/', include(FinanceUrls, namespace='FinanceAPI')),
    path('organisation/', include(OrgMgrUrls, namespace='OrganisationMgr')),
]

## Internal AJAX path
urlpatterns += [
    path('ajax/getUserAvatar/', Views.GetUserAvatar, name="ajax_getUserAvatar"),
    path('ajax/checkEmailIntegrity/', Views.CheckEmailIntegrity, name="ajax_checkEmailIntegrity"),
    path('ajax/checkPhoneIntegrity/', Views.CheckTelIntegrity, name="ajax_checkTelIntegrity"),
    path('ajax/checkStudentIdIntegrity/', Views.CheckStudentIdIntegrity, name="ajax_checkStudentIdIntegrity"),
    path('ajax/userlookup/', Views.UserLookup.as_view(), name="ajax_userLookup")
]