mail-sender
===========

A simple python script to send an html email using smtplib

## How to use ##

Just clone this repo and create a config.py file containing the smtp settings.

The config.py file should be located in the same repo folder. There is also a template file showing the required parameters.

To run the script just go on the shell:

```sh
./sendmail.py
```

To specify a custom template file:

```sh
./sendmail.py -t /somefile.html
```

For more help:

```sh
./sendmail.py --help
```

## License ##

Released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
