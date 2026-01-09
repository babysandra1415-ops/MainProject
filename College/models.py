from django.db import models
from Guest.models import *

# Create your models here.

class tbl_collegedepartment(models.Model):
    department=models.ForeignKey(tbl_department,on_delete=models.CASCADE)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE)
class tbl_collegecourse(models.Model):
    course=models.ForeignKey(tbl_course,on_delete=models.CASCADE) 
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE)

class tbl_faculty(models.Model):
    faculty_name=models.CharField(max_length=100)
    faculty_email=models.CharField(max_length=100)
    faculty_contact=models.CharField(max_length=100)
    faculty_photo=models.FileField(upload_to="Assets/CollegeDocs/Faculty/Photo/")
    faculty_password=models.CharField(max_length=100)
    faculty_status=models.IntegerField(default=0)
    faculty_accounttype=models.IntegerField(default=0)
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE)
    department=models.ForeignKey(tbl_collegedepartment,on_delete=models.CASCADE)
    faculty_doj=models.DateField(auto_now_add=True)
    faculty_bio=models.CharField(max_length=500)
    faculty_username=models.CharField(max_length=50)


class tbl_student(models.Model):
    student_name=models.CharField(max_length=100)
    student_email=models.CharField(max_length=100)
    student_contact=models.CharField(max_length=100)
    student_bio=models.CharField(max_length=300)
    student_username=models.CharField(max_length=100)
    student_status=models.IntegerField(default=0)
    student_accounttype=models.IntegerField(default=0)
    student_password=models.CharField(max_length=100)
    student_photo=models.FileField(upload_to="Assets/StudentDocs/")
    college=models.ForeignKey(tbl_college,on_delete=models.CASCADE)
    course=models.ForeignKey(tbl_collegecourse,on_delete=models.CASCADE)
    academicyear=models.ForeignKey(tbl_academicyear,on_delete=models.CASCADE)
class tbl_assignsubject(models.Model):
    subject=models.ForeignKey(tbl_subject,on_delete=models.CASCADE)
    faculty=models.ForeignKey(tbl_faculty,on_delete=models.CASCADE)