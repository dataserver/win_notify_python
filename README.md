# Windows Notification Server

A simple Python app to receive Windows notifications on your network using REST requests.

## How it works

The app creates an HTTP server on port 8081 and a system tray icon to control it.

POST requests sent to the host endpoint `xxx:8081/notification` will create a Windows notification on the machine.

## POST request format
```
POST http://your_network_ip:8081/notification
content-type: application/json

{
    "title": "Notification Title",
    "body_message": "Your message here."
}
```

Remember to copy the `/assets` directory so the app can use the appropriate icons.

- `assets/notificationlogo.png` -  Used for the Windows notification.
- `assets/trayicon.ico` - Used as the tray icon.

## Windows Startup

Add the app to Windows startup so the server is loaded automatically on start.


## PyInstaller
```
pyinstaller app.spec
```
## Nuitika

```
python -m nuitka src/main.py --standalone --windows-icon-from-ico=src/appicon.png --windows-console-mode=disable --include-data-files=src/appicon.png=appicon.png --include-data-files=src/appicon.ico=appicon.ico --include-data-files=src/config.json=config.json
```

---

Or add to the top of `main.py`
``` 
# nuitka-project: --standalone
# nuitka-project: --windows-icon-from-ico=src/appicon.png
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/appicon.png=appicon.png
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/appicon.ico=appicon.ico
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/config.json=config.json
```
and run
```
python -m nuitka src/main.py
```

## api_requests.http
Visual Studio Code extension `REST Client`

https://marketplace.visualstudio.com/items?itemName=humao.rest-client


## License ##

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.