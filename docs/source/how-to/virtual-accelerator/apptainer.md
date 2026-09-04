# Installing Apptainer

Virtual accelerators are deployed as [Apptainer](https://apptainer.org/) containers.

Instructions for how to install and run Apptainer on different OS are available here.

## Linux

Installation instructions are available at <https://apptainer.org/docs/admin/main/installation.html#installation-on-linux>.

Try to first install using the [pre-build packages](https://apptainer.org/docs/admin/main/installation.html#install-from-pre-built-packages) for your Linux distribution.

If that doesn't work (for example if it requires root permissions which you don't have), do an [unprivileged installation](https://apptainer.org/docs/admin/main/installation.html#install-from-pre-built-packages) instead.

You should then be able to run Apptainer in a terminal.

## Windows

For Windows you need to install and run in [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/). Follow the instructions at <https://apptainer.org/docs/admin/main/installation.html#windows>.

You can then start the Ubuntu app which opens a Linux terminal where you can run Apptainer.

## Mac

For Mac you need to use Lima. Instructions are available at <https://apptainer.org/docs/admin/main/installation.html#mac> but more detailed instructions are below since some additonal steps are required.

For ARM-based MacOS server:

```
brew install qemu lima

limactl start –rosetta –vm-type=vz –network=vzNAT template://apptainer
```

For Intel-based MacOS server:

```
brew install lima

limactl start –vm-type=vz –network=vzNAT template://apptainer
```

To run a container you need to first do the following command before you can run Apptainer:

```
limactl shell apptainer
```

To stop the container you need to do:

```
limactl stop apptainer

limactl delete apptainer
```
