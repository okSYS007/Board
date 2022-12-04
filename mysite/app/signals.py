import os
from random import randint
from django.shortcuts import redirect

from django.db.models.signals import pre_delete, post_save
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from .models import Announcement, Files, User, OneTimeCode

from django.template.loader import render_to_string

@receiver(pre_delete, sender=Announcement)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    objFiles = Files.objects.filter(Announcement = instance)
    for file in objFiles:
        if os.path.isfile(file.File.path):
            os.remove(file.File.path)


@receiver(post_save, sender = User)
def confirm_code_registration(sender, instance, created, **kwargs):
    """
    Send confirmation code to new users
    """
    if created:
        code_Obj = OneTimeCode.objects.create(User = instance)
        #doing loop with hope that old cods will be deleted =)
        CodeAccepted = False
        while not CodeAccepted:
            rand_code = randint(0, 9999)
       
            if len(str(rand_code)) == 1:
                rand_code = "000" + str(rand_code);
            elif len(str(rand_code)) == 2:
                rand_code = "00" + str(rand_code);
            elif len(str(rand_code)) == 3:
                rand_code = "0" + str(rand_code);
            else:
                rand_code = str(rand_code)

            if not OneTimeCode.objects.filter(Code = rand_code).exists():
                CodeAccepted = True
                code_Obj.Code = rand_code;
                code_Obj.save()

        html_content = render_to_string( 
            'account/register_code_email.html',
            {
                'register_code': rand_code,
                'user': instance.username,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Код поддтверждения',
            body="", #  это то же, что и message
            from_email='ViacheslavDan803@gmail.com',
            to=[instance.email], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html

        msg.send() # отсылаем

    return redirect('/announce/')
