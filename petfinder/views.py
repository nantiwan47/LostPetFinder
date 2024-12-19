from django.shortcuts import render
from django.views.generic import ListView
from .models import *

# แสดงรายการประกาศสัตว์เลี้ยงหาย
def lost_pet_list(request):
    # ดึงข้อมูลประกาศเฉพาะที่เป็นประเภท 'สัตว์เลี้ยงหาย'
    lost_announcements = PetAnnouncement.objects.filter(announcement_type='lost').order_by('-created_at')
    return render(request, 'lost_pet_list.html', {
        'lost_list': lost_announcements})

def find_list(request):
    return render(request, 'find_list.html')
