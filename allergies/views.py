from django.shortcuts import render


# Create your views here.
def allergies_list(request):
    return render(request, "allergies/allergies_list.html")


# if request.method == 'POST':
# process request: Handle form submission for adding new allergies
