import subprocess

def is_valid_email_from_sendmail_output(output):
    # Check for indicators of successful delivery (valid email)
    if "Message accepted for delivery" in output:
        return True
    
    # Check for indicators of failed delivery (invalid email)
    if "no such user" in output.lower():
        return False
    
    # Check for other error codes or messages indicating invalid email
    if "550" in output and "no such" in output.lower():
        return False
    
    # If none of the above conditions match, assume invalid email
    return False

def send_test_email(sender_email, recipient_email, subject, body):
    # Construct the sendmail command to execute
    sendmail_command = f"echo 'Subject: {subject}\n{body}' | /usr/sbin/sendmail -v {recipient_email}"
    
    try:
        # Execute the sendmail command and capture the output
        result = subprocess.run(sendmail_command, shell=True, capture_output=True, text=True)
        
        # Check the return code to determine success or failure
        if result.returncode == 0:
            print("Email sent successfully.")
        else:
            print(f"Failed to send email to {recipient_email}.")

        # Check if the recipient email is valid based on the sendmail output
        is_valid_email = is_valid_email_from_sendmail_output(result.stdout)
        if not is_valid_email:
            print(f"Recipient email '{recipient_email}' is invalid or does not exist.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    sender_email = 'testing@locolope.com'  # Your email address
    recipient_email = 'reb234ee323_2_2w232wr13@gmail.com'  # Recipient's email address
    subject = 'Test Email'
    body = 'This is a test email to check delivery.'

    send_test_email(sender_email, recipient_email, subject, body)
