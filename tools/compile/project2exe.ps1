param (
  [string]$path,
  [switch]$install = $false
)

$source = $path -replace 'tools.*', 'algorithm'

$tmp = "$HOME\bardstmp"
$old = (Get-Location).Path
cd "$path"
New-Item -ItemType Directory -Force -Path "$HOME\bardstmp" | Out-Null

$pip = "pip"
$python = "python"
$pyinstaller = "pyinstaller"

Function install_python() {
  $python = "$HOME\AppData\Local\Programs\Python\Python37\python.exe"
  $pip = "$HOME\AppData\Local\Programs\Python\Python37\Scripts\pip.exe"
  $pyinstaller = "$HOME\AppData\Local\Programs\Python\Python37\Scripts\pyinstaller.exe"
  if (!(Test-Path -path $python)) {
    wget https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe -O $HOME\bardstmp\python-install.exe
    & $tmp\python-install.exe /quiet
  }
  & $pip install -r "$path\..\requirement.txt"
}

Function build($spec, $py) {
  cp $spec $tmp
  cd $tmp
  $pathex="             pathex=[`"$source`"]," -replace '\\', '\\'
  $analysis="a = Analysis([`"$source\$py`"]," -replace '\\', '\\'
  $icon="          icon=`"$path`logo.ico`")" -replace '\\', '\\'
  (Get-Content $spec) -replace '.*pathex.*', $pathex | Set-Content $spec
  (Get-Content $spec) -replace '.*Analysis.*', $analysis | Set-Content $spec
  (Get-Content $spec) -replace '.*icon.*', $icon | Set-Content $spec
  (Get-Content $spec) -replace "path = '.'", "path = r`"$source`"" | Set-Content $spec
  & $pyinstaller --clean $spec
  $bin_built="dist\$($spec.Remove($spec.Length - 5))"
  echo "from checksumdir import dirhash`r`nprint(dirhash(r`"$bin_built`"), '-- $($spec.Remove($spec.Length - 5))')" | python | Add-Content "dist/checksum"
  Invoke-WebRequest -Uri "https://github.com/brihoumb/bardsway/releases/download/1.0.0/sciter.dll" -OutFile "$bin_built\sciter.dll"
  cd $path
}

Function retrieve_exe() {
  New-Item -ItemType Directory -Force -Path "$old\binaries" | Out-Null
  Move-Item -Path "$tmp\dist\*" -Destination "$old\binaries" -Force
  Remove-Item "$tmp\dist"
}

if ($install) {
  install_python
}

$specs = (dir *.spec).Name

forEach ($spec in $specs) {
  if ($spec -eq 'installer.spec') {
    build "$spec" "__main_installer__.py"
  } elseif ($spec -eq 'bardsway.spec') {
    build "$spec" "__main__.py"
  } else {
    build "$spec" "$($spec.Remove($spec.Length - 4))py"
  }
}

If (Test-Path "$tmp\dist" -PathType Container) {retrieve_exe}
