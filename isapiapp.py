#!python
from __future__ import print_function

from jaraco.site.isapi import (
	factory as __ExtensionFactory__,
	handle_command_line, setup_environment,
	)
print('setting up environment')
setup_environment(__file__)
print('done setting up environment')
if __name__ == '__main__': handle_command_line()
