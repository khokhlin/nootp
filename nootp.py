"""Cisco AnyConnect VPN without a cellphone"""
import os
import configparser
import argparse
import pyotp


def get_config(configfile=None):
    config = configparser.ConfigParser()
    cfgpath = configfile or os.path.expanduser("~/.nootp.ini")
    if not os.path.exists(cfgpath):
        config.add_section("auth")
        config["auth"]["secret"] = input("Secret: ")
        config["auth"]["prefix"] = input("Prefix (optional): ")
        config["auth"]["postfix"] = input("Postfix (optional): ")
        with open(cfgpath, "w") as cf:
            config.write(cf)
    else:
        config.read(cfgpath)
    return config


def parse_args():
    parser = argparse.ArgumentParser("Cisco Anyconnect VPN in one click")
    parser.add_argument("-c", "--config")
    parser.add_argument("--clip", action="store_true",
                        default=False, help="Copy to clipboard on Windows")
    return parser.parse_args()


def main():
    args = parse_args()
    config = get_config(configfile=args.config)

    secret = pyotp.totp.TOTP(config["auth"]["secret"]).now()
    result = "{prefix}{secret}{postfix}".format(
        prefix=config["auth"]["prefix"] or "",
        secret=secret,
        postfix=config["auth"]["postfix"] or "")

    if args.clip:
        if os.system("echo '" + result + "' | clip") != 0:
            print("Clipboard is unavailable")
    else:
        print(result)


if __name__ == "__main__":
    main()
