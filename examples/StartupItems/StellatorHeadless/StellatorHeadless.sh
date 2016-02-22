#!/bin/sh
#
# Example startupitem script to suspend and resume running headless VMs.
#
# Expects install prefix /usr/local - fix as needed
#

. /etc/rc.common

INSTALL_PREFIX="/usr/local"

# Make sure custom modules are available on python path
export PYTHONPATH="$PYTHONPATH:$INSTALL_PREFIX/lib/python2.7:$INSTALL_PREFIX/lib/python2.7/site-packages"

# Resume headless VMs with 'autoresume' flag set by StopService command
StartService()
{
    "$INSTALL_PREFIX/bin/stellator" resume
}

# Suspend running headless VMs and add 'autoresume' flag to resume these (but not other suspended VMs)
StopService()
{

    "$INSTALL_PREFIX/bin/stellator" suspend --autoresume
}

RunService "$1"
