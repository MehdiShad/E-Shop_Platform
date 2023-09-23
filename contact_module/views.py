from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import ContactUsForm, ContactUsModelForm, ProfileForm
from .models import ContactUs, UserProfile
from site_module.models import SiteSetting



# Create your views here.


# def contact_us_page(request):
#     # if request.method == "POST":
#     #     if request.POST['email'] == '':
#     #         return render(request, 'contact_module/contact_us_page.html', {
#     #             'has_error': True
#     #         })
#     #     return redirect(reverse('home_page'))
#     # return render(request, 'contact_module/contact_us_page.html', {
#     #     'has_error': False
#     # })
#
#     if request.method == "POST":
#         # contact_form = ContactUsForm(request.POST) #--old
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             print(contact_form.cleaned_data)
#             # contact = ContactUs(
#             #     title=contact_form.cleaned_data.get("title"),
#             #     email=contact_form.cleaned_data.get("email"),
#             #     full_name=contact_form.cleaned_data.get("full_name"),
#             #     message=contact_form.cleaned_data.get("message"),
#             #     is_read_by_admin=False,
#             # )
#             # contact.save();
#             contact_form.save()
#             return redirect('home_page')
#
#     # contact_form = ContactUsForm() #--old
#     contact_form = ContactUsModelForm()
#     return render(request, 'contact_module/contact_us_page.html', {
#         'contact_form': contact_form
#     })


class ContactUsView(View):
    def get(self, request):
        contact_form = ContactUsModelForm()
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = {
            'contact_form': contact_form,
            'site_setting': site_setting,
        }
        return render(request, 'contact_module/contact_us_page.html', context=context)

    def post(self, request):
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect('home_page')

        context = {
            'contact_form': contact_form
        }
        return render(request, 'contact_module/contact_us_page.html', context=context)



def store_file(file):
    with open('temp/image.jpg', "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)

# class CreateProfileView(View):
#     def get(self, request):
#         return render(request, 'contact_module/create_profile_page.html')
#
#     def post(self, request):
#         print(request.FILES)
#         store_file(request.FILES['profile'])
#         return redirect('/contact-us/create-profile')


# class CreateProfileView(View):
#     def get(self, request):
#         form = ProfileForm()
#         return render(request, 'contact_module/create_profile_page.html', {
#             'form': form
#         })
#
#     def post(self, request):
#         submitted_form = ProfileForm(request.POST, request.FILES)
#
#         if submitted_form.is_valid():
#             # store_file(request.FILES['profile'])
#             profile = UserProfile(image=request.FILES['user_image'])
#             profile.save()
#             return redirect('/contact-us/create-profile')
#             # submited_form.save()
#         # print(request.FILES).
#         return render(request, 'contact_module/create_profile_page.html', {
#             'form': submitted_form
#         })


class CreateProfileView(CreateView):
    template_name = 'contact_module/create_profile_page.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/contact-us/create-profile'


class ProfilesView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list_page.html'
    context_object_name = 'profiles'

