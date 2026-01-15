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
  path('ViewPost/',views.ViewPost,name="ViewPost"),
  path('likepost/<int:pid>',views.likepost,name="likepost"),
  path('Comment/<int:cid>',views.Comment,name="Comment"),
  path('FollowF/<int:fid>',views.FollowF,name="FollowF"),
  path('FollowC/<int:Cid>',views.FollowC,name="FollowC"),
  path('FacultyList/',views.FacultyList,name="FacultyList"),
  path('CollegeList/',views.CollegeList,name="CollegeList"),
  path('StudentList/',views.StudentList,name="StudentList"),
  path('FollowS/<int:Sid>',views.FollowS,name="FollowS"),
]