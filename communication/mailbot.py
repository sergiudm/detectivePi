import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_email(subject, body, to_emails, from_email, password, smtp_server, smtp_port, image_path=None):
    # Create the email
    msg = MIMEMultipart('related')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    # Create the HTML part
    html_body = f"""
    <html>
    <body>
        {body}
        <br>
        <img src="cid:image1">
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # Attach an image if provided
    if image_path:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data, name=os.path.basename(image_path))
            image.add_header('Content-ID', '<image1>')
            msg.attach(image)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)

        # Send the email
        server.sendmail(from_email, to_emails, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()

# # Example usage
# if __name__ == "__main__":
#     # Get the first image from the directory
#     # 获取当前文件的绝对路径
#     current_file_path = os.path.abspath(__file__)

#     # 获取当前文件的父文件夹路径
#     parent_parent_directory = os.path.dirname(os.path.dirname(current_file_path))

#     # 构建指向父文件夹中的 mailPic 目录的路径
#     image_directory = os.path.join(parent_parent_directory, "resources")
    
#     image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
#     if image_files:
#         first_image_path = os.path.join(image_directory, image_files[0])
#     else:
#         first_image_path = None
#         print("No image files found in the directory.")

#     send_email(
#         subject="Test Email",
#         body="<h1>This is a test email for 🤡🤡🤡🤡🤡</h1><p>With an image attached below.</p>",
#         to_emails=["2824174663@qq.com", "12212635@mail.sustech.edu.cn"],
#         from_email="2990973166@qq.com",
#         password="xfmhwdmoutajdhed",
#         smtp_server="smtp.qq.com",
#         smtp_port=587,
#         image_path=first_image_path  # Use the first image found
#     )