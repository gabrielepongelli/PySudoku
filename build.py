import os
import platform
import tempfile
import subprocess
from shutil import copy, copytree
from config import BuildConfig


def get_dir_size(dir_path: str = ".") -> int:
    """Get the total size of the dir specified.

    Args:
        dir_path (str, optional): path of the dir to use. Defaults to ".".

    Returns:
        int: the total size in bytes.
    """

    total_size = 0
    for dirpath, _, filenames in os.walk(dir_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):  # skip if it is symbolic link
                total_size += os.path.getsize(fp)

    return total_size


def replace_personal_values(
    script: str,
    app_name: str,
    background: str = None,
    icon: str = None,
    app_position: str = None,
    output_position: str = None,
    version: str = None,
    author: str = None,
) -> str:
    """Replace personal values inside the script string.

    Args:
        script (str): string to modify.
        app_name (str): name of the app.
        background (str, optional): background image name. Defaults to None.
        icon (str, optional): path of the icon to use. Defaults to None.
        app_position (str, optional): path of the app to include. Defaults to None.
        output_position (str, optional): path where the output should be saved. Defaults to None.
        version (str, optional): version number of the app. Defaults to None.
        author (str, optional): author of the app. Defaults to None.

    Returns:
        str: the script personalized with the specified values.
    """

    replaceables = [
        (app_name, "APP_NAME"),
        (icon, "ICON"),
        (background, "BACKGROUND"),
        (app_position, "APP"),
        (output_position, "OUTPUT"),
        (version, "VERSION"),
        (author, "AUTHOR"),
    ]

    replaceables = {key: value for value, key in replaceables if value is not None}

    for key, value in replaceables.items():
        script = script.replace(f"###{key}###", value)

    return script


def personalize_script(input_path: str, output_path: str, **kwargs) -> None:
    """Read and write the modified script.

    Args:
        input_path (str): path where to find the script to modify.
        output_path (str): path where to save the modified script.
    """

    with open(input_path, "r") as f:
        script = f.read()

    script = replace_personal_values(script=script, **kwargs)

    with open(output_path, "w") as f:
        f.write(script)


if __name__ == "__main__":

    conf = BuildConfig()

    # generatig the exec
    separator = ";" if platform.system() == "Windows" else ":"
    app_icon = (
        conf.app_icon["path"] + conf.app_icon["name"] + conf.app_icon["extension"]
    )
    if platform.system() == "Windows":
        app_icon_dest_path = (
            "."
            + conf.app_icon["path"].split(
                os.path.dirname(os.path.realpath(__file__))
            )[1]
        )
    else:
        app_icon_dest_path = "." + os.sep
    subprocess.run(
        f"pyinstaller {conf.entrypoint} -w -y -n {conf.app_name} -i {app_icon} --add-data={app_icon + separator + app_icon_dest_path} --add-data=config.yml{separator + '.' + os.sep}",
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("Executable folder created.")

    if platform.system() == "Windows":
        with tempfile.TemporaryDirectory() as dirpath:
            personalize_script(
                conf.installer["path"]
                + conf.installer["name"]
                + conf.installer["extension"],
                dirpath + os.sep + conf.installer["name"] + conf.installer["extension"],
                app_name=conf.app_name,
                icon=app_icon,
                app_position=conf.output_path + conf.app_name,
                output_position=conf.output_path + conf.app_name + "Setup.exe",
                version=conf.version,
                author=conf.author,
            )
            subprocess.run(
                f"makensis {dirpath + os.sep + conf.installer['name'] + conf.installer['extension']}",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            print("Installer created.")

    else:
        with tempfile.TemporaryDirectory() as dirpath:
            # copy the app bundle in the temp dir
            temp_bundle_path = dirpath + os.sep + "bundle"
            os.mkdir(temp_bundle_path)
            copytree(
                conf.output_path + conf.app_name + ".app",
                temp_bundle_path + os.sep + conf.app_name + ".app",
            )

            # calculate the size of the dmg
            size = (
                get_dir_size(temp_bundle_path + os.sep + conf.app_name + ".app")
                // (1024 ** 2)
            ) + 5  # MB
            output_name = dirpath + os.sep + "temp.dmg"

            # create the dmg
            subprocess.run(
                f"hdiutil create -srcfolder {temp_bundle_path} -volname {conf.app_name} -fs HFS+ -fsargs '-c c=64,a=16,e=16' -format UDRW -size {size}m {output_name}",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            print("Dmg file created.")

            # mount the dmg file and get its path
            device_path = (
                os.popen(
                    "hdiutil attach -readwrite -noverify -noautoopen '%s' | egrep '^/dev/' | sed 1q | awk '{print $1}'"
                    % output_name
                )
                .readline()
                .strip()
            )

            # copy the background image in the hidden temp dir
            background_path = (
                os.sep + "Volumes" + os.sep + conf.app_name + os.sep + ".background"
            )
            os.mkdir(background_path)
            background_image = (
                conf.apple_background_image_name["path"]
                + conf.apple_background_image_name["name"]
                + conf.apple_background_image_name["extension"]
            )
            copy(
                background_image,
                background_path,
            )

            # personalize the script with the app data
            personalize_script(
                conf.installer["path"]
                + conf.installer["name"]
                + conf.installer["extension"],
                dirpath + os.sep + conf.installer["name"] + conf.installer["extension"],
                app_name=conf.app_name,
                background=conf.apple_background_image_name["name"]
                + conf.apple_background_image_name["extension"],
            )

            # execute the script
            subprocess.run(
                f"cat {dirpath + os.sep + conf.installer['name'] + conf.installer['extension']} | osascript",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            print("Dmg layout setted.")

            # finalize the dmg creation
            if os.path.exists(conf.output_path + conf.app_name + ".dmg"):
                os.remove(conf.output_path + conf.app_name + ".dmg")

            subprocess.run(
                f"chmod -Rf go-w /Volumes/{conf.app_name}",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            subprocess.run(
                f"hdiutil detach {device_path}",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            subprocess.run(
                f"hdiutil convert '{output_name}' -format UDZO -imagekey zlib-level=9 -o {conf.output_path + conf.app_name}",
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            print("Installer created.")
