#!/bin/csh
#******************************************************************************
# (C) 2015, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Compares all Python files from this directory with Python files from an     *
# external directory $1                                                       *
#******************************************************************************
foreach python_file (` ls *.py */*.py `)
  echo "--- $python_file ---"
  diff $python_file $1/$python_file
end
