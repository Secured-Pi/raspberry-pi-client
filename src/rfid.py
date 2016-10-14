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
