import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('manuelotaiza53@gmail.com', 'wawa citw kmdf lvwe')
    server.quit()
    print("Conexión SMTP exitosa")
except Exception as e:
    print(f"Error al conectar con SMTP: {e}")
