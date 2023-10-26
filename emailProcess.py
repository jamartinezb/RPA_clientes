import smtplib
import logging
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailView:
    def __init__(self, smtp_host, smtp_port, email, password):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def enviar_correo_con_adjunto(self, destinatario, asunto, cuerpo, adjunto):
        try:
            smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp.starttls()
            smtp.login(self.email, self.password)

            message = MIMEMultipart()
            message["Subject"] = asunto
            message["From"] = self.email
            message["To"] = destinatario

            body = cuerpo
            text_part = MIMEText(body, "plain")
            message.attach(text_part)

            with open(adjunto, "rb") as f:
                file_data = f.read()

            attachment = MIMEApplication(file_data, "octet-stream")
            attachment.add_header("Content-Disposition", "attachment", filename=adjunto)
            message.attach(attachment)

            smtp.sendmail(self.email, destinatario, message.as_string())
            
            smtp.quit()  # Cerrar la conexión SMTP después del envío
        except Exception as e:
            logging.error(f"Error al enviar el correo electrónico: {e}")
            raise Exception(f"Error al enviar el correo electrónico: {e}")

    def enviar_correo(self, destinatario, asunto, cuerpo):
        try:
            smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp.starttls()
            smtp.login(self.email, self.password)

            message = MIMEText(cuerpo)
            message["Subject"] = asunto
            message["From"] = self.email
            message["To"] = destinatario

            smtp.sendmail(self.email, destinatario, message.as_string())
            
            smtp.quit()  # Cerrar la conexión SMTP después del envío
        except Exception as e:
            logging.error(f"Error al enviar el correo electrónico: {e}")
            raise Exception(f"Error al enviar el correo electrónico: {e}")
        
class ConsoleView:
    def mostrar_mensaje(self, mensaje):
        print(mensaje)
