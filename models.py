from django.db import models
import os
# Create your models here.
class UserModel(models.Model):
    firstname = models.CharField(max_length=100)
    lastname =  models.CharField(max_length=100)
    email =  models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.firstname + " " + self.lastname
    
    class Meta:
        db_table = "UserModel"  
    
class UploadFileModel(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=os.path.join('static', 'Files'))
    uploaderemail = models.EmailField()
    file_name = models.CharField(max_length=255)  # Store the original file name
    encrypted_data = models.BinaryField()  # Store the encrypted file content
    keyword = models.CharField(max_length=255)  # Store the encrypted keyword
    privatekey = models.BinaryField()  # Store optional attributes (for ABE)
    Publickey = models.BinaryField()
    hash =  models.BinaryField(null=True)
    status = models.CharField(max_length=255,default='Encrypted')
    auditstatus = models.CharField(max_length=100,default='pending')


    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = "UploadFileModel"


class RequestFileModel(models.Model):
    fid = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=os.path.join('static', 'DECFiles'))
    uploaderemail = models.EmailField()
    file_name = models.CharField(max_length=255)  # Store the original file name
    encrypted_data = models.TextField()  # Store the encrypted file content
    keyword = models.CharField(max_length=255)  # Store the encrypted keyword
    privatekey = models.BinaryField()  # Store optional attributes (for ABE)
    Publickey = models.BinaryField()
    hash =  models.BinaryField(null=True)
    status = models.CharField(max_length=255,default='Encrypted')
    Requesteremail = models.CharField(max_length=100)
    Rname = models.CharField(max_length=100)
    key = models.IntegerField(null=True)

    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = "RequestFileModel"
