# Email Scheduler with Encryption

A secure Flask-based email scheduling application that lets you schedule emails to be sent at specific times, even when the application is closed. Your email data is encrypted using Fernet encryption for security.

## Features

- ✅ Schedule emails to be sent at specific times
- 🔒 Secure storage of email data with encryption
- 📧 Support for multiple recipients with CC/BCC options
- 📅 View history of sent emails
- ❌ Cancel scheduled emails
- 🕒 Send emails at scheduled times even if the application is closed

## Requirements

- Python 3.7 or higher
- Flask and related libraries
- Yagmail for sending emails
- Cryptography for encryption

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/email-scheduler.git
   cd email-scheduler
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages:
   ```
   pip install flask==2.3.2 flask-apscheduler==1.12.4 yagmail==0.15.293 cryptography==41.0.3 email-validator==2.0.0 gunicorn==21.2.0 psycopg2-binary==2.9.6
   ```

   Alternatively, you can create a requirements.txt file with these dependencies and install them:
   ```
   # requirements.txt content
   Flask==2.3.2
   Flask-APScheduler==1.12.4
   yagmail==0.15.293
   cryptography==41.0.3
   email-validator==2.0.0
   gunicorn==21.2.0
   psycopg2-binary==2.9.6

   # Install using
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```
   Or using Gunicorn (recommended for production):
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## Using the Email Scheduler

### Scheduling an Email

1. Fill out the Sender Information section:
   - Your Email (Gmail account recommended)
   - App Password (See below for instructions on creating an app password)

2. Enter Email Content:
   - To: The recipient's email address
   - Optional: Add CC/BCC recipients
   - Subject: The email subject
   - Content: The body of the email

3. Set Schedule Time:
   - Enter the hours (0-23), minutes (0-59), and seconds (0-59) when you want the email to be sent
   - If the time has already passed today, it will be scheduled for tomorrow

4. Click "Schedule Email" to confirm and schedule your email

### Viewing History and Scheduled Emails

1. Click on "History" in the navigation menu
2. View your scheduled emails and sent email history
3. Cancel specific scheduled emails or all scheduled emails
4. Delete your email history if needed

## Creating a Google App Password

This application uses Gmail's SMTP server, which requires an app password for security:

1. Go to your Google Account settings (https://myaccount.google.com/)
2. Select "Security"
3. Under "Signing in to Google," select "App passwords" (you may need to enable 2-Step Verification first)
4. Select "Mail" and "Other (Custom name)" and enter "Email Scheduler"
5. Click "Generate"
6. Use the 16-character password that appears in the application

## How it Works

- The application uses Flask for the web interface
- Flask-APScheduler manages the scheduled email jobs
- Email data is encrypted using Fernet symmetric encryption
- Yagmail sends the emails through Gmail's SMTP server
- The scheduler runs in the background, allowing emails to be sent even if the web interface is closed

## Project Structure

```
email-scheduler/
├── app.py               # Main Flask application
├── main.py              # Entry point for Gunicorn
├── email_service.py     # Email sending logic
├── encryption.py        # Data encryption/decryption
├── scheduler.py         # Job scheduling functionality
├── templates/           # HTML templates
│   ├── base.html        # Base template with layout
│   ├── index.html       # Home page with email form
│   └── history.html     # Email history page
├── static/              # Static assets
│   ├── css/             # CSS styles
│   │   └── custom.css   # Custom styling
│   └── js/              # JavaScript
│       └── main.js      # Client-side functionality
├── encryption.key       # Generated encryption key
├── *.enc                # Encrypted email data files
├── email_scheduler.log  # Application logs
└── sent_emails.log      # History of sent emails
```

## Security Notes

- Email passwords are not stored in plain text but are encrypted
- Each job has a unique ID and separate encrypted file
- The encryption key is stored locally in a key file

## Troubleshooting

- If emails are not being sent, check that your app password is correct
- Make sure the application is running if you need to send scheduled emails
- Check that your Gmail account allows less secure apps (or preferably use an app password as described above)
- If you're experiencing issues, check the `email_scheduler.log` file for error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.