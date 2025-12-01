from datetime import timedelta
from email.message import EmailMessage

import aiosmtplib


async def send_email(
    *, sender, recipient, smtp_password, order_data={}, custom_message=None
):

    if custom_message:
        email_body = custom_message

    elif order_data:
        date_time = order_data['time'] - timedelta(hours=3)

        email_body = f'''
        Venda número {order_data['id']} foi finalizada
        pelo cliente {order_data['user_id']}
        no valor de R${order_data['total']}
        ás {date_time.strftime('%H:%M:%S do dia %d/%m/%Y')}.
        '''

    else:
        return

    msg = EmailMessage()

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Checkout Completado'
    msg.set_content(email_body)

    server_smtp = 'smtp.gmail.com'
    port = 587

    await aiosmtplib.send(
        msg,
        hostname=server_smtp,
        port=port,
        start_tls=True,
        username=sender,
        password=smtp_password
    )
