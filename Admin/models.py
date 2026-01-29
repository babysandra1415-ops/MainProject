from django.db import models


# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)
class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=100)
    admin_email=models.CharField(max_length=100)
    admin_password=models.CharField(max_length=100)
class tbl_category(models.Model):
    category_name=models.CharField(max_length=100)
class tbl_place(models.Model):
    place_name=models.CharField(max_length=100)  
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
class tbl_department(models.Model):
    department_name=models.CharField(max_length=100)
class tbl_semester(models.Model):
    semester_name=models.CharField(max_length=50)
class tbl_academicyear(models.Model):
    academicyear_year=models.CharField(max_length=50)
class tbl_course(models.Model):
    course_name=models.CharField(max_length=100)  
    department=models.ForeignKey(tbl_department,on_delete=models.CASCADE)
class tbl_subject(models.Model):
    subject_name=models.CharField(max_length=100)
    course=models.ForeignKey(tbl_course,on_delete=models.CASCADE)
    semester=models.ForeignKey(tbl_semester,on_delete=models.CASCADE)
class tbl_news(models.Model):
    news_description=models.CharField(max_length=1400)
    news_file=models.FileField(upload_to="Assets/AdminDocs/news/file",null=True)
    news_photo=models.FileField(upload_to="Assets/AdminDocs/news/photo",null=True)
    news_status=models.IntegerField(default=0)
    