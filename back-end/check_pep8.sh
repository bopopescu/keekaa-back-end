#!/bin/bash
FILES=`find ./* -name '*.py' | grep -v '/dist-packages/' | grep -v '/migrations/' | grep -v 'tests.py'`

PYTHONPATH=$PWD:$PWD/website:$PWD/website/dist-packages:${PYTHONPATH:+:$PYTHONPATH} 
export PYTHONPATH

pep8_result=$(pep8  --statistics $FILES 2>&1)
if [ -z "$pep8_result" ]; then
   pep8_status="Pass!"
else
   pep8_status="Fail!"
fi

pyflakes=$(pyflakes $FILES 2>&1)
if [ -z "$pyflakes" ]; then
   pyflakes_status="Pass!"
else
   pyflakes_status="Fail!"
fi

pychecker_result=$(pychecker $FILES 2>&1)
pylint_result=$(pylint --include-ids=y $FILES 2>&1)

pylint_scores=`echo "$pylint_result" | grep 'Your code has been rated at'`
pylint_scores=`echo ${pylint_scores:28}` 

echo "Pep8, pyflakes, pychecker, and pylint have been run to enforce python code style/standards, 
and the code is rated at $pylint_scores by pylint.  

The following is the report.


Pep8 Test Result: $pep8_status

$pep8_result 

Pyflakes Test Result: $pyflakes_status

$pyflakes

Pychecker Test Result:

$pychecker_result

Pylint Test Result:

$pylint_result"
