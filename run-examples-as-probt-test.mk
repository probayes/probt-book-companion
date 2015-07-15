# Build-system for running the Python examples from the Bayesian Programming book
# as tests for the ProBT Python bindings.
# Copyright Probayes SAS

.PHONY: all
all: book-examples

WGET = "wget"
ZIP = "7z"
PL_DIR := $(PWD)/ProBT/
PROBT_DOWNLOAD_PAGE := http://cauchy-web/telechargements/ProBT-2.3.0/
PYTHON := python
IPYTHON := ipython

UNAME := $(shell uname -s)
ifeq ($(UNAME),Darwin)
    PROBT_PKG := probt-spl-2.3.0-mac64-dynamic-release
    PROBT_PKG_ARC := $(PROBT_PKG).tar.bz2
    DLL_PATH_VAR := DYLD_LIBRARY_PATH
    DLL_PATH = $(PL_DIR)lib:$(DYLD_LIBRARY_PATH)
    PYTHONPATH := $(PL_DIR)lib:$(PYTHONPATH)
else
    PATH := /usr/local/bin:${PATH}
    ifeq ($(shell dpkg --print-architecture),amd64)
      PROBT_PKG := probt-spl-2.3.0-linux64-dynamic-release
    else
      PROBT_PKG := probt-spl-2.3.0-linux-dynamic-release
    endif
    PROBT_PKG_ARC := $(PROBT_PKG).tar.bz2
    DLL_PATH_VAR := LD_LIBRARY_PATH
    DLL_PATH = $(PL_DIR)lib:/usr/local/lib:$(LD_LIBRARY_PATH)
    PYTHONPATH := $(PL_DIR)lib:/usr/local/lib/python2.7/dist-packages/:$(PYTHONPATH)
endif

$(PROBT_PKG_ARC):
	$(WGET) --no-verbose "$(PROBT_DOWNLOAD_PAGE)$(PROBT_PKG_ARC)"

ProBT: $(PROBT_PKG_ARC)
ifeq ($(MSVC),1)
	$(ZIP) x -r $(PROBT_PKG_ARC) lib
else
	tar xf $(PROBT_PKG_ARC) $(PROBT_PKG)/lib
endif
	mv $(PROBT_PKG) ProBT

PROBT_SPL_TARGET := ProBT

distclean::
	rm -rf ProBT $(PROBT_PKG_ARC)
	rm -f Examples/execall.py

.PHONY: book-examples
book-examples: ProBT
	cp -f pyplpath.py Examples/
	cp -f execall.py Examples/
	cd Examples && PYTHONPATH="$(PYTHONPATH)"  $(DLL_PATH_VAR)="$(DLL_PATH)" \
	    $(PYTHON) execall.py

.PHONY: ipython
ipython: clean
	PYTHONPATH="$(PYTHONPATH)"  $(DLL_PATH_VAR)="$(DLL_PATH)" \
	    $(IPYTHON) --pylab --pdb

# Local Variables:
# mode: makefile
# End:
