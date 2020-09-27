# import package
import africastalking
from decouple import config


def SendSMS(first_name, phone_number, item, amount):
    # Initialize SDK
    username = config('SANDBOX_USERNAME')    # use 'sandbox' for development in the test environment
    api_key = config('SANDBOX_API_KEY')      # use your sandbox app API key for development in the test environment
    africastalking.initialize(username, api_key)

    # Initialize a service e.g. SMS
    sms = africastalking.SMS
    
    message = f'Hi {first_name}. Your order of {item}, quantity {amount}, has been received and is being processed. Thank you.'
    sender = config('SANDBOX_SENDER')
    # Use the service synchronously
    response = sms.send(message, [phone_number], sender)
    print(response)

     