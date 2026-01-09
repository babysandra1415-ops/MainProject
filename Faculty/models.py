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