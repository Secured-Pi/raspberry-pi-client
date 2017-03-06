# Client-side app

## Description
Client-side python script that let RPi subscribes to socketio stream from Secured-Pi sever.

This will require OpenCV.  Here is a great guide for setting it up on the
Raspberry Pi 3 Model B:
http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

In that same virtual environment, run
```
pip install -r requirements.txt
```

then to register your account (assuming the Django server is running and
you have already made an account):
```
python main.py
```

to register your lock.  THEN, go to your Django site as the admin and
set the lock to active and enter your RFID code.  You can find the code by
running python user_authentication.py and looking at the output.  Of course,
it will fail the first time.

After that, you can log back in as your normal account and see your lock on
the dashboard.

After verifying that the unlock/lock buttons work, you can try to use the
user authentication by running
```
python user_authentication.py
```

