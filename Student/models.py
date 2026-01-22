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
