#!/usr/bin/env python3
import yaml
import os
import sys
import pathlib
import argparse
import subprocess
import time
from pygtail import Pygtail

alert_config = str(pathlib.Path.home()) + '/.alert.yml'

## argparse arguments
parser = argparse.ArgumentParser(description="Python alerting utility")

## Backup subparser
parser.add_argument('-c', '--config', help='path to config file', metavar='PATH', nargs='+', default=alert_config)
parser.add_argument('-p', '--path', help='path(s) to tail', metavar='PATH', nargs='+', default='', required=True)
parser.add_argument('-t', '--type', help='alert type', metavar='TYPE', default='stdout')
parser.add_argument('--title', help='alert title', metavar='TITLE', default='alert-py', type=str)

args = parser.parse_args()


def check_config(path):
    fileObj = pathlib.Path(path)
    if not fileObj.is_file():
        pathlib.Path(path).touch()
        return 0
    return 1

def check_dest(path):
    fileObj = pathlib.Path(path)
    if not fileObj.is_file(): 
        if fileObj.is_dir():
            print('Path is a directory: ' + path)
            sys.exit(1)
        else:
            print('File not found: ' + path)
            sys.exit(1)

def load_yaml_slack(path):
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        global slackToken, slackChannel
        try:
            slackToken = data.get('slack', ()).get('legacy_token')
            if slackToken == None:
                raise Error
        except:
            try:
                slackTokenCommand = data.get('slack', ()).get('legacy_token_command')
                result = subprocess.run(slackTokenCommand, shell=True, stdout=subprocess.PIPE)
                slackToken = result.stdout.decode('utf-8')
                slackToken = slackToken.strip()
            except:
                print('Unable to retrieve Slack token. Exiting.')
                sys.exit(1)
        slackChannel = data.get('slack', ()).get('channel_name')
        slackChannel = '#' + str(slackChannel)


def send_stdout_alert(output):
    print(output)

def send_slack_alert(legacyToken, channel, title, output):
    from slacker import Slacker
    from requests.sessions import Session

    with Session() as session: 
        slack = Slacker(str(legacyToken), session=session)
        channelName = str(channel)

        slack.chat.post_message(channelName, title)
        slack.chat.post_message(channelName, output)


def main():
    title = args.title
    
    config = args.config
    configExists = check_config(config)

    while True:
        for path in args.path:
            check_dest(path)

            for output in Pygtail(path):
                if args.type == 'stdout':
                    send_stdout_alert(output)
                elif args.type == 'slack':
                    load_yaml_slack(config)
                    send_slack_alert(slackToken, slackChannel, title, output)
                else:
                    print('Alert type not valid.')
                    sys.exit(1)

if __name__ == '__main__':
    main()
