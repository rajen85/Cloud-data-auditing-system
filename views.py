from django.shortcuts import render, redirect

from rest_framework import generics
from .models import *
from .serializers import UserSerializer
from django.core.paginator import Paginator
from django.contrib import messages

import pickle
from phe import paillier
import os
import random
from django.shortcuts import redirect
from django.contrib import messages
from .models import RequestFileModel
from django.core.mail import send_mail
import hashlib
import os
import pickle
from phe import paillier


# API View for User registration
class UserCreateAPIView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

# API View for User listing (GET) and creation (POST)
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

# API View for retrieving, updating, or deleting a single user
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def userregister(request):
    if request.method == 'POST':
        firstname = request.POST['firstName']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        phone  = request.POST['phone']
        
        if password != confirmpassword:
            messages.success(request, 'Password and Confirm Password does not match!')
            return redirect('userregister')
        else:
            if UserModel.objects.filter(email=email).exists():
                messages.success(request, 'Email already exists!')
                return redirect('userregister')
            else:
                user = UserModel(firstname=firstname, lastname=lastname, email=email, password=password, phone=phone)
                user.save()
                messages.success(request, 'User Registered Successfully!')
                return redirect('userregister')
    return render(request, 'userregister.html')

def userlogin(request):
    # UserModel.objects.all().delete()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = UserModel.objects.filter(email=email, password=password).exists()
        if user:
            data = UserModel.objects.get(email=email)
            request.session['email'] = email
            request.session['login'] = 'user'
            request.session['name'] = data.firstname+" "+data.lastname
            return redirect('home')
        else:
            messages.success(request, 'Invalid Email or Password!')
            return redirect('userlogin')
        
    return render(request, 'userlogin.html')

def home(request):
    login = request.session['login']
    return render(request, 'home.html',{'login':login})


def logout(request):
    del request.session['email']
    del request.session['login']
    del request.session['name']
    return redirect('index')




# Function to hash text using SHA-256
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Convert text to numeric representation (ASCII values)
def text_to_numeric(text):
    return [ord(char) for char in text]

# Encrypt text using Paillier
def encrypt_text(text, pub_key):
    numeric_text = text_to_numeric(text)
    encrypted_text = [pub_key.encrypt(num) for num in numeric_text]
    return encrypted_text

# Encrypt hash using Paillier
def encrypt_hash(text_hash, pub_key):
    numeric_hash = int(text_hash, 16)  # Convert hexadecimal hash to integer
    encrypted_hash = pub_key.encrypt(numeric_hash)
    return encrypted_hash
import hashlib
import os
import pickle
from phe import paillier
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UploadFileModel

# Function to hash text using SHA-256
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Convert text to numeric representation (ASCII values)
def text_to_numeric(text):
    return [ord(char) for char in text]

# Encrypt text using Paillier
def encrypt_text(text, pub_key):
    numeric_text = text_to_numeric(text)
    encrypted_text = [pub_key.encrypt(num) for num in numeric_text]
    return encrypted_text

# Encrypt hash using Paillier
def encrypt_hash(text_hash, pub_key):
    numeric_hash = int(text_hash, 16)  # Convert hexadecimal hash to integer
    encrypted_hash = pub_key.encrypt(numeric_hash)
    return encrypted_hash


from django.core.files.base import ContentFile

# Upload and encrypt file
def uploadfiles(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        filename = request.POST.get('filename')
        file_name = file.name
        login = request.session.get('login')
        email = request.session.get('email')
        name = request.session.get('name')

        # Generate Paillier keys
        public_key, private_key = paillier.generate_paillier_keypair()

        # Save the uploaded file temporarily
        temp_file_path = os.path.join('static', 'Files', filename)
        with open(temp_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Read the file content as binary
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()

        # Convert the binary content to string for hashing
        try:
            text_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            messages.error(request, 'Unable to decode file content. Please upload a valid text file.')
            return redirect('uploadfiles')

        # Generate hash of the file content
        text_hash = hash_text(text_content)

        # Encrypt the file content and hash
        encrypted_content = encrypt_text(text_content, public_key)
        encrypted_hash = encrypt_hash(text_hash, public_key)

        # Save the encrypted data in a new file (as binary)
        encrypted_file_path = os.path.join('static', 'Files', f'encrypted_{filename}')
        with open(encrypted_file_path, 'wb') as encrypted_file:
            for encrypted_char in encrypted_content:
                encrypted_file.write(str(encrypted_char.ciphertext()).encode() + b'\n')

        # Store keys as bytes using pickle
        UploadFileModel.objects.create(
            name=name,
            uploaderemail=email,
            file=encrypted_file_path,
            keyword=filename,
            file_name=file_name,
            encrypted_data=pickle.dumps(encrypted_content),  # Ensure this is in bytes
            hash=pickle.dumps(encrypted_hash),  # Ensure this is in bytes
            privatekey=pickle.dumps(private_key),  # Store serialized private key as bytes
            Publickey=pickle.dumps(public_key)  # Store serialized public key as bytes
        )

        messages.success(request, 'File uploaded and encrypted successfully!')
        return redirect('uploadfiles')

    return render(request, 'uploadfiles.html', {'login': request.session.get('login')})


def viewfiles(request):
    # UploadFileModel.objects.all().delete()
    # RequestFileModel.objects.all().delete()
    login =request.session['login']
    email =request.session['email']
    name =request.session['name']
    files = UploadFileModel.objects.all()
    paginator = Paginator(files, 2) 
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'viewfiles.html',{'data':page_data,'login':login,'email':email,'name':name})


def myfiles(request):
    login =request.session['login']
    email =request.session['email']
    files = UploadFileModel.objects.filter(uploaderemail=email)
    paginator = Paginator(files, 2)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'myfiles.html',{'data':page_data,'login':login,'email':email})


def sendauditrequest(request, id):
    login =request.session['login']
    email =request.session['email']
    file = UploadFileModel.objects.get(id=id)
    file.auditstatus = 'Audit Request Sent to PTPC'
    file.save()
    messages.success(request, 'Audit Request Sent Successfully!')
    return redirect('myfiles')



def cloudlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if email == os.environ.get('CLOUD_EMAIL', '') and password == os.environ.get('CLOUD_PASSWORD', ''):
            request.session['email'] = email
            request.session['login'] = 'csp'
            request.session['name'] = 'cloud'
            return redirect('home')
        else:
            messages.success(request, 'Invalid Email or Password!')
            return redirect('cloudlogin')
    return render(request, 'cloudlogin.html')

def ptpclogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if email == os.environ.get('PTPC_EMAIL', '') and password == os.environ.get('PTPC_PASSWORD', ''):
            request.session['email'] = email
            request.session['login'] = 'ptpc'
            request.session['name'] = 'ptpc'
            return redirect('home')
        else:
            messages.success(request, 'Invalid Email or Password!')
            return redirect('ptpclogin')
    return render(request, 'ptpclogin.html')

def viewauditrequest(request):
    login =request.session['login']
    files = UploadFileModel.objects.filter(auditstatus='Audit Request Sent to PTPC')
    paginator = Paginator(files, 2)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'viewauditrequest.html',{'data':page_data,'login':login})


def sendchallange(request,id):
    login =request.session['login']
    email =request.session['email']
    file = UploadFileModel.objects.get(id=id)
    file.auditstatus = 'Challange Send To Cloud'
    file.save()
    messages.success(request, 'Challange Send To Cloud Successfully!')
    return redirect('viewauditrequest')


def viewchallanges(request):
    login =request.session['login']
    files = UploadFileModel.objects.filter(auditstatus='Challange Send To Cloud')
    paginator = Paginator(files, 2)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'viewchallanges.html',{'data':page_data,'login':login}) 


def sendproof(request,id):
    login =request.session['login']
    email =request.session['email']
    file = UploadFileModel.objects.get(id=id)
    file.auditstatus = 'Proof Sent'
    file.save()
    messages.success(request, 'Proof Sent To PTPC Successfully!')
    return redirect('viewchallanges')


def cloudresponses(request):
    login =request.session['login']
    files = UploadFileModel.objects.filter(auditstatus='Proof Sent')
    paginator = Paginator(files, 2)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'cloudresponses.html',{'data':page_data,'login':login}) 

def verifyproof(request,id):
    login =request.session['login']
    email =request.session['email']
    file = UploadFileModel.objects.get(id=id)
    file.auditstatus = 'Verified'
    file.save()
    messages.success(request, 'Proof Verified Successfully!')
    return redirect('cloudresponses')

def sendfilerequest(request,id):
    # RequestFileModel.objects.all().delete()
    name =request.session['name']
    email =request.session['email']
    file = UploadFileModel.objects.get(id=id)
    if RequestFileModel.objects.filter(Requesteremail=email,fid=file.id).exists():
        
        messages.error(request, 'You Already Requested This File!')
        return redirect('viewfiles')
    else:
        data = RequestFileModel.objects.create(
            fid = file.id,
            file = file.file,
            name=file.name,
            uploaderemail=file.uploaderemail,
            file_name = file.file_name,
            encrypted_data = file.encrypted_data,
            keyword = file.keyword,
            privatekey = file.privatekey,
            Publickey = file.Publickey,
            hash = file.hash,
            status = file.status,
            Requesteremail = email,
            Rname = name        
        )
        data.save()
        messages.success(request, 'File Request Sent Successfully!')
    
        return redirect('viewfiles')
    

def viewfilerequests(request):
    login =request.session['login']
    email =request.session['email']
    data = RequestFileModel.objects.filter(uploaderemail=email,status='Encrypted')
    paginator = Paginator(data, 2)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'viewfilerequests.html',{'data':page_data,'login':login})



# Convert numeric representation back to text
def numeric_to_text(numeric_list):
    return ''.join([chr(num) for num in numeric_list])

# Decrypt text using Paillier
def decrypt_text(encrypted_text, priv_key):
    decrypted_numeric = [priv_key.decrypt(c) for c in encrypted_text]
    return numeric_to_text(decrypted_numeric)
# Decrypt file
def decryptfile(request, id):
    login = request.session.get('login')
    email = request.session.get('email')

    # Get the file record from the database
    file_record = RequestFileModel.objects.get(id=id)

    # Deserialize the public and private keys from binary data
    public_key = pickle.loads(file_record.Publickey)  # Load from bytes
    private_key = pickle.loads(file_record.privatekey)  # Load from bytes

    # Read the encrypted file content as binary
    file_path = file_record.file.path
    with open(file_path, 'rb') as f:
        encrypted_content = f.readlines()

    # Convert encrypted lines (ciphertext strings) back to Paillier EncryptedNumber objects
    encrypted_text = [paillier.EncryptedNumber(public_key, int(line.strip())) for line in encrypted_content]

    # Decrypt the encrypted text
    decrypted_text = decrypt_text(encrypted_text, private_key)

    # Define the path to store the decrypted file
    decrypted_file_path = os.path.join('static', 'DECFiles', f'decrypted_{file_record.file_name}')

    # Write the decrypted text to the new file (as binary)
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_text.encode('utf-8'))



    key =random.randint(1111, 9999)
    print(key)
    file_record.status = 'Decrypted'
    file_record.file = decrypted_file_path
    file_record.encrypted_data = decrypted_text
    file_record.key = key
    file_record.save()

    email_subject = 'Key Details'
    email_message = f'Hello {file_record.Rname},\n\nWelcome To Our Website!\n\nHere are your Key details:\nEmail: {file_record.Requesteremail}\nKey: {file_record.key}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
    send_mail(email_subject, email_message, os.environ.get('EMAIL_HOST_USER', ''), [file_record.Requesteremail])

    # Notify the user that the file has been decrypted successfully
    messages.success(request, 'File decrypted successfully!')
    return redirect('viewfilerequests')


def viewresponses(request):
    login = request.session.get('login')
    email = request.session.get('email')
    data = RequestFileModel.objects.filter(Requesteremail=email,status='Decrypted')
    paginator = Paginator(data, 2)
    page_number = request.GET.get('page')
    page_data = paginator.get_page(page_number)
    return render(request, 'viewresponses.html',{'data':page_data,'login':login})

from django.http import FileResponse

def downloadfile(request, id):
    login = request.session['login']
    email = request.session['email']
    context = RequestFileModel.objects.get(id=id)

    if request.method == 'POST':
        key = request.POST['key']
        # print(type(key), context.key)
        if int(key) == int(context.key):
            file_path = context.file.path  # Get the file path
            file_name = context.file_name.split('/')[-1]  # Extract the file name
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            return response
        else:
            messages.success(request, 'You Entered key is Wrong')
            return redirect('downloadfile', id)

    return render(request, 'downloadfile.html', {'login': login, 'id': id})

