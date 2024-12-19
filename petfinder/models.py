from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=100)  # จังหวัดของผู้ใช้
    profile_picture = models.ImageField(upload_to='profile', blank=True, default='profile/default_profile.jpg')
    role = models.CharField(max_length=10, choices=[('member', 'Member'), ('admin', 'Admin')], default='user')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - ({self.role})"

    class Meta:
        verbose_name = "โปรไฟล์ผู้ใช้"
        verbose_name_plural = "โปรไฟล์ผู้ใช้ทั้งหมด"


class PetAnnouncement(models.Model):
    ANNOUNCEMENT_TYPES = [
        ('lost', 'สัตว์เลี้ยงหาย'),
        ('stray', 'ตามหาเจ้าของ'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),  # ยังค้นหาอยู่
        ('resolved', 'Resolved'),  # พบสัตว์เลี้ยงแล้ว/พบเจ้าของแล้ว
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="announcer")
    name = models.CharField(max_length=100, blank=True)  # ชื่อสัตว์
    pet_type = models.CharField(max_length=10, choices=[('cat', 'แมว'), ('dog', 'สุนัข')])  # ประเภทสัตว์
    age = models.PositiveIntegerField(blank=True, null=True)  # อายุ (เดือน)
    breed = models.CharField(max_length=100, blank=True)  # สายพันธุ์
    color = models.CharField(max_length=50)  # สีของสัตว์เลี้ยง
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'ตัวผู้'), ('female', 'ตัวเมีย'), ('unknown', 'ไม่ทราบ')],
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)  # รูปภาพสัตว์เลี้ยง
    announcement_type = models.CharField(max_length=5, choices=ANNOUNCEMENT_TYPES)
    reward = models.IntegerField(
        blank=True,
        null=True
    )  # รางวัล (หน่วยเป็นจำนวนเต็มบาท)
    location = models.CharField(max_length=200)  # สถานที่
    province = models.CharField(max_length=100)  # จังหวัด
    lost_date = models.DateField(null=True, blank=True)  # วันที่หาย
    found_date = models.DateField(null=True, blank=True)  # วันที่พบ
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        reward_display = f"฿{self.reward}" if self.reward else "ไม่มีรางวัล"  # แสดงรางวัลในรูปแบบ '฿xxx'
        return f'{self.announcement_type} - {self.name}/{self.pet_type} ({self.status}) - {self.province} - {reward_display}'

    class Meta:
        verbose_name = 'ข้อมูลประกาศ'
        verbose_name_plural = 'ข้อมูลประกาศทั้งหมด'
        ordering = ['-created_at']


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="notifications")
    announcement = models.ForeignKey(PetAnnouncement, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ระบุว่าผู้ใช้อ่านการแจ้งเตือนหรือยัง