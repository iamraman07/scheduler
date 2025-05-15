import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_apscheduler import APScheduler
import logging
# import yagmail
from datetime import datetime, timedelta
import uuid

# Import custom modules
from encryption import generate_or_load_key, encrypt_data, decrypt_data
from email_service import send_scheduled_email
from scheduler import init_scheduler, add_job, remove_job, get_jobs

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='email_scheduler.log'
)

# Configuration
ENCRYPTION_KEY_FILE = "encryption.key"
EMAIL_DATA_FILE = "email_data.enc"
HISTORY_FILE = "sent_emails.log"

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Initialize the scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
init_scheduler(scheduler)

# Generate or load encryption key
encryption_key = generate_or_load_key(ENCRYPTION_KEY_FILE)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule_email():
    """Handle email scheduling"""
    try:
        # Get form data
        sender_email = request.form.get('sender_email')
        password = request.form.get('password')
        to_email = request.form.get('to_email')
        cc_email = request.form.get('cc_email', '')
        bcc_email = request.form.get('bcc_email', '')
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        # Get scheduling information
        hours = int(request.form.get('hours', 0))
        minutes = int(request.form.get('minutes', 0))
        seconds = int(request.form.get('seconds', 0))
        
        # Validate inputs
        if not all([sender_email, password, to_email, subject, content]):
            flash('All required fields must be filled out', 'danger')
            return redirect(url_for('index'))
        
        # Calculate send time
        now = datetime.now()
        send_time = now.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
        if now > send_time:
            send_time += timedelta(days=1)
        
        # Create unique job ID
        job_id = str(uuid.uuid4())
        
        # Prepare email data
        email_data = {
            'sender_email': sender_email,
            'password': password,
            'to_email': to_email,
            'cc_email': cc_email if cc_email else None,
            'bcc_email': bcc_email if bcc_email else None,
            'subject': subject,
            'content': content,
            'scheduled_time': send_time.strftime('%Y-%m-%d %H:%M:%S'),
            'job_id': job_id
        }
        
        # Encrypt and store email data
        encrypt_data(email_data, encryption_key, job_id)
        
        # Schedule the email
        wait_seconds = (send_time - now).total_seconds()
        add_job(
            job_id, 
            send_scheduled_email, 
            run_date=send_time,
            args=[job_id, encryption_key]
        )
        
        flash(f'Email scheduled successfully for {send_time.strftime("%Y-%m-%d %H:%M:%S")}', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Error scheduling email: {e}")
        flash(f'Error scheduling email: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/cancel', methods=['POST'])
def cancel_scheduled():
    """Cancel scheduled emails"""
    try:
        job_id = request.form.get('job_id')
        
        if job_id:
            # Cancel specific job
            remove_job(job_id)
            # Remove the encrypted file for this job
            encrypted_file = f"{job_id}.enc"
            if os.path.exists(encrypted_file):
                os.remove(encrypted_file)
            flash(f'Scheduled email with ID {job_id} was cancelled', 'success')
        else:
            # Cancel all jobs
            for job in get_jobs():
                job_id = job.id
                remove_job(job_id)
                # Remove the encrypted file for this job
                encrypted_file = f"{job_id}.enc"
                if os.path.exists(encrypted_file):
                    os.remove(encrypted_file)
            flash('All scheduled emails were cancelled', 'success')
        
        return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Error cancelling scheduled emails: {e}")
        flash(f'Error cancelling scheduled emails: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/history')
def view_history():
    """View email sending history"""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            for line in file:
                history.append(line.strip())
    
    # Get list of currently scheduled jobs
    scheduled_jobs = []
    for job in get_jobs():
        job_id = job.id
        job_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Try to get more info about the job
        try:
            job_data = decrypt_data(encryption_key, job_id)
            if job_data:
                scheduled_jobs.append({
                    'id': job_id,
                    'time': job_time,
                    'to': job_data.get('to_email'),
                    'subject': job_data.get('subject')
                })
        except Exception:
            scheduled_jobs.append({
                'id': job_id,
                'time': job_time,
                'to': 'Unable to decrypt',
                'subject': 'Unable to decrypt'
            })
    
    return render_template('history.html', history=history, scheduled_jobs=scheduled_jobs)

@app.route('/delete_history', methods=['POST'])
def delete_history():
    """Delete email history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            flash('Email history deleted successfully', 'success')
        else:
            flash('No email history found to delete', 'warning')
        
        return redirect(url_for('history'))
    
    except Exception as e:
        logging.error(f"Error deleting history: {e}")
        flash(f'Error deleting history: {str(e)}', 'danger')
        return redirect(url_for('history'))

@app.route('/jobs')
def get_scheduled_jobs():
    """Get list of scheduled jobs as JSON"""
    job_list = []
    for job in get_jobs():
        job_list.append({
            'id': job.id,
            'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(job_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
