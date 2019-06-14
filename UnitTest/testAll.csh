#!/bin/csh
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
setenv PYTHONPATH ${HOME}/Python/SpacePyLibrary
setenv HOST 127.0.0.1
setenv TESTENV ../TESTENV
foreach test_file (` grep unittest *.py | grep import  | sed s/":.*"//g `)
  echo "*** $test_file ***"
  ./${test_file}
end
