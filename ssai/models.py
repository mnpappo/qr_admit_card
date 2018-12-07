from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os


# Create your models here.
class StudentInfo(models.Model):
    student_name = models.CharField(max_length=200, help_text="Student's Full Name")
    roll_no = models.CharField(max_length=50, help_text="Student's Roll Number", unique=True)
    dob = models.DateField(help_text="Student's Date of Birth", blank=True, null=True)
    exam_date_time = models.DateTimeField(help_text="Exam Date and Time", blank=True, null=True)
    sit_location = models.CharField(max_length=200,help_text="Exam Sit and Hall Location", default="")
    admit_pic = models.ImageField(help_text="Students Picture on Admit Card", upload_to = 'pic_folder/', default = 'pic_folder/default.png')

    qrcode_img = models.ImageField(upload_to='qr_code/', blank=True, null=True, editable=False)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        qr_link = 'http://192.168.1.102:8000/ssai/'+str(self.pk)
        qr.add_data(qr_link)
        qr.make(fit=True)

        img = qr.make_image()
        temp_handle = BytesIO()
        img.save(temp_handle, 'png')
        temp_handle.seek(0)
        suf = SimpleUploadedFile('qr.png', temp_handle.read(), content_type='image/png')
        self.qrcode_img.save('qr.png', suf, save=False )
    
    def save(self, *args, **kwargs):
        self.generate_qrcode()

        return super(StudentInfo, self).save(*args, **kwargs)
    
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.admit_pic) )
    image_tag.short_description = 'Image Preview'

    def qrimage_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.qrcode_img) )
    qrimage_tag.short_description = 'Qr Image'



    # def generate_qr_code(self):
    #     qr = qrcode.QRCode(
    #         version=1,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=4,
    #     )
    #     qr.add_data(self.roll_no)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color="black", back_color="white")
    #     img.save('/media/qr_code.png')
    #     img.show()
    #     return mark_safe('<img src="%s" width="150" height="150" />' % ('/media/qr_code.png') )

    def __str__(self):
        return self.student_name    