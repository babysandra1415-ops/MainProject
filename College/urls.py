from django.urls import path,include
from College import views
app_name="College"

urlpatterns = [
  path('HomePage/',views.HomePage,name="HomePage"),  
  path('CollegeProfile/',views.CollegeProfile,name="CollegeProfile"),
  path("EditProfile/",views.EditProfile,name="EditProfile"),
  path("ChangePassword/",views.ChangePassword,name="ChangePassword"),
  path('FacultyRegistration/',views.FacultyRegistration,name="FacultyRegistration"),
  path('delfaculty/<int:did>',views.delfaculty,name="delfaculty"),
  path('CollegeDepartment/',views.CollegeDepartment,name="CollegeDepartment"),
  path('deldepartment/<int:did>',views.deldepartment,name="deldepartment"),
  path('CollegeCourse/',views.CollegeCourse,name="CollegeCourse"),
  path('delcourse/<int:did>',views.delcourse,name="delcourse"),
  path('AjaxCollegeCourse/',views.AjaxCollegeCourse,name="AjaxCollegeCourse"),
  path('AssignSubject/<int:fid>',views.AssignSubject,name="AssignSubject"),
  path('AjaxSubject/',views.AjaxSubject,name="AjaxSubject"),
  path('delsubject/<int:did>',views.delsubject,name="delsubject"),
  path('Post/',views.Post,name="Post"),
  path('delpost/<int:did>',views.delpost,name="delpost"),
]