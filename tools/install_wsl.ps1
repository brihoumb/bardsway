$WSL = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
if ($WSL.statue = 0) {
  Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
  md $HOME\bardstmp
  Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile $HOME\bardstmp\Ubuntu.appx -UseBasicParsing
  Add-AppxPackage $HOME\bardstmp\Ubuntu.appx
  shutdown -r -t 60
}

if([System.IO.File]::Exists($HOME\bardstmp)){
  Invoke-WebRequest -URi https://netix.dl.sourceforge.net/project/vcxsrv/vcxsrv/1.20.5.1/vcxsrv-64.1.20.5.1.installer.exe -OutFile $HOME\Downloads\vcxsrv_installer.exe
  wsl
  wsl -- "sudo apt update && sudo apt upgrade && sudo apt install git openssh python3.7 python3-pip"
  wsl -- "echo "export DISPLAY=localhost:0" >> ~/.bashrc"
}