import os
import json
from threading import Thread, Lock
from typing import Any
from inquirer import List, prompt
from importlib import import_module
import platform

# TODO - Profiles and random profile
# TODO - Cleanup windows code


def get_directories(entries: list) -> list:
    """Filter a path containing possibly files & folders to only folders.

    Arguements:
        path: A path string of a directory.
        aEntries: A list of entries objects.

    Returns:
        [str, str]: List of strings of all folder paths.
    """
    directories = [
        entry.path
        for entry in entries
        if entry.is_dir() and not entry.name.startswith("__")
    ]
    return directories


def get_all_sites(path: str) -> list:
    """Read directory and extract all site names from folders.

    Arguements:
        path: A path string where the site folders are located.

    Returns:
        List of strings of all site paths.
    """
    DEPTH_LIMIT = 2  # How many folders deep to check
    site_paths = []

    with os.scandir(path) as entries:
        possible_site_folders = get_directories(entries)

        # Remove old folder from possible site folders
        possible_site_folders = [
            folder_path
            for folder_path in possible_site_folders
            if not folder_path.endswith("old")
        ]

        current_folders_to_check = possible_site_folders
        next_folders_to_check = []

        # Only go to a certain depth (folders in folders)
        for _ in range(0, DEPTH_LIMIT):
            # Check each folder path for more folders or Task.py files
            for folder_path in current_folders_to_check:
                directories = []

                with os.scandir(folder_path) as entries:

                    for entry in entries:
                        # If entry is a directory
                        if entry.is_dir():
                            directories.append(entry.path)
                        # If entry is a Task.pyp file
                        if entry.path.endswith("Task.py"):
                            # print(f"Got Task.py file in {folder_path}")
                            site_paths.append(folder_path)

                if directories:
                    next_folders_to_check = [*next_folders_to_check, *directories]

            current_folders_to_check = next_folders_to_check
            next_folders_to_check = []

    return site_paths


class BotStartupHandler:
    """Used to load all info to start tasks on a specific site.

    Attributes:
        tasks_created: Amount of tasks created

    """

    def __init__(self) -> None:
        self.tasks_created = 0

    def do_startup(self, site_paths: list) -> list:
        """Loads everything and starts tasks.

        Arguements:
            site_paths: List of all site paths

        Returns:
            A list of thread objects.
        """
        user_site = self.get_user_site(site_paths)
        if platform.system() == "Windows":
            module_path = ".".join(user_site.split("/")[1:]).replace("\\", ".")
            module = import_module(f"{module_path}.Task")
        else:
            module = import_module(f"{'.'.join(user_site.split('/')[1:])}.Task")

        settings = self.get_all_settings()
        if platform.system() == "Windows":
            tasks = self.get_all_tasks(user_site.split("\\")[-1])
        else:
            tasks = self.get_all_tasks(user_site.split("/")[-1])

        default_file = [task for task in tasks if task.endswith("default.json")]
        if default_file:
            task_file, task_file_path = self.get_user_task(
                chosen_task_path=default_file[0]
            )
        else:
            task_file, task_file_path = self.get_user_task(tasks=tasks)

        task_file_path = default_file[0]
        task_file_settings = None

        if type(task_file) == list:
            all_task_data = task_file
        elif "tasks" in task_file.keys():
            all_task_data = task_file["tasks"]
            if "settings" in task_file.keys():
                task_file_settings = task_file["settings"]
            else:
                task_file_settings = None
        else:
            raise Exception("Invalid tasks file format")

        kill_task_list = []
        thread_lock = Lock()
        profiles = self.get_profiles()

        # Custom code for each site

        site_name_lower = user_site.split("/")[-1]
        if site_name_lower == "redacted":
            if len(all_task_data) > 1:
                print("Can only run 1 task for redacted")
                quit()

        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        for task_file_json in all_task_data:
            task_file_json["taskFilePath"] = task_file_path
            if task_file_settings:
                task_file_json["taskFileSettings"] = task_file_settings

            # Override settings if they are set in a tasks file
            if (
                task_file_settings
                and "webhookURL" in task_file_settings.keys()
                and task_file_settings["webhookURL"]
            ):
                settings["webhookURL"] = task_file_settings["webhookURL"]

            if (
                task_file_settings
                and "monitorDelay" in task_file_settings.keys()
                and task_file_settings["monitorDelay"]
            ):
                settings["monitorDelay"] = task_file_settings["monitorDelay"]

            if (
                task_file_settings
                and "errorDelay" in task_file_settings.keys()
                and task_file_settings["errorDelay"]
            ):
                settings["errorDelay"] = task_file_settings["errorDelay"]

            try:
                profile_selected = self.get_selected_profile(
                    profiles, task_file_json["profile"]
                )
            except KeyError:
                profile_selected = {"HI": "NO PROFILE !  ! !"}

            thread = Thread(
                target=module.Task,
                args=(
                    thread_lock,
                    kill_task_list,
                    self.tasks_created + 1,
                    settings,
                    task_file_json,
                    profile_selected,
                ),
                daemon=True,
            )

            thread.start()
            self.tasks_created = self.tasks_created + 1

        return kill_task_list

    def get_profiles(self):
        with open("./settings/profiles.json") as f:
            return json.load(f)

    def get_selected_profile(self, profiles, profile_name):
        return [
            profile for profile in profiles if profile["profileName"] == profile_name
        ][0]

    def get_user_task(self, tasks: list = [], chosen_task_path: str = "") -> list:
        """Display a list of tasks for current site and returns
        site name based on users selection.

        Args:
            tasks (list): A list of task paths.
            chosen_task_path (str): A task path that has already been selected
                meaning there will be no task selection.

        Returns:
            List:
                dict: The selected task JSON data.
                str: The selected task file path.
        """
        if tasks:
            all_task_names = [task.split("/")[-1] for task in tasks]

            questions = [
                List(
                    "task",
                    message="Please select a task",
                    choices=all_task_names,
                )
            ]
            chosen_task = prompt(questions)["task"]
            chosen_task_path = [path for path in tasks if path.endswith(chosen_task)][0]
        else:
            chosen_task_path = chosen_task_path

        with open(chosen_task_path) as f:
            data = json.load(f)

        return data, chosen_task_path

    def get_all_tasks(self, site_name: str) -> list:
        """Returns a list of task file paths.

        Args:
            site_name (str): Site name, used in path.

        Returns:
            list: Task file paths.
        """
        with os.scandir(f"settings/tasks/{site_name}") as entries:
            tasks = [entry.path for entry in entries if entry.path.endswith(".json")]

        return tasks

    def get_user_site(self, site_paths) -> str:
        """Display a list of sites for the user to chose from
            and return the site name.

        Arguements:
            site_paths: A path string where the site folders are located.

        Returns:
            String of chosen site path.
        """
        all_site_names = []
        for site_path in site_paths:
            if "monitors" in site_path:
                all_site_names.append(f"{site_path.split('/')[-1]} - Monitor")
            else:
                all_site_names.append(site_path.split("/")[-1])

        def is_monitor(site):
            return " - Monitor" in site

        all_site_names.sort(key=is_monitor)
        if platform.system() == "Windows":
            chosen_site = self.get_choice_from_list(all_site_names)
        else:
            questions = [
                List(
                    "site",
                    message="Please select a site",
                    choices=all_site_names,
                )
            ]
            chosen_site = prompt(questions)["site"]

        chosen_site = chosen_site.split(" - ")[0]
        chosen_site_path = [path for path in site_paths if path.endswith(chosen_site)][
            0
        ]
        return chosen_site_path

    def get_choice_from_list(self, choices: list):
        """Returns a user choice from list of choices.

        Args:
            choices (list): A list of choices.

        Returns:
            Any: The chosen item from list.
        """
        for index, choice in enumerate(choices):
            print(f"[{index+1}] - {choice}")

        selection = input("Please make a selection: ")
        return choices[int(selection) - 1]

    def get_all_settings(
        self,
        settings_path: str = "./settings",
        settings_files: list = ["settings.json", "settings_dev.json"],
    ) -> dict:
        """Reads and combines JSON files.

        Arguements:
            settings_path: A path string where the settings files are located,
                format: './settings.
            settings_files: A list of strings of the settings file names,
                file name with extension included.

        Returns:
            Settings: A dictionary of all settings combined.
        """
        settings_all = {}
        for file in settings_files:
            with open(f"{settings_path}/{file}") as f:
                settings_all = {**settings_all, **json.load(f)}

        # # Adding killTaskData to control the threads
        # settings_all = {
        #     **settings_all,
        #     "killTaskData": {"shouldKill": False, "isKilled": False},
        # }

        return settings_all
