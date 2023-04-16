==============================
Developing the Forever Library
==============================


Introduction
=============
The Forever Library is an Android App that is
written in Python using the Kivy UI framework.


Prerequisites
=============
Before setting up the development environment,
you need to make sure that you have the following
prerequisites installed on your system:

* Ubuntu 20.04
* Python 3.8.10


Install the Java Development Kit (JDK)
======================================
To build an Android application on Ubuntu, you
will need to install a version of the Java
Development Kit (JDK) that is compatible with
the Android SDK.

Kivy requires a minimum of JDK 8 or later, but as
of the time of writing, the recommended version
of Java for building Android apps is JDK 11. You
can install JDK 11 on Ubuntu using the following
command::

    sudo apt-get install openjdk-11-jdk

This will install the OpenJDK 11 JDK, which is
free and open-source. Note that if you have other
versions of Java installed on your system, you
may need to configure your PATH environment
variable to use the correct version.


Install the Android SDK
=======================

Once you have installed the JDK, you can download
and install the Android SDK, and use tools like
buildozer to build your app. Be sure to follow
the Kivy documentation and the Android developer
documentation for the specific version of Android
you are targeting.

Use the following command to download and install
the Android SDK::

    sudo apt-get install android-sdk-platform-tools-common


Add user to plugdev group
=========================

To access USB devices, you need to add your user
to the ```plugdev group```. You can do this by
running the following command::

    sudo usermod -aG plugdev $USER

You will need to restart your workstation for 
the changes to take effect.


Set up udev rules
=================

Setting up udev rules on Ubuntu is necessary to
allow non-root users to access Android devices
connected to the computer via USB. Without proper
udev rules, you may encounter permission errors
when attempting to access the device.

To set up the udev rules on Ubuntu, follow these steps:

Create a new file /etc/udev/rules.d/51-android.rules
using a text editor with root privileges
(e.g., sudo nano /etc/udev/rules.d/51-android.rules).

Add the following line to the file to grant access
to devices using the Google USB vendor ID::

    SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"

If you are using a different device with a
different vendor ID, you will need to replace
idVendor with the appropriate value. You can find
the vendor ID for your device by running the lsusb
command in a terminal and looking for the device
in the list.

Save the file and exit the text editor.

Reload the udev rules by running the following 
command in a terminal::

    sudo udevadm control --reload-rules

This will reload the udev rules without having
to reboot your system.

Disconnect and reconnect your Android device to 
the computer via USB.

After completing these steps, your Android device
should be recognized by the system and accessible
to non-root users without encountering permission
errors.


FAQ
===

adb devices says that the device is unauthorized,
what does that mean?

If adb devices shows your Android device as
"unauthorized", it means that your computer
is not currently authorized to communicate with
the device over USB debugging.

When you connect an Android device to a computer
via USB, the device will display a prompt asking
you to allow USB debugging from the computer.
If you previously granted authorization and have
not revoked it, it is possible that the RSA key
used to identify your computer has changed or
become invalid, causing the device to reject
the connection.

To resolve this issue, you can follow these steps:

Disconnect your Android device from the computer.
Revoke USB debugging authorization for your 
computer on the device:

* Go to the "Settings" app on your Android device.
* Scroll down to "Developer options".
* Tap "Revoke USB debugging authorizations".
* Reconnect your Android device to the computer via USB.
* When prompted on your Android device, allow USB debugging from the computer.
* Run adb devices again to see if your device is now authorized.

If these steps do not resolve the issue, you may
need to reset the RSA key used for USB debugging
on your computer. To do this, you can delete the
.android directory in your home directory, which
contains the RSA key and other configuration files
used by adb::

    rm -rf ~/.android

After deleting this directory, reconnect your
Android device to the computer and try running
adb devices again. This should prompt your Android
device to allow USB debugging and generate a new
RSA key for your computer.
