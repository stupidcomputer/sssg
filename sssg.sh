#!/bin/sh

if [ "$1" = "-h" ]; then
	cat <<EOF
ssg.sh
-h: print help
-s: spin up an http server with python3 -m http.server
-d: deploy website to beepboop.systems
EOF
	exit
fi

# if we're trying to do anything, check if the directory has a valid root
if [ ! -f ".sssg_generated" ]; then
	printf "it doesn't seem like I'm in a static site directory -- is that true?\n"
	exit 1
fi

if [ "$1" = "-s" ]; then
	python3 -m http.server -d output
	exit
fi

if [ "$1" = "-d" ]; then
	if [ -f ".deploy" ]; then
		sh ./.deploy
	else
		printf "configure a deploy script first!\n"
		exit 1
	fi

	exit
fi

files=$(find -type f | grep -v "output/")
directories=$(find -type d | grep -v "output/")

IFS='
'

mkdir -p ./output

# if there's special things that need to run, run them
if [ -f ".special_commands" ]; then
	sh ./.special_commands
fi

for i in $directories; do
	if [ ! "$i" = "./output" ]; then
		mkdir -p "./output/$i"
	fi
done

# only commits with 'CHANGE' in them go into the changelog
git log --grep 'CHANGE' > output/changelog.rst
pandoc -s --template=./template.html -f rst -t html -o "output/changelog.html" "output/changelog.rst"
rm changelog.rst

set -x
for i in $files; do
	without_extension=${i%.*}
	case $i in
		*.rst)
			pandoc -s --template=./template.html -f rst -t html -o "output/$without_extension.html" "$without_extension.rst"
			;;
		"./ssg.sh") # don't copy this file
			;;
		"./shell.nix") # ditto
			;;
		"./template.html")
			;;
		*)
			cp "$i" "output/$i"
			;;
	esac
done
set +x
