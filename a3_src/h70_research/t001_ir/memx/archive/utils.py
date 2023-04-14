import os
import logging
import sys
import datetime 

def create_log_file(log_directory="logs"):
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)
    log_files = os.listdir(log_directory)
    log_count = len(log_files)
    log_file_name = f"chat_log_{log_count}.json"
    log_path = os.path.join(log_directory, log_file_name)

    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_file = logging.handlers.TimedRotatingFileHandler(
        log_path,
        when="midnight",
        backupCount=7
    )
    log_file.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(log_file)

    return logger

@staticmethod
def log_messages(func):
    def wrapper(*args, **kwargs):
        human_message = kwargs.get("human_message")
        bot_response = func(*args, **kwargs)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the logger set up in create_log_file
        logger = logging.getLogger(__name__)

        # capture stdout and stderr
        stdout_before = sys.stdout
        stderr_before = sys.stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer

        try:
            # execute the decorated function to capture any printed output
            bot_response = func(*args, **kwargs)
        finally:
            # restore stdout and stderr
            sys.stdout = stdout_before
            sys.stderr = stderr_before

        # get the output from stdout and stderr
        stdout_output = stdout_buffer.getvalue().strip()
        stderr_output = stderr_buffer.getvalue().strip()

        log_message = {
            "timestamp": current_time,
            "user_message": human_message,
            "bot_response": bot_message
        }