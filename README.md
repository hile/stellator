
VMWare Fusion headless VM control scripts
=========================================

This python module contains scripts for OS X to discover and manage
VMware Fusion virtual machines, escpecially VMs running in headless
mode that can't be controller directly by VMWare Fusion GUI.

Installing
----------

This code can be installed normally with pip:

    pip install stellator

Pip install does not currently include the files from examples directory.

Using the tool
==============

There is just one script called 'stellator' installed to your path. See --help
for all arguments what it can do.

In the command line arguments, VM names are case insensitive. You can also use
wildcards in VM name arguments

Examples
--------

* stellator list

  Lists detected virtual machines

* stallator status

  Shows status of virtual machines

* stallator status rhel*

  Shows status of virtual machines starting with name rhel

* stellator suspend facebook

  Suspends a VM called facebook

* stellator start zabbix

  Starts a VM called zabbix. If the VM was suspended, it's resumed, otherwise booted.

* stellator stop zabbix

  Shuts down a VM called zabbix.

* stellator details facebook

  Shows some configuration details parsed from the .vmx file and disk configuration.


Configuring for headless VM reboot suspend/resume
-------------------------------------------------

Following instructions expect you installed stellator to /usr/local. Adjust paths in the
script accordingly if this is not the case.

Example configuration in examples/StartupItems can be used to configure automatic suspend
and resume of headless VMs during reboots with:

    sudo install -d /Library/StartupItems/StellatorHeadless
    sudo cp examples/StartupItems/StellatorHeadless/* /Library/StartupItems/StellatorHeadless/
    sudo chown -R root:root /Library/StartupItems/StellatorHeadless/*
    sudo chmod 0644 /Library/StartupItems/StellatorHeadless/StartupParameters.plist
    sudo chmod 0755 /Library/StartupItems/StellatorHeadless/StellatorHeadless.sh

Naming and Credits
==================

Named after 'stellator' type fusion reactor design. While I don't know a thing
about fusion power, I value the efforts by the people who do.

The details how to run VMs as headless are based on the cummunity documentation in:

https://communities.vmware.com/thread/292873?tstart=0

Thanks for finding the details to allow me writing this without too much debugging.
