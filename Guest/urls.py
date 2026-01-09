from django.urls import path,include
from Guest import views
app_name="Guest"

urlpatterns = [
  path('UserRegistration/',views.UserRegistration,name="UserRegistration"), 
  path('CollegeRegistration/',views.CollegeRegistration,name="CollegeRegistration"), 
  path('Login/',views.Login,name="Login"),
  path('AjaxPlace/',views.AjaxPlace,name="ajaxplace"),
  path('StudentRegistration/',views.StudentRegistration,name="StudentRegistration"),
  path('AjaxCourse/',views.AjaxCourse,name="AjaxCourse"),
  path('AjaxDepartment/',views.AjaxDepartment,name="AjaxDepartment"),
 
  
]