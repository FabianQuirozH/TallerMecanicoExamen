# email_test.py
import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('manuelotaiza53@gmail.com', 'wawa citw kmdf lvwe')
    message = 'Subject: {}\n\n{}'.format('Prueba', 'Este es un correo de prueba')
    server.sendmail('manuelotaiza53@gmail.com', 'tallermecanicopweb@gmail.com', message)
    server.quit()
    print("Correo enviado exitosamente")
except Exception as e:
    print(f"Error al enviar el correo: {e}")