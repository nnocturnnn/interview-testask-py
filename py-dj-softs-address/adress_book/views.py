from django.shortcuts import render
from adress_book.forms import UserRegistration, ContactAdd, MobileNumberSave
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from adress_book.models import MobileNumber, ContactInfo
import csv
from io import TextIOWrapper
import io
import ast


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(username__exact=request.user.username)  # only logged in users saved list will be showed
        return render(request, 'user_home.html', context={'user': user})

    else:
        return render(request, 'user_home.html')


def user_login(request):
    """ Method to get a user logged in"""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            return HttpResponse("invalid username or password")

    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_registration(request):
    """ Method to get a user registered"""

    if request.method == 'POST':

        # Register user
        registration_form = UserRegistration(data=request.POST)

        if registration_form.is_valid():
            user = registration_form.save()
            user.set_password(user.password)
            user.save()

            # Logging in
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

            return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'registration.html')


def add_contact(request):
    """ Method to add contacts"""

    if request.method == 'POST':
        if request.user.is_authenticated:

            contact_info = ContactAdd(request.POST)

            # Saving the information in multiple connected tables
            if contact_info.is_valid():
                info = contact_info.save(commit=False)
                info.user_name = request.user
                info.save()

                phone = MobileNumberSave(request.POST)

                phone_number = phone.save(commit=False)
                phone_number.phone_id = info
                phone_number.save()

                return HttpResponseRedirect(reverse('index'))
            else:
                print(contact_info.errors)
                return HttpResponse("invalid data!")

        else:
            return HttpResponse("u r not logged in")
    else:
        return render(request, 'add_contact.html')


def add_phone_number(request, id):
    """ Method to add multiple phone number of a particular user"""

    contact_info = ContactInfo.objects.get(id=id)

    if request.method == "POST":
        number = MobileNumberSave(request.POST)

        if number.is_valid():
            phone_number = number.save(commit=False)
            phone_number.phone_id = contact_info
            phone_number.save()

    return render(request, 'add_phone_number.html', context={'contact_info': contact_info})


def delete_phone_number(request, id):
    """ To delete a particular phone number"""

    MobileNumber.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('index'))


def update_phone_number(request, id):
    """To update a particular phone number"""

    info = MobileNumber.objects.get(id=id)

    if request.method == "POST":
        updated_info = MobileNumberSave(request.POST)

        if updated_info.is_valid():
            MobileNumberSave(request.POST, instance=info).save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'edit_phone.html', context={'info': info})


def update_contact_info(request, id):
    """To update or edit contact info"""

    info = ContactInfo.objects.get(id=id)

    if request.method == "POST":
        updated_info = ContactAdd(request.POST)

        if updated_info.is_valid():
            ContactAdd(request.POST, instance=info).save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'edit_contacts.html', context={'info': info})


def delete_contact_info(request, id):
    """ To delete a particular Contact info"""

    ContactInfo.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('index'))


def upload_csv(request):
    if request.POST and request.FILES:

        file = TextIOWrapper(request.FILES['csv_file'].file, encoding=request.encoding)
        data = csv.reader(file)
        for row in data:
            full_name = row[0]
            nick_name = row[1]
            address = row[2]
            date_of_birth = row[3]
            phone_numbers = ast.literal_eval(row[4])  # string into list

            contact_info = ContactInfo(full_name=full_name, nick_name=nick_name, address=address,
                                       date_of_birth=date_of_birth)
            contact_info.user_name = request.user
            contact_info.save()
            # print(phone_numbers, type(phone_numbers))

            for phone_number in phone_numbers:
                phone = MobileNumber(phone_number=phone_number)

                phone.phone_id = contact_info
                # print(phone_number)
                phone.save()

    return HttpResponseRedirect(reverse('index'))


def download_csv_file(request, id):
    buffer = io.StringIO()
    wr = csv.writer(buffer, quoting=csv.QUOTE_ALL)

    contacts = request.user.contactinfo_set.all()

    for contact in contacts:
        phone_numbers = contact.mobilenumber_set.all()
        phone_list = []
        for phone_number in phone_numbers:
            phone_list.append(phone_number.phone_number)

        wr.writerow([contact.full_name, contact.nick_name, contact.address, contact.date_of_birth, phone_list])

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=contacts.csv'

    return response
