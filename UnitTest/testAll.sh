#!/bin/sh
#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under under the terms of the MIT License as published by the      *
# Massachusetts Institute of Technology.                                      *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the MIT License    *
# for more details.                                                           *
#******************************************************************************
# Start scrip for an overall Unit Test.                                       *
#******************************************************************************
export PYTHONPATH=${HOME}/Python/SpacePyLibrary
export HOST=127.0.0.1
export TESTENV=../TESTENV
export PYTHON=python3
for test_file in `grep unittest *.py | grep import | sed s/":.*"//g`
do
  echo "*** $test_file ***"
  ${PYTHON} -m unittest -b ${test_file}
done
