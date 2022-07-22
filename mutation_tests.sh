#!/bin/bash

# Need pytest and mutatest installed (`pip install pytest` and `pip install mutatest`)
echo "Starting tests."
mkdir testing || { echo "ERROR: Failed to create test execution folder. [FINISHING SCRIPT]"; exit; }
cp tests/pytest.ini testing/ || { echo "ERROR: Failed to set Pytest mode. [CONTINUING SCRIPT]"; }
cp -r tests/ testing/ || { echo "ERROR: Failed to copy test folder. [FINISHING SCRIPT]"; rm -rf testing; exit; }
cp -rf func/. testing/ || { echo "ERROR: Failed to copy src folder. [FINISHING SCRIPT]"; rm -rf testing; exit; }
cd testing || { echo "ERROR: Failed to change folder. [FINISHING SCRIPT]"; rm -rf testing; exit; }
export PYTHONPATH="$PWD"
pytest -vv || { echo "ERROR: Error while running Pytest. Make sure it is installed or check if the tests ran correctly. [CONTINUING SCRIPT]";  }


# Mutatest
default_params="-y if nc ix su bs bc bn"
default_folder_project="src"
default_folder_test="tests"
default_locations_to_tests=1000
default_coverage_path="coverages"

src_folder=$default_folder_project
tests_folder=$default_folder_test


project_reports="../mutation_tests_reports/"


default_pytest_command="python3 -m pytest --cov-report term-missing  --cov-config=.coveragerc --cov=${src_folder} ${tests_folder}"

mutatest -s ${src_folder} ${default_params} -x 60 -n ${default_locations_to_tests} -t "${default_pytest_command}" -o ${project_reports}reports.rst ||
{ echo "ERROR: Error while running mutatest. Make sure it is installed or check if the tests ran correctly. [CONTINUING SCRIPT]";  }


# Finishing
cd .. || { echo "ERROR: Failed to exit test execution folder. [FINISHING SCRIPT]"; exit; }
rm -rf testing || { echo "ERROR: Failed to remove test execution folder. [FINISHING SCRIPT]"; exit; }
echo "Tests completed successfully."