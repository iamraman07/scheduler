import yagmail
import logging
from datetime import datetime
import os
from encryption import decrypt_data

# Configuration
HISTORY_FILE = "sent_emails.log"

def send_scheduled_email(job_id, encryption_key):
    """Send a scheduled email using the encrypted data"""
    try:
        # Decrypt the email data
        email_data = decrypt_data(encryption_key, job_id)
        
        if not email_data:
            logging.error(f"Failed to decrypt email data for job_id: {job_id}")
            return False
        
        sender_email = email_data.get('sender_email')
        password = email_data.get('password')
        to_email = email_data.get('to_email')
        cc_email = email_data.get('cc_email')
        bcc_email = email_data.get('bcc_email')
        subject = email_data.get('subject')
        content = email_data.get('content')
        
        # Validate required fields
        if not all([sender_email, password, to_email, subject, content]):
            logging.error(f"Missing required email fields for job_id: {job_id}")
            return False
        
        # Send the email
        with yagmail.SMTP(sender_email, password) as yag:
            yag.send(
                to=to_email,
                cc=cc_email if cc_email != 'None' else None,
                bcc=bcc_email if bcc_email != 'None' else None,
                subject=subject,
                contents=content
            )
        
        # Log successful send to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] To: {to_email} | Subject: '{subject}'"
        
        with open(HISTORY_FILE, "a") as history_file:
            history_file.write(log_entry + "\n")
        
        # Clean up the encrypted file
        encrypted_file = f"{job_id}.enc"
        if os.path.exists(encrypted_file):
            os.remove(encrypted_file)
        
        logging.info(f"Email sent successfully to {to_email} with subject '{subject}'")
        return True
    
    except Exception as e:
        logging.error(f"Error sending scheduled email (job_id: {job_id}): {e}")
        return False
