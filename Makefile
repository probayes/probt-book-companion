# Build-system for packaging the ProBT Python bindings accompanying the
# Bayesian Programming book.
# Copyright Probayes SAS
#--------------------------------------------------------------------------------------------------

#TODO: the packages generated by this makefile are not functional,
#      because they use the official ProBT packages, whereas we need
#      special ProBT builds which are not available under Jenkins yet.

#TODO: distribute the C++ reference documentation ?

WGET = "wget"
ZIP = "7z"
ZIP_OPTS = a -r
UNZIP_OPTS = x -r
INSTALL ?= /usr/bin/install
PREFIX ?= artefacts
PROBT_DOWNLOAD_PAGE := http://cauchy-web/telechargements/ProBT-2.3.0/

#--------------------------------------------------------------------------------------------------
LIN32_DIR           := ProBtLinux32
LIN32_DIR_ARC       := $(LIN32_DIR).tar.bz2
LIN32_DIR_ARC_TYPE  := TBZ2
LIN32_PROBT_PKG     := probt-spl-2.3.0-linux-dynamic-release
LIN32_PROBT_PKG_ARC := $(LIN32_PROBT_PKG).tar.bz2
LIN32_TARGET_OS     := UNIX
LIN32_DLIB_SUFFIX   := so
LIN32_README        := README-Linux32.txt

LIN64_DIR           := ProBtLinux64
LIN64_DIR_ARC       := $(LIN64_DIR).tar.bz2
LIN64_DIR_ARC_TYPE  := TBZ2
LIN64_PROBT_PKG     := probt-spl-2.3.0-linux64-dynamic-release
LIN64_PROBT_PKG_ARC := $(LIN64_PROBT_PKG).tar.bz2
LIN64_TARGET_OS     := UNIX
LIN64_DLIB_SUFFIX   := so
LIN64_README        := README-Linux64.txt

MAC64_DIR           := ProBtMac64
MAC64_DIR_ARC       := $(MAC64_DIR).zip
MAC64_DIR_ARC_TYPE  := ZIP
MAC64_PROBT_PKG     := probt-spl-2.3.0-mac64-dynamic-release-system_python26
MAC64_PROBT_PKG_ARC := $(MAC64_PROBT_PKG).tar.bz2
MAC64_PROBT_DOWNLOAD_PAGE := http://jenkins/view/PrBT-P/job/ProBT-2.3.x-packages-mac64-system_python26/lastSuccessfulBuild/artifact/system/packages/
MAC64_TARGET_OS     := UNIX
MAC64_DLIB_SUFFIX   := dylib
MAC64_README        := README-Mac64.rtf

WIN32_DIR           := ProBtWindows
WIN32_DIR_ARC       := $(WIN32_DIR).zip
WIN32_DIR_ARC_TYPE  := ZIP
WIN32_PROBT_PKG     := probt-spl-2.3.0-vc10-dynamic-release-python27
WIN32_PROBT_PKG_ARC := $(WIN32_PROBT_PKG).zip
WIN32_PROBT_DOWNLOAD_PAGE := http://jenkins/view/PrBT-P/job/ProBT-2.3.x-packages-vc-dynamic-python27/lastSuccessfulBuild/artifact/system/packages/
WIN32_TARGET_OS     := WINDOWS
WIN32_DLIB_SUFFIX   := dll
WIN32_BOOST_VERSION := 1_46_1
WIN32_VC_VERSION    := vc100
WIN32_README        := README-Windows.rtf

ALL_MODULES = LIN32 LIN64 MAC64 WIN32

#--------------------------------------------------------------------------------------------------
define rules_template

$(1)_PROBT_DOWNLOAD_PAGE ?= $(PROBT_DOWNLOAD_PAGE)

$$($(1)_PROBT_PKG):
	$(WGET) --no-verbose "$$($(1)_PROBT_DOWNLOAD_PAGE)$$($(1)_PROBT_PKG_ARC)"
ifeq ($$($(1)_TARGET_OS),WINDOWS)
	$(ZIP) $(UNZIP_OPTS) "$$($(1)_PROBT_PKG_ARC)" lib doc
else
	tar xjf "$$($(1)_PROBT_PKG_ARC)" "$$($(1)_PROBT_PKG)/lib" "$$($(1)_PROBT_PKG)/doc"
endif
	rm "$$($(1)_PROBT_PKG_ARC)"

.PHONY:
clean-$(1)::
	rm -rf "$$($(1)_PROBT_PKG)"


$(PREFIX)/$$($(1)_DIR):
	$(INSTALL) -d "$(PREFIX)/$$($(1)_DIR)"
	tar cf - --exclude CVS --exclude .cvsignore --exclude .DS_Store Examples \
		| tar xf - -C "$(PREFIX)/$$($(1)_DIR)"
	$(INSTALL) $$($(1)_README) "$(PREFIX)/$$($(1)_DIR)"
	$(INSTALL) execall.py "$(PREFIX)/$$($(1)_DIR)"/Examples
ifeq ($$($(1)_TARGET_OS),WINDOWS)
	$(INSTALL) run.bat "$(PREFIX)/$$($(1)_DIR)"
else
	$(INSTALL) run.command "$(PREFIX)/$$($(1)_DIR)"
endif


$(PREFIX)/$$($(1)_DIR)/pypl: $(PREFIX)/$$($(1)_DIR) $$($(1)_PROBT_PKG)
	$(INSTALL) -d "$(PREFIX)/$$($(1)_DIR)/pypl"
ifeq ($$($(1)_TARGET_OS),WINDOWS)
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/spl-$$($(1)_VC_VERSION).dll "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/boost_*-$$($(1)_VC_VERSION)-mt-$$($(1)_BOOST_VERSION).dll "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/libtcc.dll "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/_pypl.pyd "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/pypl.py "$(PREFIX)/$$($(1)_DIR)/pypl"
else
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/libspl.$$($(1)_DLIB_SUFFIX) "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/libboost*$$($(1)_DLIB_SUFFIX)* "$(PREFIX)/$$($(1)_DIR)/pypl"
	if [ -f "$$($(1)_PROBT_PKG)"/lib/libtcc.$$($(1)_DLIB_SUFFIX) ]; then \
		$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/libtcc.$$($(1)_DLIB_SUFFIX) \
		           "$(PREFIX)/$$($(1)_DIR)/pypl"; fi
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/_pypl.so "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/pypl.py "$(PREFIX)/$$($(1)_DIR)/pypl"
endif
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/PROBT_LICENSE.txt "$(PREFIX)/$$($(1)_DIR)/pypl"
	$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/BOOST_LICENSE.txt "$(PREFIX)/$$($(1)_DIR)/pypl"
	if [ -f "$$($(1)_PROBT_PKG)"/lib/TCC_LICENSE.txt ]; then \
		$(INSTALL) "$$($(1)_PROBT_PKG)"/lib/TCC_LICENSE.txt "$(PREFIX)/$$($(1)_DIR)/pypl"; fi
	$(INSTALL) pyplpath.py "$(PREFIX)/$$($(1)_DIR)/pypl"


$(PREFIX)/$$($(1)_DIR)/Documentation: $(PREFIX)/$$($(1)_DIR) $$($(1)_PROBT_PKG)
	$(INSTALL) -d "$(PREFIX)/$$($(1)_DIR)/Documentation"
	tar cf - --exclude CVS --exclude .cvsignore --exclude .DS_Store \
		-C "$$($(1)_PROBT_PKG)"/doc/html . \
		| tar xf - -C "$(PREFIX)/$$($(1)_DIR)/Documentation"


$(PREFIX)/$$($(1)_DIR_ARC): $(PREFIX)/$$($(1)_DIR) $(PREFIX)/$$($(1)_DIR)/pypl $(PREFIX)/$$($(1)_DIR)/Documentation
ifeq ($$($(1)_DIR_ARC_TYPE),ZIP)
	cd "$(PREFIX)" ; $(ZIP) $(ZIP_OPTS) "$$($(1)_DIR_ARC)" "$$($(1)_DIR)"
else
	tar cjf "$(PREFIX)/$$($(1)_DIR_ARC)" -C "$(PREFIX)" "$$($(1)_DIR)"
endif


.PHONY: install-$(1) dist-$(1) clean-$(1) distclean-$(1)

install-$(1):: $(PREFIX)/$$($(1)_DIR) $(PREFIX)/$$($(1)_DIR)/pypl

clean-$(1)::
	rm -rf "$(PREFIX)/$$($(1)_DIR)"

dist-$(1):: $(PREFIX)/$$($(1)_DIR_ARC)

distclean-$(1):: clean-$(1)
	rm -f "$(PREFIX)/$$($(1)_DIR_ARC)"

install:: install-$(1) 
dist:: dist-$(1) 
clean:: clean-$(1) 
distclean:: distclean-$(1) 


endef #rules_template
#--------------------------------------------------------------------------------------------------

$(foreach module, $(ALL_MODULES), $(eval $(call rules_template,$(module))))
ALL_TARGETS := $(foreach module, $(ALL_MODULES), $(PREFIX)/$($(module)_DIR_ARC))
.PHONY:
all:	$(ALL_TARGETS)
.DEFAULT_GOAL := all

.PHONY: install dist clean distclean
clean::
	find . -name "*~" -exec rm {} \;
	find . -name ".DS_Store" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;

$(PREFIX):
	$(INSTALL) -d "$(PREFIX)"
