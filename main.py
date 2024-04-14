from flask import Flask, render_template, request, abort
import time
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import random
import string
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Define rate limiting parameters
RATE_LIMIT = 10  # Maximum requests per minute per IP address
RATE_LIMIT_PERIOD = 60  # Rate limit period in seconds (1 minute)

# Define IP blacklist parameters
BAN_DURATION = 3600  # Ban duration in seconds (1 hour)

# Maintain dictionaries to track access counts and blacklisted IPs
ip_access_counts = defaultdict(int)
ip_blacklist = {}
ip_last_access = defaultdict(float)  # Dictionary to store last access time for each IP

# Function to generate a random password
def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# Generate a random admin password
admin_password = generate_random_password()

# Function to get user's public IP address
def get_ip_address():
    try:
        # In a local environment, we cannot fetch the public IP address
        # Returning a dummy IP address for demonstration purposes
        return "127.0.0.1"
    except Exception as e:
        print("Error getting IP address:", e)
        return None

# Function to handle abnormal activity from an IP address
def handle_abnormal_activity(ip):
    ban_expiration = time.time() + BAN_DURATION
    ip_blacklist[ip] = ban_expiration
    # Store blocked IP address in a file
    with open("ipblocked.txt", "a") as file:
        file.write(ip + "\n")
    print(f"IP address {ip} has been banned until {time.ctime(ban_expiration)}")

# Middleware to enforce rate limiting and IP blacklisting
@app.before_request
def protect_against_ddos():
    ip = request.remote_addr
    current_time = time.time()

    # Check if the IP address is blacklisted
    if ip in ip_blacklist:
        if current_time < ip_blacklist[ip]:
            return abort(403)  # Forbidden
        else:
            del ip_blacklist[ip]  # Remove from blacklist if ban has expired

    # Update access count and last access time for the IP address
    ip_access_counts[ip] += 1
    ip_last_access[ip] = current_time

    # Check if rate limit is exceeded
    if ip_access_counts[ip] > RATE_LIMIT:
        handle_abnormal_activity(ip)
        return abort(429)  # Too Many Requests

# Function to load blocked IP addresses from file and block them
def block_blocked_ips():
    try:
        with open("ipblocked.txt", "r") as file:
            blocked_ips = file.readlines()
            for ip in blocked_ips:
                ip = ip.strip()
                ip_blacklist[ip] = time.time() + BAN_DURATION
    except FileNotFoundError:
        pass

# Clear IP access counts periodically to avoid memory bloat
def clear_ip_access_counts():
    current_time = time.time()
    for ip in list(ip_access_counts.keys()):
        if current_time - ip_last_access[ip] > RATE_LIMIT_PERIOD:
            del ip_access_counts[ip]

# Schedule periodic cleanup of IP access counts and blocking of blocked IPs
SCHEDULE_INTERVAL = 300  # Cleanup every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(clear_ip_access_counts, 'interval', seconds=SCHEDULE_INTERVAL)
scheduler.add_job(block_blocked_ips, 'interval', seconds=10)  # Check every 10 seconds
scheduler.start()

# Make sure to stop the scheduler when the application exits
atexit.register(lambda: scheduler.shutdown())

# Updated admin_permission function
def admin_permission(name, mail, passwords, ip_address, admin_password):
    # Write the randomly generated admin password to a file
    with open("admin_password.txt", "w") as file:
        file.write(admin_password)

    # Prompt the admin for permission and password
    print("\nINFORMATION OF USER TRYING TO ACCESS:\n")
    print(f"Name: {name}\nMail: {mail}\nPasswords: {passwords}\nIP Address: {ip_address}\n")
    admin_input = input("admin >> joined, granted? (Y/N): ")
    if admin_input.lower() == "y":
        admin_pass_input = input("Enter admin password: ")

        # Read the admin password from the file
        with open("admin_password.txt", "r") as file:
            stored_admin_password = file.read().strip()

        # Delete the admin password file
        os.remove("admin_password.txt")

        return admin_pass_input == stored_admin_password
    else:
        print("WRONG ADMIN PASS, USER HAS BEEN REJECTED FROM LOGGING IN!")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    try:
        if request.method == 'POST':
            name = request.form['name']
            passwords = request.form['password']
            mail = request.form['mail']
            ip_address = get_ip_address()  # Get user's IP address

            # Prompt for admin permission
            if not admin_permission(name, mail, passwords, ip_address, admin_password):
                return render_template("admin_rejected.html")
            else:
                # Check password and email requirements
                pass_length = len(passwords)
                if pass_length >= 8:
                    print("Received name:", name)
                    print("Received email:", mail)
                    print("Received pass:", passwords)
                    # Save client information to a file
                    save_client_info(name, mail, ip_address)
                    return render_template("post.html", name=name, passwords=passwords, mail=mail, ip=ip_address)
                else:
                    return render_template("error_connects.html")
    except Exception as e:
        print("ERROR: ", e)
        return render_template("error_connect.html")

def save_client_info(name, mail, ip_address):
    # Create the CLIENT_INFO directory if it doesn't exist
    if not os.path.exists("CLIENT_INFO"):
        os.makedirs("CLIENT_INFO")
    
    # Generate the file name based on the username
    username = name.split()[0].lower()
    file_name = f"CLIENT_INFO/{username}_logininfo.txt"
    
    # Write client information to the file
    with open(file_name, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {mail}\n")
        file.write(f"IP Address: {ip_address}\n")

if __name__ == '__main__':
    block_blocked_ips()  # Block IPs stored in ipblocked.txt upon program startup
    app.run(debug=True)
