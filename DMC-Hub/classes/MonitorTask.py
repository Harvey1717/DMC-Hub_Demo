from bs4 import element
from classes.Task import Task, tasks_decorator
from threading import Lock

# requests_decorator = requests_decorator


class MonitorTask(Task):
    """The child class of a Task class,
    used for monitors.

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
        super().__init__(
            thread_lock, kill_task_list, task_number, settings, task_data, profile_data
        )

    def compare(self, old_list: list, new_list: list) -> list:
        """Compare two lists and return differences.

        Args:
            old_list (list): Old data.
            new_list (list): New data.

        Returns:
            list: [new_data, removed_data]
                added_data: Data that has been added.
                removed_data: Data that has been removed.
        """
        added_data = [element for element in new_list if element not in old_list]
        removed_data = [element for element in old_list if element not in new_list]

        return added_data, removed_data


# MonitorTask()
