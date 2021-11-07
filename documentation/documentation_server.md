# Bard's Way server documentation #
>
> Documentation for the server.
>

## Summary: ##
- SSH access



## SSH access: ##

Port : `49550`

with the command `ssh bardsway@x2021bardsway4101150483000.northeurope.cloudapp.azure.com -p 49550`  
You have now access to the Linux server of Bard's Way.

To upload files remotely use SCP like the following `scp path/to/file root@x2021bardsway4101150483000.northeurope.cloudapp.azure.com:/path/to/file -P 49550
`

If you want to upload to the 1TO disk you need to be root.

Spleeter environment : bardspleeter  
test environment : bardstest

There is 340 GO in /mnt and 1 TO in /datadisk  
The bard's way repository is in /home/bardsway
