# Bard's Way development environment #
>
> Instruction to install and use Bard's Way on Windows10.
>

## Summary: ##
- Install the WSL
  - Command Line
  - Graphical Mode
- Configure the WSL and tools

## Install the WSL ##
### • In Command Line ###
> In an admin powershell (⊞Win + X then A).

To install the Windows Subsystem Linux you'll need to enable the feature then reboot.
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```
After rebooting run the follow commands:
```powershell
md $HOME\bardstmp
Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile $HOME\bardstmp\Ubuntu.appx -UseBasicParsing
Add-AppxPackage $HOME\bardstmp\Ubuntu.appx
ubuntu #If you don't want to create a user and only use root (not recommended) just close the terminal and open it again
```

### • In Graphical Mode ###
> You need to be administrator of your machine.

Press ⊞Win and search for 'turn windows features' (Whatsoever your system language).  
Check the Windows Subsystem for Linux.  
Reboot.  
Open the Microsoft Store and search for Ubuntu 18.04 LTS and download it.  
Press ⊞Win and open Ubuntu 18.04.

## Configure the WSL and tools ##
When it's installed you can run normal linux command.  
You'll first be invited to run the following:  
```bash
sudo apt update && sudo apt upgrade && sudo apt install git openssh python3-pip python3.7 && echo "export DISPLAY=localhost:0" >> ~/.bashrc && powershell.exe Invoke-WebRequest -URi https://netix.dl.sourceforge.net/project/vcxsrv/vcxsrv/1.20.5.1/vcxsrv-64.1.20.5.1.installer.exe -OutFile $HOME\Downloads\vcxsrv_installer.exe
```
Install vcxsrv and startXLaunch in 'Multiple windows' with display number set at -1 when you need a X server for your WSL.  
After everything is installed you can push your new SSHkey (```ssh-keygen && cat ~/.ssh/id_rsa.pub```) on github and clone the Bard's Way repository.  
Finally checkout to dev and run ```bash
python3.7 -m pip install -r ./tools/requirement.txt```  
And you are ready to run graphics on Windows 10.