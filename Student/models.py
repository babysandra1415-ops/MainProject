from django.db import models

from College.models import *
from Faculty.models import *




# Create your models here.

class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=400)
    complaint_content=models.CharField(max_length=1400)
    complaint_reply=models.CharField(max_length=1400,null=True)
    complaint_status=models.IntegerField(default=0)
    complaint_date=models.DateField(auto_now_add=True)
    student=models.ForeignKey(tbl_student,on_delete=models.CASCADE,null=True)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,null=True)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE,null=True)
    post=models.ForeignKey(tbl_post,on_delete=models.CASCADE,null=True)
class tbl_chat(models.Model):
    chat_content = models.CharField(max_length=500)
    chat_time = models.DateTimeField()
    chat_file = models.FileField(upload_to='ChatFiles/')
    student_from = models.ForeignKey(tbl_student,on_delete=models.CASCADE,related_name="student_from",null=True)
    student_to = models.ForeignKey(tbl_student,on_delete=models.CASCADE,related_name="student_to",null=True)
    faculty_from = models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,related_name="faculty_from",null=True)
    faculty_to = models.ForeignKey(tbl_faculty,on_delete=models.CASCADE,related_name="faculty_to",null=True)
    college_from = models.ForeignKey(tbl_college,on_delete=models.CASCADE,related_name="college_from",null=True)
    college_to = models.ForeignKey(tbl_college,on_delete=models.CASCADE,related_name="college_to",null=True)
