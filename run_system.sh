#!/usr/bin/env bash

setup_venv()
{
    ${PYTHON_INTERPRETER} -m venv $SYSTEM_WORKSPACE/venv --without-pip
    source $SYSTEM_WORKSPACE/venv/${PIP_PATH}/activate
    curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_INTERPRETER
    pip install -r $SYSTEM_WORKSPACE/requirements.txt
}

setup_folders()
{
if [[ ! -d $SYSTEM_WORKSPACE/venv ]]; then
    echo "Virtual environment not found. Setting up a new venv."
    setup_venv
else
    source $SYSTEM_WORKSPACE/venv/${PIP_PATH}/activate
fi

if [[ ! -d $SYSTEM_WORKSPACE/media ]]; then
    mkdir $SYSTEM_WORKSPACE/media
fi
}

main()
{
export SYSTEM_WORKSPACE=$PWD

setup_folders

python anti_theft_system.py
}

os_check()
{
case "$(uname -s)" in

	Linux)
		PYTHON_INTERPRETER=python3
		PIP_PATH=bin
		;;
	CYGWIN*|MINGW32*|MSYS*)
		PYTHON_INTERPRETER=python
		PIP_PATH=Scripts
		;;
esac
}

os_check
main
#EOF