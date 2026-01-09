from django.urls import path,include
from Student import views
app_name="Student"

urlpatterns = [
  path('HomePage/',views.HomePage,name="HomePage"), 
  path('MyProfile/',views.MyProfile,name="MyProfile"),
  path("EditProfile/",views.EditProfile,name="EditProfile"),
  path('topublic/<int:pid>',views.topublic,name="topublic"),
  path('toprivate/<int:prid>',views.toprivate,name="toprivate"),
  path("ChangePassword/",views.ChangePassword,name="ChangePassword"), 
  path("ViewNotes/",views.ViewNotes,name="ViewNotes"),
  path("AjaxCourse/",views.AjaxCourse,name="AjaxCourse"),
  path('Post/',views.Post,name="Post"),
  path('delpost/<int:did>',views.delpost,name="delpost"),
  path('ViewPost/',views.ViewPost,name="ViewPost"), 
  path('likepost/<int:pid>',views.likepost,name="likepost"),
]