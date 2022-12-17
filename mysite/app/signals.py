import os
from random import randint
from django.shortcuts import redirect

from django.db.models.signals import pre_delete, post_save
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from .models import Announcement, Files, OneTimeCode, MyUser, Comments

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

@receiver(post_save, sender = MyUser)
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

@receiver(post_save, sender = Comments)
def email_response_to_user(sender, instance, created, **kwargs):
    """
    Send email for accepted comment
    """
    if created:
        html_content = render_to_string( 
            'announce/comment_added.html',
            {
                'post_id': instance.Announcement_id,
                'post_title': instance.Announcement.Announcement_title,
                'user': instance.Announcement.Announcement_author,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Новый отклик к посту',
            body="", #  это то же, что и message
            from_email='ViacheslavDan803@gmail.com',
            to=[instance.Announcement.Announcement_author.email], # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html

        msg.send() # отсылаем
    else:
        if instance.Comment_accepted:
            html_content = render_to_string( 
                'announce/comment_accepted.html',
                {
                    'post_id': instance.Announcement_id,
                    'post_title': instance.Announcement.Announcement_title,
                    'user': instance.User.username,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Отклик к посту',
                body="", #  это то же, что и message
                from_email='ViacheslavDan803@gmail.com',
                to=[instance.User.email], # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html") # добавляем html

            msg.send() # отсылаем