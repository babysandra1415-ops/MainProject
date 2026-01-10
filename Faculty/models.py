from django.db import models
from Admin.models import *
from College.models import *
from Guest.models import *

# Create your models here.

class tbl_notes(models.Model):
    notes_description=models.CharField(max_length=400)
    notes_file=models.FileField(upload_to="Assets/FacultyDocs/Notes/")
    notes_status=models.IntegerField(default=0)
    subject=models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE)
class tbl_post(models.Model):
    post_description=models.CharField(max_length=400)
    post_photo=models.FileField(upload_to="Assets/FacultyDocs/Posts/")
    post_status=models.IntegerField(default=0)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True)
    post_type=models.IntegerField(default=0)
    post_pd=models.DateField(auto_now_add=True)
class tbl_like(models.Model):
    post=models.ForeignKey(tbl_post,on_delete=models.CASCADE)
    student=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True)


class tbl_comment(models.Model):
    comment_content=models.CharField(max_length=500)
    comment_date=models.DateField(auto_now_add=True)
    comment_status=models.IntegerField(default=0)
    post=models.ForeignKey(tbl_post,on_delete=models.CASCADE)
    student=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True)


class tbl_commentreply(models.Model):
    commentreply_content=models.CharField(max_length=500)
    commentreply_date=models.DateField(auto_now_add=True)
    commentreply_status=models.IntegerField(default=0)
    comment=models.ForeignKey(tbl_comment,on_delete=models.CASCADE,related_name="replies")
    student=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True)

class tbl_follow(models.Model):
    follow_status=models.IntegerField(default=0)
    follow_date=models.DateField(auto_now_add=True)
    fromstudent=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True,related_name="from_student")
    tostudent=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True,related_name="to_student")
    fromfaculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True,related_name="from_faculty")
    tofaculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True,related_name="to_student")
    fromcollege=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True,related_name="from_college")
    tocollege=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True,related_name="to_college")
