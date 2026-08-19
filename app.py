import os
import logging
import threading
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

# Logging configuration setup for Render logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'sr_technologies_secret_key'

# Configuration using Environment Variables
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "hari.srtechnologies@gmail.com")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

def send_async_email(name, email, message):
    try:
        logging.info("Sending email via Resend API...")
        
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "from": "onboarding@resend.dev",
            "to": [ADMIN_EMAIL],
            "subject": f"New Project Enquiry from {name} - SR Technologies",
            "text": f"""You have received a new enquiry from your website contact form:

Name: {name}
Email: {email}

Message:
{message}"""
        }
        
        response = requests.post("https://api.resend.com/emails", json=payload, headers=headers)
        
        if response.status_code == 200:
            logging.info(f"Email successfully sent via Resend for {name}")
        else:
            logging.error(f"Resend API Error: {response.text}")
            
    except Exception as e:
        logging.error(f"Background Email Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/technologies')
def technologies():
    return render_template('technologies.html')

@app.route('/ai-planner')
def ai_planner():
    return render_template('ai_planner.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        logging.info(f"Contact form submission received from: {name} ({email})")
        threading.Thread(target=send_async_email, args=(name, email, message)).start()
        
        flash('Mail successfully sent! Our engineering lead will respond within one business day.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

@app.route('/ai/generate-proposal', methods=['POST'])
def generate_proposal():
    data = request.get_json() or {}
    description = data.get('description', '').lower()
    
    est_price = "₹30,000 - ₹70,000"
    sol_type = "Custom Business Web Application"
    modules = "Responsive UI, Database Architecture, Contact System, Admin Dashboard"
    
    if 'erp' in description or 'manufacturing' in description:
        est_price = "₹3 Lakhs - ₹6 Lakhs"
        sol_type = "Enterprise ERP & Operations Management"
        modules = "Inventory Tracking, Finance Module, Multi-branch Access"
    elif 'crm' in description or 'sales' in description or 'leads' in description:
        est_price = "₹1.5 Lakhs - ₹3 Lakhs"
        sol_type = "Custom CRM & Sales Pipeline"
        modules = "Lead Tracking, Automated Pipelines, Client Management"
    elif 'ecommerce' in description or 'store' in description or 'shop' in description:
        est_price = "₹70,000 - ₹1.5 Lakhs"
        sol_type = "Secure E-Commerce Platform"
        modules = "Product Catalog, Secure Checkout, Order Management"
    elif 'dental' in description or 'clinic' in description or 'hospital' in description:
        est_price = "₹40,000 - ₹90,000"
        sol_type = "Patient Portal & Appointment Booking App"
        modules = "Online Booking System, Patient Records, SMS Reminders"

    return {
        "success": True,
        "industry": data.get('description', ''),
        "solution": sol_type,
        "price": est_price,
        "features": modules
    }

if __name__ == '__main__':
    app.run(debug=True)