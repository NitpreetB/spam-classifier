import markovify
import streamlit as st
import pandas as pd
import os
import csv
import subprocess

# Sample data: Replace these lists with your actual spam and non-spam email data
spam_emails = [
    "Congratulations! You've won a $1000 gift card. Click here to claim your prize now!",
    "You have been selected for a limited time offer. Buy now and get 50 off!",
    "Urgent: Your account has been compromised. Verify your details immediately by clicking this link.",
    "Get rich quick! Join our exclusive program and start earning thousands today.",
    "Congratulations! You've won a $1,000 Walmart gift card, Click here to claim now!",
    "You have been selected for a limited time offer, Call now!",
    "This is your final notice about your car's extended warranty, Act now!",
    "Get a free iPhone by completing this short survey,",
    "Urgent! Your account has been compromised, Verify your information now!",
    "You are pre-approved for a $10,000 loan, Apply today!",
    "Earn $500 a day working from home, No experience needed!",
    "You have one new message from a secret admirer, Click to read it now!",
    "100 free online dating, Find your soulmate today!",
    "You have been selected to win a brand new car, Don't miss out!",
    "Congratulations! You've won a $2,000 Amazon gift card, Click here to claim now!",
    "You have been selected for an exclusive offer, Call now!",
    "This is your final notice about your credit card's expiration, Act now!",
    "Get a free MacBook by completing this short survey,",
    "Urgent! Your bank account has been compromised, Verify your information now!",
    "You are pre-approved for a $15,000 loan, Apply today!",
    "Earn $600 a day working from home, No experience needed!",
    "You have one new message from an old friend, Click to read it now!",
    "100 free online courses, Enhance your skills today!",
    "You have been selected to win a brand new motorcycle, Don't miss out!",
    "Act now to receive a $500 gift card from Best Buy, Click here!",
    "Your PayPal account has been limited, Verify your identity immediately!",
    "Participate in our survey and win a $1,000 gift card, Click here!",
    "Get a free vacation package by filling out this quick form,",
    "Exclusive offer: Save 50 on your next purchase, Click now!",
    "You've been selected for a $300 gas card, Claim yours today!",
    "Your subscription has expired, Renew now to avoid interruption!",
    "Win a free iPad by joining our loyalty program, Sign up now!",
    "Confirm your email address to win a $200 shopping spree!",
    "Upgrade your smartphone for free, Limited time offer!",
    "Congratulations! You have been chosen to receive a $1,000 Home Depot gift card, Claim here!",
    "Your Apple account has been locked, Verify your information now!",
    "Act fast to claim your free sample pack, Click here!",
    "You've been selected to participate in our exclusive survey, Win big!",
    "Unlock a $500 travel voucher by completing this survey!",
    "Receive a free smartwatch by signing up today!",
    "Important! Your email account will be deactivated, Confirm now!",
    "Limited offer: Get a $100 gift card for referring friends, Act now!",
    "Your account will be terminated if not verified within 24 hours, Click here!",
    "Get a $1,000 Visa gift card by joining our rewards program!"
]

non_spam_emails = [
    "Reminder: Your appointment with Dr. Smith is scheduled for tomorrow at 3 PM",
    "Don't forget to submit your project report by the end of the day",
    "Team meeting has been rescheduled to 10 AM tomorrow. Please be on time",
    "Your Amazon order has been shipped and will arrive by Friday",
    "Can you please review the attached document and provide your feedback?",
    "Let's catch up for lunch next week. How about Tuesday?",
    "Your subscription to the monthly newsletter has been confirmed",
    "The office will be closed next Monday for the public holiday",
    "Please remember to update your contact information in the company directory",
    "Join us for the annual company picnic this Saturday at the park",
    "Reminder: Your dental appointment is scheduled for next Monday at 2 PM",
    "Please review the updated project plan and send your feedback by EOD",
    "Our team meeting has been moved to 11 AM tomorrow. Please mark your calendars",
    "Your package has been delivered. Check your mailbox",
    "Could you look over the attached proposal and let me know your thoughts?",
    "How about we meet for coffee next Wednesday at noon?",
    "Your membership renewal has been processed successfully",
    "The office will be open this Saturday for maintenance work",
    "Please update your emergency contact details in the HR system",
    "Join us for a virtual happy hour this Friday at 5 PM",
    "Don't forget to RSVP for the company holiday party next week",
    "Your feedback on the recent training session is requested. Please fill out the survey",
    "Reminder: Submit your timesheets by the end of the day",
    "Your subscription to the monthly magazine has been successfully renewed",
    "Our office will be closed on Friday for a team-building event",
    "Please remember to change your password before it expires",
    "We look forward to seeing you at the conference next week",
    "Your expense report for June has been approved",
    "Join our webinar on cybersecurity next Thursday. Register now!",
    "Your request for vacation days has been approved"
]

# Combine the emails into single text blobs
spam_text = "\n".join(spam_emails)
non_spam_text = "\n".join(non_spam_emails)

# Build the Markov models
spam_model = markovify.Text(spam_text)
non_spam_model = markovify.Text(non_spam_text)

# Function to generate spam message
def generate_spam():
    return spam_model.make_sentence()

# Function to generate non-spam message
def generate_not_spam():
    return non_spam_model.make_sentence()

#Function to write to spam.csv
def write_to_spam_file(message):
    try:
        with open('spam_gen.csv', 'a', newline='', encoding='latin-1') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['spam', message])
    except FileNotFoundError as e:
        print(f"Error: File 'spam_gen.csv' not found. {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


#Function to write to not-spam.csv
def write_to_not_spam_file(message):
    try:
        with open('not-spam.csv', 'a', newline='', encoding='latin-1') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['ham', message])
    except FileNotFoundError as e:
        print(f"Error: File 'not-spam.csv' not found. {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Function to retrain the spam model
def retrain_spam_model():
    try:
        with open('spam.csv', 'a', newline='', encoding='latin-1') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')

            # Check and write contents of Spam_gen.csv if it exists
            if os.path.exists('Spam_gen.csv'):
                with open('Spam_gen.csv', 'r', encoding='latin-1') as spam_gen_file:
                    spam_gen_reader = csv.reader(spam_gen_file)
                    for row in spam_gen_reader:
                        if len(row) == 2:  # Ensure each row has label and message
                            csv_writer.writerow(row)
                        else:
                            print(f"Skipping malformed row in Spam_gen.csv: {row}")

            # Check and write contents of not-spam.csv if it exists
            if os.path.exists('not-spam.csv'):
                with open('not-spam.csv', 'r', encoding='latin-1') as not_spam_file:
                    not_spam_reader = csv.reader(not_spam_file)
                    for row in not_spam_reader:
                        if len(row) == 2:  # Ensure each row has label and message
                            csv_writer.writerow(row)
                        else:
                            print(f"Skipping malformed row in not-spam.csv: {row}")

        # Run spam_detection.py using subprocess
        subprocess.run(['python', 'spam_detection.py'])
        print("Spam model retrained successfully!")
        st.session_state['spam_counter'] = 0
        st.session_state['non_spam_counter'] = 0

    except FileNotFoundError as e:
        print(f"Error during retraining: {e}")
    except Exception as e:
        print(f"Unexpected error during retraining: {e}")

    finally:
        # Cleanup: Remove temporary files
        try:
            if os.path.exists("Spam_gen.csv"):
                os.remove("Spam_gen.csv")
            if os.path.exists("not-spam.csv"):
                os.remove("not-spam.csv")
        except FileNotFoundError:
            pass  # Handle case where files might not exist


# Main Streamlit function
def main():
    st.title("Generate Spam and Non-Spam Messages")

    # Counter initialization
    if 'spam_counter' not in st.session_state:
        st.session_state['spam_counter'] = 0

    if 'non_spam_counter' not in st.session_state:
        st.session_state['non_spam_counter'] = 0

    # Button to generate spam message
    if st.button("Generate Spam Message"):
        spam_message = generate_spam()
        if spam_message:
            st.success(spam_message)
            write_to_spam_file(spam_message)
            st.session_state['spam_counter'] += 1

    # Button to generate non-spam message
    if st.button("Generate Non-Spam Message"):
        not_spam_message = generate_not_spam()
        if not_spam_message:
            st.success(not_spam_message)
            write_to_not_spam_file(not_spam_message)
            st.session_state['non_spam_counter'] += 1

    # Button to retrain the spam model
    if st.button("Retrain Spam Model"):
        retrain_spam_model()
        st.success("Spam model retrained successfully!")

    # Display counters
    st.write(f"Spam Messages Generated: {st.session_state['spam_counter']}")
    st.write(f"Non-Spam Messages Generated: {st.session_state['non_spam_counter']}")

if __name__ == "__main__":
    main()