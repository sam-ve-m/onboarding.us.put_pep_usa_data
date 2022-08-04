#!/bin/bash

# Need pytest installed (pip install pytest)
echo "Starting tests."
mkdir testing || { echo "ERROR: Failed to create test execution folder. [FINISHING SCRIPT]"; exit; }
cp tests/pytest.ini testing/ || { echo "ERROR: Failed to set Pytest mode. [CONTINUING SCRIPT]"; }
cp -r tests/ testing/ || { echo "ERROR: Failed to copy test folder. [FINISHING SCRIPT]"; rm -rf testing; exit; }
cp -rf func/. testing/ || { echo "ERROR: Failed to copy src folder. [FINISHING SCRIPT]"; rm -rf testing; exit; }
cd testing || { echo "ERROR: Failed to change folder. [FINISHING SCRIPT]"; rm -rf testing; exit; }
export PROJECT_PATH="$PWD"
python3 ./tests/run_tests.py || { echo "ERROR: Error while running Pytest. Make sure it is installed or check if the tests ran correctly. [CONTINUING SCRIPT]";  }
cd .. || { echo "ERROR: Failed to exit test execution folder. [FINISHING SCRIPT]"; exit; }
rm -rf testing || { echo "ERROR: Failed to remove test execution folder. [FINISHING SCRIPT]"; exit; }
echo "Tests completed successfully."