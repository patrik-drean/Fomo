from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.MIMEText import MIMEText

@view_function
def process_request(request):
    # utc_time = datetime.utcnow()
    if request.method == 'POST':
        print(request.POST['inputName'])
        print(request.POST['inputEmail'])
        print(request.POST['inputSubject'])
        print(request.POST['inputMessage'])

        # Send an actual email
        # fromaddr = "dreantester@gmail.com"
        # toaddr = request.POST['inputEmail']
        # subject = request.POST['inputSubject']
        # message = request.POST['inputMessage']
        #
        # msg = MIMEMultipart()
        # msg['From'] = fromaddr
        # msg['To'] = toaddr
        # msg['Subject'] = subject
        #
        # body = message
        # msg.attach(MIMEText(body, 'plain'))
        #
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(fromaddr, "TestAcount")
        # text = msg.as_string()
        # server.sendmail(fromaddr, toaddr, text)
        # server.quit()
    context = {
    }
    return request.dmp.render('contact.html', context)
