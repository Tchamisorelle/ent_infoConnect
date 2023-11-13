# from django.core.mail import send_mail
import os
from decouple import config
# from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
def send_notification_email(subject, message, recipient_list):
    # Charger les variables d'environnement
    email_password = config('EMAIL_HOST_PASSWORD') 
    from_email = config('EMAIL_HOST_USER')
    # Envoyer l'e-mail en utilisant les variables d'environnement
    # send_mail(
    #     subject,
    #     message,
    #     from_email,
    #     recipient_list,
    #     auth_user,
    #     auth_password=email_password,
        
    #     # fail_silently=False,
    # )

    #########   methode 2 avec fichier html externe ######

    html_content = render_to_string('result.html', {'message': message})
    text_content = strip_tags(html_content)  # Version texte du contenu HTML
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email="pharma.prjt.yde <'pharma.prjt.yde@gmail.com'>",
        to=recipient_list,
    ) 
    email.attach_alternative(html_content, "text/html")



    ##### methode 2 ########

    # email = EmailMultiAlternatives(
    #     subject=subject,
    #     body=message,
    #     from_email=from_email,
    #     to=recipient_list,
    # ) 
    # html_content = f"""
    #                <html> 
    #                <body>
    #                     <center>
    #                     <img src="./static/a.jpg" alt="en tete" width="20%" height="15%"></center>
    #                     <p>{message}
    #                     <br>Bonjour, Merci de vous être inscrit sur notre site.
    #                     <br><span style='color:red'> Vous pouvez maintenant accéder à toutes nos fonctionnalités.</span>
    #                     <br> Visitez notre repertoire telephonique des communes du cameroun : https://qgiscloud.com/sorelle/annuaire/
    #                     </p>
    #                 </body>
    #                 </html>
    #                  """
    # email.attach_alternative(html_content, "text/html")
    

    #for attachment_path in attachment_paths:
     #   email.attach_file(attachment_path)

    email.send(fail_silently=False)



def send_signup_email(user_email):
    subject = 'Bienvenue sur notre site'
    message = 'Merci de vous être inscrit sur notre site. Bienvenue!'
    from_email = 'info@example.com'
    recipient_list = [user_email]
    from_email = 'tamensorelle5@gmail.com'
    print('mon mail', from_email)
    send_mail(subject, message, from_email, recipient_list)
