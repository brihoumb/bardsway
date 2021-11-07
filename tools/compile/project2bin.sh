#!/bin/bash
path=$(realpath "$0")
path="${path%${path##*/}}"
old="$PWD"
cd "$path"
source=$(echo $path | sed 's/tools.*/algorithm/')

tmp="/tmp/bardsway"
mkdir -p "$tmp"

build() {
  cp "$arg" "$tmp"
  cd "$tmp"
  analysis="a = Analysis([\"$source/$2\"],"
  pathex="\ \ \ \ \ \ \ \ \ \ \ \ pathex=[\"$source\"],"
  sed -i "/pathex/c\ $pathex" $arg
  sed -i "/Analysis/c\\$analysis" $arg
  sed -i "/path = '.'/c\\path = \"$source\"" $arg
  pyinstaller --clean "$1"
  bin_built="dist/${arg::-5}"
  echo -e "from checksumdir import dirhash\nprint(dirhash(\"$bin_built\"), '-- ${arg::-5}')" | python >> "dist/checksums"
  curl "https://github.com/brihoumb/bardsway/releases/download/1.0.0/libsciter-gtk.so" -o "$bin_built/libsciter-gtk.so"
  cd "$path"
}

retrieve_bin() {
  mkdir -p "$old/binaries"
  mv $tmp/dist/* "$old/binaries"
  cd "$old"
  rm -rf "$tmp/dist"
}

args=($(ls -d *.spec))

for arg in "${args[@]}"; do
  if [[ "$arg" == "installer.spec" ]]; then
    build "$arg" "__main_installer__.py"
  elif [[ "$arg" == "bardsway.spec" ]]; then
    build "$arg" "__main__.py"
  else
    build "$arg" "${arg%${arg##*.}}py"
  fi
done

[ -d "$tmp/dist" ] && retrieve_bin
