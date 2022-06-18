# Comiks

Comiks is a command line tool to retrieve authors informations (names and emails) in the repository commits of a given user.

![Example](./doc/heading.png)

## Installation

```shell
$ pip install git+https://github.com/b0oml/Comiks
```

## Configuration

The first time `comiks` runs, it will generate a config file `.config/comiks/config.toml` in your home directory. This will be the default configuration file used when using comiks.

By default, only Github provider is enabled, other providers needs an API key/access token. To enable and configure others providers, you can update the configuration file in your home directory.

It is also possible to load the configuration file from another path with option `-c, --config`.

```shell
$ comiks -c ./path/to/config.toml username
```

If you wan to create your own configuration file, you can take example on [this one](./comiks/config.toml).

## Usage

```shell
$ comiks --help
usage: comiks [-h] [-c CONFIG] [-l HIGHLIGHT] [-p TAGS] [-sb] username

Retrieve authors informations from commits.

positional arguments:
  username              Username for which to scan commits.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Custom config file (default is ~/.config/comiks/config.toml).
  -l HIGHLIGHT, --highlight HIGHLIGHT
                        Strings to highlight in output, separated by a comma (default is username).
  -p TAGS, --providers TAGS
                        Comma-sperated list of tags to select which providers to enable (default is in
                        config).
  -sb, --show-branches  Show in which branches authors have been found.
```

### Examples

Normal scan, use config in home directory.

```shell
$ comiks b0oml
```

Scan using another config.

```shell
$ comiks -c my_config.toml b0oml
```

In tables output, comiks try to highlight names and emails similar to the given username. You can highlight based on other strings than the username by giving a comma-separated list of strings.

```shell
$ comiks -l john b0oml
$ comiks -l john,doe,something b0oml
```

You can enable/disable availables providers by updating config.toml. Now, let's imagine you have configured all the providers. But, for a given username, you only want to launch one of the providers. Rather than modifying the config each time this happens, you can select which provider to launch with tags.

```shell
$ comiks -p github,bitbucket b0oml
$ comiks -p gitlab b0oml
```

## Providers

Below is listed all providers currently implemented.

| Name      | Url                            | Authentication                                        | Enabled by default | Tags        |
| --------- | ------------------------------ | ----------------------------------------------------- | ------------------ | ----------- |
| GitHub    | [github.com](github.com)       | Not needed, but allows to get a higher API rate limit | yes                | `github`    |
| GitLab    | [gitlab.com](gitlab.com)       | Needed                                                | no                 | `gitlab`    |
| Bitbucket | [bitbucket.org](bitbucket.org) | Needed                                                | no                 | `bitbucket` |
