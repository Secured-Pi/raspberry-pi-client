import RPi.GPIO as GPIO
import MFRC522
import signal


def get_RFID():
    """Return the uid of rfid card."""
    def end_read(signal, frame):
        global continue_reading
        continue_reading = False
        GPIO.cleanup()

    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()
    looking = True
    print('waiting for rfid...')
    while looking:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("Card read UID: " + str(uid))
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            MIFAREReader.MFRC522_SelectTag(uid)
            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(8)
                MIFAREReader.MFRC522_StopCrypto1()
                looking = False
    print('returning uid: ', str(uid))
    return str(uid)



# continue_reading = True

# # Capture SIGINT for cleanup when the script is aborted
# def end_read(signal,frame):
#     global continue_reading
#     continue_reading = False
#     GPIO.cleanup()

# # Hook the SIGINT
# signal.signal(signal.SIGINT, end_read)
# # Create an object of the class MFRC522
# MIFAREReader = MFRC522.MFRC522()
# # This loop keeps checking for chips. If one is near it will get the UID and authenticate
# while continue_reading:
#     # Scan for cards
#     (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
#     # If a card is found
#     if status == MIFAREReader.MI_OK:
#         print("Card detected")
#     # Get the UID of the card
#     (status,uid) = MIFAREReader.MFRC522_Anticoll()
#     # If we have the UID, continue
#     if status == MIFAREReader.MI_OK:
#         # Print UID
#         print("Card read UID: "+str(uid))
#         # This is the default key for authentication
#         key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
#         # Select the scanned tag
#         MIFAREReader.MFRC522_SelectTag(uid)
#         # Authenticate
#         status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
#         # Check if authenticated
#         if status == MIFAREReader.MI_OK:
#             MIFAREReader.MFRC522_Read(8)
#             MIFAREReader.MFRC522_StopCrypto1()
#         else:
#             print("Authentication error")
