## alert

Alert is a simple tool for tailing a file (or multiple files) and then sending an alert when content is appended to the file.


## Configuration:

For the alerts that require additional configuration, alerts will look at `~/.alert.yml` for configuration. Refer to the individual alert documentation for how to configure this file.


## Usage:

Alert can be configured to deliver the following alerts:

stdout -- log changes to stdout
slack -- post a message to Slack via a legacy token


### stdout:

In order to use the `stdout` alert, one only needs to supply the path to the file(s) to watch:

`./alert.py --path /path/to/file`


### slack:

In order to use the `slack` alert, configure `slack` in `~/.alert.yml`:

```
---
slack:
  channel_name: my_channel
  legacy_token_command: 'gpg --decrypt /tmp/gpg.asc'
  #legacy_token: xxxx-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Set `legacy_token_command` to a command that retrieves your legacy token API key. Alternatively set the value of `legacy_token` to equal your legacy token.

Then use `slack` as the value for the `--type` flag when running `alert.py`, like so:

`./alert.py --path ~/Downloads/tmp.txt --type slack`
