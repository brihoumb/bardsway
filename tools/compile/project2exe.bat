@ECHO off

SET Arg=%1
SET ScriptPS="%~dp0project2exe.ps1"

SET ARG=%1
IF DEFINED ARG (
  IF "%ARG%"=="/i" PowerShell -NoProfil -ExecutionPolicy Unrestricted -File %ScriptPS% -install "%~dp0
) ELSE (
  PowerShell -NoProfil -ExecutionPolicy Unrestricted -File %ScriptPS% "%~dp0
)
EXIT /B 0
