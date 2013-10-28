Background

This directory contains the examples found in the book entitled:
Bayesian Programming.

This package supports Ubuntu Linux Desktop version 12.04 or higher.

"MyDirectory" denotes the directory where you have installed the
package and XX denotes the type of machine you are using (a 64 or 32
bit machine).

You are reading "MyDirectory/ProBtLinuxXX/README.txt". 

The examples of each chapter may be found in the corresponding
sub-directories of "MyDirectory/ProBtLinuxXX/Examples".

The library as well as the Python bindings are located in
 "MyDirectory/ProBtLinuxXX/pypl"


Documentation

The reference documentation is useful for users of the Python bindings
of ProBT willing to modify and run the programs found in the bayesian
programming book. To get started, point your web browser at
  "MyDirectory/ProBtLinuxXX/Documentation/index.html"

Please note that this documentation is designed for c++
programmers. 98% of the functions share the same names, except for
template functions which have a dedicated name in Python. To get the
list of the exact methods names of an object, you can type
help(name_of_object) in the interpreter.


To run the programs presented in the book: 

1) Double-click the icon named "run.command" in the ProBtLinuxXX
directory. A request will then appear, asking to either execute or
show the content of this command. Please choose "Run in a terminal".
Alternatively, in you prefer to use a terminal, go to the ProBtLinuxXX
directory and type
  sh run.command

2) The program will then check if everything it needs is installed,
and if not it will ask for your administrator password to perform the
required installations.

3) You are now in a ProBT-enabled interactive Python shell. You can
now type the following command to run the examples:
  execfile('Examples/execall.py')

Happy coding!
