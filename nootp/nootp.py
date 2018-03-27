"""Cisco AnyConnect VPN without a cellphone"""

import os
import sys
import binascii
import configparser
import argparse
import time
import pyotp
import pyperclip


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


def clear_clipboard(content):
    old_content = pyperclip.paste()
    if old_content == content:
        pyperclip.copy(" ")


def parse_args():
    parser = argparse.ArgumentParser("Cisco Anyconnect VPN in one click")
    parser.add_argument("-c", "--config")
    parser.add_argument("--copy", action="store_true",
                        default=False, help="Copy to clipboard")
    parser.add_argument("--clear-timeout", "-ct", type=int, default=10,
                        help="Timeout before clearing clipboard")
    return parser.parse_args()


def main():
    args = parse_args()
    config = get_config(configfile=args.config)

    secret = config["auth"]["secret"]
    try:
        secret = pyotp.totp.TOTP(secret).now()
    except binascii.Error:
        sys.exit("Mailformed secret")

    result = "{prefix}{secret}{postfix}".format(
        prefix=config["auth"]["prefix"] or "",
        secret=secret,
        postfix=config["auth"]["postfix"] or "")

    func = pyperclip.copy if args.copy else print
    func(result)

    if args.copy and args.clear_timeout > 0:
        time.sleep(args.clear_timeout)
        clear_clipboard(result)


if __name__ == "__main__":
    main()
