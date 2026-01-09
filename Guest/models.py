from django.db import models
from Admin.models import *



class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    user_contact=models.CharField(max_length=50)
    user_address=models.CharField(max_length=80)
    user_password=models.CharField(max_length=50)
    user_photo=models.FileField(upload_to="Assets/UserDocs/")
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
class tbl_college(models.Model):
    college_name=models.CharField(max_length=100)
    college_email=models.CharField(max_length=100)
    college_password=models.CharField(max_length=100)
    college_address=models.CharField(max_length=100)
    college_photo=models.FileField(upload_to="Assets/CollegeDocs/Photo/")
    college_logo=models.FileField(upload_to="Assets/CollegeDocs/Logo/")
    college_proof=models.FileField(upload_to="Assets/CollegeDocs/Proof/")
    college_contact=models.CharField(max_length=100)
    college_status=models.IntegerField(default=0)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)

