from time import sleep
import traceback
from typing import Callable
from functools import wraps
from harveyutils.loggerv2 import Logger
from classes.Session import SessionCustom
from threading import Lock


def log_sleep(logger: Logger, wait_time: int, units: str, prefix: str) -> None:
    logger.log(f"Sleeping {prefix}[{wait_time}{units}]...")


class ExceptionNoLog(Exception):
    """Custom exception class, doesn't print all exception info when raised
    and sleeps using the sleep_monitor function rather than the sleep_error
    function.
    """

    pass


def tasks_decorator(func: Callable):
    """The decorator for request methods.

    Arguements:
        func: Function to execute inside the wrapper

    Returns:
        A request response
    """

    @wraps(func)
    def wrapper_decorator(*args, **kwargs):
        self = args[0]
        if self.kill_task_data["shouldKill"] and not self.kill_task_data["isKilled"]:
            with self.thread_lock:
                self.stop_task(block=False)

            while True:
                pass
        else:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(e)

                if type(e) == ExceptionNoLog:
                    self.sleep_monitor()
                else:
                    traceback.print_tb(e.__traceback__)
                    self.sleep_error()

                return wrapper_decorator(*args, **kwargs)

    return wrapper_decorator


class Task:
    """The very base of any Task.

    Arguements:
        thread_lock: A lock shared between all tasks.

        kill_task_list: A list of dict data containing Task.kill_task_data.

        task_number: Task (thread) number.
        settings: JSON from settings/settings.json and settings_dev.json.
        task_data: Data from a task file.
        profile_data: A profile from the profiles file.

    Attributes:
        kill_task_data: A requests session.
        thread_lock: A requests session.
        task_number: A requests session.
        settings: A requests session.
        task_data: A requests session.
        profile_data: A requests session.
        ses: A requests session.
        logger: A logger object.
    """

    def __init__(
        self,
        thread_lock: Lock,
        kill_task_list: list,
        task_number: int,
        settings: dict,
        task_data: dict,
        profile_data: dict,
    ) -> None:
        self.kill_task_data = {
            "shouldKill": False,
            "isKilled": False,
            "setShouldKill": self.set_should_kill,
        }
        self.thread_lock = thread_lock
        self.task_number = task_number
        self.settings = settings
        self.task_data = task_data
        self.profile_data = profile_data

        # Appending kill_task_data to kill_task_list
        with self.thread_lock:
            kill_task_list.append(self.kill_task_data)

        # Requests session
        self.ses = SessionCustom()

        # Custom logger object
        self.logger = Logger(True, self.task_number)
        pass

    def stop_task(self, block=True):
        """Stop task."""
        self.logger.error("Stopping task...")
        self.kill_task_data["isKilled"] = True
        if block:
            while True:
                pass

    def set_should_kill(self):
        self.kill_task_data["shouldKill"] = True

    @tasks_decorator
    def sleep_monitor(self) -> None:
        """Sleeps for the time of the monitor delay."""
        wait_time_ms = self.settings["monitorDelay"]
        log_sleep(self.logger, wait_time_ms, "ms", "M")
        sleep(wait_time_ms / 1000)

    @tasks_decorator
    def sleep_error(self) -> None:
        """Sleeps for the time of the error delay."""
        wait_time_ms = self.settings["errorDelay"]
        log_sleep(self.logger, wait_time_ms, "ms", "E")
        sleep(wait_time_ms / 1000)

    @tasks_decorator
    def sleep_custom(
        self, wait_time_ms: int, prefix: str = "Custom", should_log: bool = True
    ) -> None:
        """Sleeps for a custom amount of time.

        Arguements:
            wait_time_ms: Time to wait for in MS.
            prefix: Text to prefix the log message with, log message
                example -> 'Sleeping Custom[1000ms]....'
            should_log: Boolean to set whether to log the wait.
        """
        if should_log:
            log_sleep(self.logger, wait_time_ms, "ms", prefix)

        sleep(wait_time_ms / 1000)

    @tasks_decorator
    def sleep_custom_s(self, wait_time_s: int):
        log_sleep(self.logger, wait_time_s, " Secs", "Custom")

        sleep(wait_time_s)
