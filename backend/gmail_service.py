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


async def send_order_status_update_email(to_email: str, order_data: dict, old_status: str, new_status: str):
    """Send email notification when order status is updated"""
    try:
        if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
            logger.warning("Gmail credentials not configured. Email not sent.")
            return False
            
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Order Status Update - #{order_data["order_id"]}'
        msg['From'] = f'Anantha Home Foods <{GMAIL_EMAIL}>'
        msg['To'] = to_email
        
        # Status display names with emojis
        status_display = {
            'confirmed': '✅ Confirmed',
            'processing': '🔄 Processing',
            'shipped': '🚚 Shipped',
            'delivered': '📦 Delivered',
            'cancelled': '❌ Cancelled'
        }
        
        # Status color mapping
        status_colors = {
            'confirmed': '#16a34a',
            'processing': '#2563eb',
            'shipped': '#f59e0b',
            'delivered': '#059669',
            'cancelled': '#dc2626'
        }
        
        new_status_display = status_display.get(new_status, new_status.title())
        status_color = status_colors.get(new_status, '#666')
        
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
                <h2 style="color: #f97316; text-align: center;">📬 Order Status Update</h2>
                <p>Dear {order_data.get("customer_name", "Customer")},</p>
                <p>Your order status has been updated!</p>
                
                <div style="background-color: #fff7ed; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <h3 style="color: {status_color}; margin: 0; font-size: 24px;">
                        {new_status_display}
                    </h3>
                    <p style="margin-top: 10px; color: #666;">Order ID: <strong>{order_data["order_id"]}</strong></p>
                    <p style="color: #666;">Tracking Code: <strong>{order_data.get("tracking_code", "")}</strong></p>
                </div>
                
                <div style="background-color: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #16a34a; margin-top: 0;">Delivery Details</h3>
                    <p><strong>Address:</strong><br>{address_html}<br>
                    {order_data.get("location", "")}</p>
                    <p><strong>Phone:</strong> {order_data.get("phone", "")}</p>
                    <p><strong>Total Amount:</strong> ₹{order_data.get("total", 0)}</p>
                </div>
                
                <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin-top: 0;">📦 Track Your Order</h4>
                    <p>You can track your order anytime using your Order ID or Tracking Code on our website.</p>
                    <p>Visit our Track Order page and enter your details to get real-time updates!</p>
                </div>
                
                <p style="margin-top: 30px;">If you have any questions, feel free to contact us at <strong>9985116385</strong></p>
                
                <p style="text-align: center; color: #666; margin-top: 30px; font-size: 12px;">
                    Thank you for choosing Anantha Home Foods!<br>
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
        
        logger.info(f"Order status update email sent successfully to {to_email} via Gmail")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order status update email via Gmail: {str(e)}")
        return False


async def send_city_approval_email(to_email: str, city_data: dict):
    """Send email notification when a city suggestion is approved"""
    try:
        if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
            logger.warning("Gmail credentials not configured. Email not sent.")
            return False
            
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Great News! We now deliver to {city_data["city"]}! 🎉'
        msg['From'] = f'Anantha Home Foods <{GMAIL_EMAIL}>'
        msg['To'] = to_email
        
        html_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #16a34a; text-align: center;">🎉 Exciting News!</h2>
                <p>Dear {city_data.get("customer_name", "Valued Customer")},</p>
                <p>We're thrilled to inform you that we now deliver to <strong>{city_data["city"]}, {city_data["state"]}</strong>!</p>
                
                <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <h3 style="color: #16a34a; margin: 0; font-size: 24px;">
                        ✅ City Added
                    </h3>
                    <p style="margin-top: 15px; font-size: 18px; color: #166534;">
                        <strong>{city_data["city"]}, {city_data["state"]}</strong>
                    </p>
                </div>
                
                <div style="background-color: #fff7ed; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #ea580c; margin-top: 0;">📍 Delivery Information</h3>
                    <p>Thanks to your suggestion, we've added {city_data["city"]} to our delivery locations!</p>
                    <p>You can now enjoy our delicious traditional foods delivered right to your doorstep.</p>
                </div>
                
                <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin-top: 0;">🛍️ Start Shopping!</h4>
                    <p>Visit our website to browse our complete collection of:</p>
                    <ul style="margin: 10px 0;">
                        <li>Traditional Laddus & Chikkis</li>
                        <li>Authentic Sweets</li>
                        <li>Hot Snacks & Items</li>
                        <li>Homemade Pickles</li>
                        <li>Fresh Powders & Spices</li>
                    </ul>
                    <p>All made with authentic ingredients and traditional recipes!</p>
                </div>
                
                <p style="margin-top: 30px; text-align: center;">
                    <strong>Ready to place your first order?</strong><br>
                    Visit our website and start shopping today!
                </p>
                
                <p style="margin-top: 20px;">If you have any questions, feel free to contact us at <strong>9985116385</strong></p>
                
                <p style="text-align: center; color: #666; margin-top: 30px; font-size: 12px;">
                    Thank you for choosing Anantha Home Foods!<br>
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
        
        logger.info(f"City approval email sent successfully to {to_email} via Gmail")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send city approval email via Gmail: {str(e)}")
        return False

async def send_city_rejection_email(to_email: str, city_data: dict):
    """Send email notification when a city suggestion is rejected"""
    try:
        if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
            logger.warning("Gmail credentials not configured. Email not sent.")
            return False
            
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Update on Your City Request - {city_data["city"]}'
        msg['From'] = f'Anantha Home Foods <{GMAIL_EMAIL}>'
        msg['To'] = to_email
        
        html_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #ea580c; text-align: center;">Update on Your Delivery Request</h2>
                <p>Dear {city_data.get("customer_name", "Valued Customer")},</p>
                <p>Thank you for your interest in getting Anantha Home Foods delivered to <strong>{city_data["city"]}, {city_data["state"]}</strong>.</p>
                
                <div style="background-color: #fff7ed; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #ea580c; margin: 0;">📍 Current Status</h3>
                    <p style="margin-top: 15px;">
                        We appreciate your suggestion! Unfortunately, we are not able to deliver to <strong>{city_data["city"]}</strong> at this time due to logistical constraints.
                    </p>
                </div>
                
                <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin-top: 0;">🔔 Stay Updated</h4>
                    <p>We're constantly expanding our delivery network! If there's enough demand from your area, we'll definitely consider adding {city_data["city"]} in the future.</p>
                    <p>We'll keep your request on file and notify you if we start delivering to your area.</p>
                </div>
                
                <div style="background-color: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="margin-top: 0;">💡 Alternative Options</h4>
                    <p>In the meantime, you might consider:</p>
                    <ul style="margin: 10px 0;">
                        <li>Checking if we deliver to nearby cities</li>
                        <li>Arranging a bulk order for delivery to a nearby location</li>
                        <li>Following us on social media for expansion updates</li>
                    </ul>
                </div>
                
                <p style="margin-top: 30px;">If you have any questions or would like to discuss alternatives, feel free to contact us at <strong>9985116385</strong></p>
                
                <p style="text-align: center; color: #666; margin-top: 30px; font-size: 12px;">
                    Thank you for your understanding and interest in Anantha Home Foods!<br>
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
        
        logger.info(f"City rejection email sent successfully to {to_email} via Gmail")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send city rejection email via Gmail: {str(e)}")
        return False

