from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
import os
from events.models import Events, Event_Participants
from users.models import Organisation


# Create your views here.
def uploadsView (request):
    event = Events.objects.all().get(id=1)
    context = {
        "page_name": "Upload Documents",
        "file": event.file,
    }
    
    if request.POST:
        if 'org_submit' in request.POST:
            print("org_submit")
            org = Organisation()
            org.name = request.POST['org_name']
            org.year = request.POST['org_year']
            org.internal = request.POST['org_internal']
            org.file = request.FILES['org_file']
            org.save()
        elif 'event_submit' in request.POST:
            event = Events()
            
    return render(request, "uploads.html", context)

def download_excel(request, template_name):
    file_path = os.path.join(settings.BASE_DIR, 'media/template', template_name+'.xlsx')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response