import sys, os
from colorama import init, Fore, Style


# Init Colorama
init(autoreset=True)

# Raise error if script isn't launch on linux
if sys.platform not in ("linux", "linux2"):
    raise Exception("Bad platform, try on linux")


def update_files():
    # Update code on vm
    os.system("rm -rf bin")
    os.system("rm -rf app")
    print("Update ...")
    os.system("mkdir app")
    os.system("cp -R /mnt/time-skipper/app/. app/.")
    os.system("rm -rf buildozer.spec")
    os.system("cp -R /mnt/time-skipper/buildozer.spec buildozer.spec")
    print("Update of buildozer.spec and app/ completed")

    from app._version import __version__

    return __version__


def start_compilation():
    # Start buildozer compilation
    os.system("buildozer --verbose android debug")

    print(f"\n\n{Style.BRIGHT}{Fore.GREEN}     Compilation finished !\n\n{Fore.BLACK}")


def copy_apk(version):
    rep = input("Do you want a copy out of the vm ? (y/n) ")
    if rep.lower() == "y":
        os.system(
            f"cp -R ./bin/timeskipper-{version}-armeabi-v7a_arm64-v8a-debug.apk /mnt/time-skipper/timeskipper-{version}-armeabi-v7a_arm64-v8a-debug.apk"
        )
        print(f"{Style.BRIGHT}{Fore.GREEN}Copy done !{Fore.BLACK}")


def main():
    version = update_files()
    start_compilation()
    copy_apk(version)


if __name__ == "__main__":
    main()
