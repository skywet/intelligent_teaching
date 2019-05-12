import smtplib
from utils.warning_module import warning
from utils.load_config import load_config
from email.mime.text import MIMEText
from email.header import Header

def send_mail():
    mail_host = 'smtp.163.com'
    mail_user = 'm15970551155@163.com'
    mail_passwd = '123456ex'

    tolerence = load_config()[1]

    sender = 'm15970551155@163.com'
    receivers = [i+'@smail.mail.net' for i in warning()]

    mail_message = '''
    <p>系统提醒您</p>
    <p>系统将在您下一次缺课后自动归零您的平时分</p>
    '''
    message = MIMEText(mail_message,'html','utf-8')
    message['From'] = Header('智能教学辅助系统','utf-8')
    
    message['Subject'] = Header('智能教学辅助提醒','utf-8')

    try:
        if len(receivers) > 0:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host,25)
            smtp_obj.login(mail_user,mail_passwd)
            smtp_obj.sendmail(sender,receivers,message.as_string())
    except smtplib.SMTPException:
        print('Error!')
    return 0