import yaml
import platform
import os
from typing import Any, Dict

def log(*args, **kwargs):
    with open("/Users/gabrielepongelli/Desktop/log.txt", "w") as f:
        f.write(f"{args}{kwargs}")


def get_extension(icon: bool = False, installer: bool = False) -> str:
    """Get the right extension for the file specified.

    Args:
        icon (bool, optional): get the icon extension. Default to False.
        installer (bool, optional): get the installer extension. Default to False.

    Returns:
        str: the extension name.
    """

    if icon:
        options = ("ico", "icns")
    elif installer:
        options = ("nsi", "scpt")
    else:
        options = None

    if platform.system() == "Windows":
        return options[0]
    else:
        return options[1]


class Config:
    def __init__(self, config_file: str = "config.yml") -> None:
        """Initialize a new configuration object.

        Args:
            config_file (str, optional): file where the configurations are
            stored. Defaults to "config.yml".
        """

        self._config = self._read_config(config_file)
    
    def _read_config(self, config_file: str) -> Dict[str, str]:
        """Load configutayions from file the config file.

        Args:
            config_file (str): file where the configurations are stored.

        Returns:
            Dict[str, str]: the configurations read.
        """

        try:
            result = yaml.safe_load(open(config_file, "r"))
        except:
            # if on macos it could be an alias, so if we are in the .app bundle it will be in ../Resources
            if platform.system() == "Darwin":
                config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + ".." + os.sep + "Resources" + os.sep + config_file
                result = yaml.safe_load(open(config_file, "r"))
        
        return result

    def get_property(self, property_name: str) -> Any:
        """Get the value of the specified property.

        Args:
            property_name (str): name of the property.

        Returns:
            Any: the value stored.
        """

        if property_name not in self._config.keys():
            return None
        else:
            return self._config[property_name]


class AppConfig(Config):
    """Configurations needed by the application."""

    @property
    def app_name(self) -> str:
        return self.get_property("APP_NAME")

    @property
    def app_icon(self) -> Dict[str, str]:

        result = {
            "name": self.get_property("APP_ICON_NAME"),
            "extension": "." + get_extension(icon=True),
            "path": (
                "."
                + os.sep
                + self.get_property("APP_NAME")
                + os.sep
                + "resources"
                + os.sep
                + "icons"
                + os.sep
                + platform.system().lower()
                + os.sep
            ),
        }

        return result


class BuildConfig(AppConfig):
    """Configurations needed in the building process."""

    @property
    def app_icon(self) -> Dict[str, str]:

        result = super().app_icon
        result["path"] = (
            os.path.dirname(os.path.realpath(__file__)) + result["path"].split(".")[1]
        )

        return result

    @property
    def entrypoint(self) -> str:
        return self.get_property("ENTRY_POINT")

    @property
    def version(self) -> str:
        return self.get_property("VERSION")

    @property
    def author(self) -> str:
        return self.get_property("AUTHOR")

    @property
    def apple_background_image_name(self) -> Dict[str, str]:

        image_full_name: str = self.get_property("APPLE_BACKGROUND_IMAGE_NAME")

        result = self.installer
        result["name"] = image_full_name.split(".")[0]
        result["extension"] = "." + image_full_name.split(".")[1]

        return result

    @property
    def installer(self) -> Dict[str, str]:
        result = {
            "name": "installer",
            "extension": "." + get_extension(installer=True),
            "path": (
                os.path.dirname(os.path.realpath(__file__))
                + os.sep
                + "installer"
                + os.sep
                + platform.system().lower()
                + os.sep
            ),
        }

        return result

    @property
    def output_path(self) -> str:
        return os.path.dirname(os.path.realpath(__file__)) + os.sep + "dist" + os.sep
