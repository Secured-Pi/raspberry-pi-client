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

and then to register your account (assuming the Django server is running and
you have already made an account):
```
python main.py
```
Keep this script running, as it is listening to teh Flask server for instructions.

You should then set a couple environmental variables LOCK_USER and LOCK_PW to match
your account credentials for the user_authentication script to use.  I find it easiest
to modify the ~/.profile file by adding to the bottom:
```
export LOCK_USER='some_username'
export LOCK_PW='some_password'
```

After that, you can log back in on the Django site as your normal account and
see your lock on the dashboard.  Then, set the lock to active by clicking
'Edit Details'.

You can also add your RFID code if you know the number by logging into the admin site.
You can find the code by running python user_authentication.py and looking at the output.

After verifying that the unlock/lock buttons work, you can try to use the
user authentication by running the script in a separate terminal window on the RPi
```
python user_authentication.py
```

