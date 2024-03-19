from django.core.mail import EmailMessage
from users.models import User
from learning_passport import settings
import pandas as pd


def noMatricEmail(request, to_users, cc_users, student_df, event_name):
    to_list = list()
    cc_list = list()

    for user in to_users:
        to_list.append(user.email)

    for user in cc_users:
        cc_list.append(user.email)

    # student_df = pd.DataFrame(columns=["Matric Number"])
    # for student in student_list:
    #     student_df.loc[len(student_df.index)] = [student]

    # student_html = student_df.to_html()
    student_html = student_df.to_html(index=False)

    scheme = request.scheme               # http or https
    domain = request.META['HTTP_HOST']    # example.com
    initial = f"{scheme}://{domain}"
    subject = f"[REJECTED] {len(student_df)} students commitment for {event_name} rejected."
    body = rf"""
    Dear PIC,<br><br>

    Please be informed that the form you approved for {event_name} have invalid student's matric number. <br>
    Below shows the list of invalid matric numbers.

    {student_html}
    
    <br><br>

    Thank you.<br><br>
        
    [This is an email generated by Learning Passport system.]
    """

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to_list,
        cc=cc_list,
    )
    email.content_subtype = "html"

    email.send(fail_silently=False)

def approvedEmail(request, to_users, cc_users, event_name):
    to_list = list()
    cc_list = list()

    for user in to_users:
        to_list.append(user.email)

    for user in cc_users:
        cc_list.append(user.email)

    # student_df = pd.DataFrame(columns=["Matric Number"])
    # for student in student_list:
    #     student_df.loc[len(student_df.index)] = [student]

    scheme = request.scheme               # http or https
    domain = request.META['HTTP_HOST']    # example.com
    initial = f"{scheme}://{domain}"
    subject = f"[APPROVED] Students commitment for {event_name} approved."
    body = rf"""
    Dear student,<br><br>

    Please be informed that the form you submitted for {event_name} is approved. <br>
    
    <br>
    Thank you.<br><br>
        
    [This is an email generated by Learning Passport system.]
    """

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to_list,
        cc=cc_list,
    )
    email.content_subtype = "html"

    email.send(fail_silently=False)

def inquiryEmail(request, to_users, cc_users, name, student_matric, inquiry_title, inquiry_content):
    to_list = list()
    cc_list = list()

    for user in to_users:
        to_list.append(user.email)

    for user in cc_users:
        cc_list.append(user.email)

    # student_df = pd.DataFrame(columns=["Matric Number"])
    # for student in student_list:
    #     student_df.loc[len(student_df.index)] = [student]

    scheme = request.scheme               # http or https
    domain = request.META['HTTP_HOST']    # example.com
    initial = f"{scheme}://{domain}"
    subject = f"[INQUIRY] {student_matric}: {inquiry_title}"
    body = rf"""
    Dear Admin,<br><br>

    {inquiry_content}
    
    <br><br>
    Name: {name}<br>
    Matric Number: {student_matric}
    <br><br>
    Thank you.<br><br>
    
    [This is an email generated by Learning Passport system.]
    """

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to_list,
        cc=cc_list,
    )
    email.content_subtype = "html"

    email.send(fail_silently=False)