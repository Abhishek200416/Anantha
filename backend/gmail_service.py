import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

GMAIL_EMAIL = os.environ.get('GMAIL_EMAIL', '')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')

async def send_order_confirmation_email_gmail(to_email: str, order_data: dict):
    """Send order confirmation email using Gmail SMTP"""
    try:
        if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
            logger.warning("Gmail credentials not configured. Email not sent.")
            logger.info(f"Would send email to: {to_email} for order: {order_data['order_id']}")
            return False
            
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Order Confirmation - #{order_data["order_id"]}'
        msg['From'] = f'Anantha Lakshmi <{GMAIL_EMAIL}>'
        msg['To'] = to_email
        
        # Format items HTML
        items_html = ""
        for item in order_data.get("items", []):
            items_html += f'''
            <div style="padding: 10px; border-bottom: 1px solid #e5e7eb;">
                <p><strong>{item["name"]}</strong> ({item["weight"]})</p>
                <p>Quantity: {item["quantity"]} × ₹{item["price"]} = ₹{item["quantity"] * item["price"]}</p>
            </div>
            '''
        
        # Format address
        if order_data.get("doorNo"):
            address_html = f'''
            {order_data.get("doorNo", "")}, {order_data.get("building", "")}<br>
            {order_data.get("street", "")}<br>
            {order_data.get("city", "")}, {order_data.get("state", "")} - {order_data.get("pincode", "")}
            '''
        else:
            address_html = f'{order_data.get("address", "")}'
        
        html_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #f97316; text-align: center;">🎉 Order Confirmed!</h2>
                <p>Dear {order_data["customer_name"]},</p>
                <p>Thank you for your order from Anantha Lakshmi Traditional Foods!</p>
                
                <div style="background-color: #fff7ed; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #ea580c; margin-top: 0;">Order Details</h3>
                    <p><strong>Order ID:</strong> {order_data["order_id"]}</p>
                    <p><strong>Tracking Code:</strong> {order_data["tracking_code"]}</p>
                    <p><strong>Order Date:</strong> {order_data["order_date"]}</p>
                    <p><strong>Total Amount:</strong> ₹{order_data["total"]}</p>
                </div>
                
                <div style="background-color: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #16a34a; margin-top: 0;">Delivery Address</h3>
                    <p>{address_html}<br>
                    {order_data["location"]}</p>
                    <p><strong>Phone:</strong> {order_data["phone"]}</p>
                </div>
                
                <div style="margin: 20px 0;">
                    <h3 style="color: #1e40af;">Items Ordered</h3>
                    {items_html}
                </div>
                
                <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin-top: 0;">📦 Track Your Order</h4>
                    <p>You can track your order anytime using your Order ID <strong>{order_data["order_id"]}</strong> or Tracking Code <strong>{order_data["tracking_code"]}</strong> on our website.</p>
                    <p>Simply visit the Track Order page and enter your tracking code, phone number, or email to get updates!</p>
                </div>
                
                <p style="margin-top: 30px;">If you have any questions, feel free to contact us at <strong>9985116385</strong></p>
                
                <p style="text-align: center; color: #666; margin-top: 30px; font-size: 12px;">
                    Thank you for choosing Anantha Lakshmi Traditional Foods!<br>
                    Handcrafted with love and tradition 💚
                </p>
            </div>
        </body>
        </html>
        '''
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email using Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email} via Gmail")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email via Gmail: {str(e)}")
        return False
