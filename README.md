# Client-side app

## Description
Client-side python script that let RPi subscribes to socketio stream from Secured-Pi Flask sever.

This will require OpenCV.  Here is a great guide for setting it up on the
Raspberry Pi 3 Model B:
http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

- Note:  You only need the 'face' module from the opencv_contrib repo.  You can delete the other
modules in teh modules folder.  I find that they usually have some error when trying to install
them.

Install a couple of dependencies on the RPi:
```
sudo apt-get install pigpio
sudo apt-get install python3-rpi.gpio python-rpi.gpio
```

In that same virtual environment (that you hopefully used), run
```
pip install -r requirements.txt
```

If you did not, you may have to copy some files over from your system python path
(you can find how to do this on StackOverflow...I will provide a link later)

In the src/main.py file, change you Django server to the appropriate  network ip of
the computer running the Django server (you can find this by running ifconfig on the machine).
Do this for the user_authentication.py as well.
Then to register your account (assuming the Django server is running and you have
already made an account):
```
python main.py
```

Enter the required information to register your lock, including scanning the RFID card
if you wish to use it.
- Note:  if you want to use facial recognition, you will also need
to use RFID as well.  This lets the script know when to take pictures.

Keep this script running, as it is listening to the Flask server for instructions.
The next time you run it, you will only need to enter your login credentials.

You should then set a couple environmental variables LOCK_USER and LOCK_PW to match
your account credentials for the user_authentication script to use.  I find it easiest
to modify the ~/.profile file by adding to the bottom:
```
export LOCK_USER='some_username'
export LOCK_PW='some_password'
```

Save the file, and of course, make sure to load your profile file at the command line:

```
source ~/.profile
```

After that, you can log back in on the Django site as your normal account and
see your lock on the dashboard.  Then, set the lock to active by clicking
'Edit Details'.

You can also add your RFID code if you know the number by logging into the admin site.
You can find the code by running python user_authentication.py and looking at the output.

After verifying that the unlock/lock buttons work, you can try to use the
user authentication.

IMPORTANT!  Make sure that you change the lock_id value in the send_img_to_server
function to match the ID of your lock (if needed)!  You can find this in the terminal window where
you are running the main.py script (lock pk), or on the Django site.  It will most
likely be '1' for you.  If you have another lock, however, the next lock will have
a different lock_id.

run the script in a separate terminal window on the RPi, making sure to be in the
src directory, run:

```
python user_authentication.py
```

If you do not have facial recognition enabled, you will not be required to pass
the test.  If you do have it enabled, you must first train it to recognize you.
I would suggest using the same camera to train as you use on the pi, in the same
environment/lighting.  This part can be tricky, and more instructions to come later...

