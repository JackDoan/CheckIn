########################################################################
#
# Arduino command line tools Makefile
# System part (i.e. project independent)
#
# Copyright (C) 2010,2011,2012 Martin Oldfield <m@mjo.tc>, based on
# work that is copyright Nicholas Zambetti, David A. Mellis & Hernando
# Barragan.
# 
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.
#
########################################################################

# Default TARGET to cwd (ex Daniele Vergini)
ifndef TARGET
TARGET  = $(notdir $(CURDIR))
endif

# CheckIn variable definitions
# Jack Doan 4/13/2014

TARGET     = CheckIn
ARDUINO_LIBS = LiquidCrystal
AVR_TOOLS_PATH	= /usr/bin
ARDUINO_LIB_PATH  = ./lib
MCU   = atmega328p
F_CPU = 16000000L
OBJDIR  	  = build-cli

########################################################################
# Local sources

LOCAL_C_SRCS	= $(wildcard *.c)
LOCAL_CPP_SRCS  = $(wildcard *.cpp)
LOCAL_CC_SRCS   = $(wildcard *.cc)
LOCAL_PDE_SRCS  = $(wildcard *.pde)
LOCAL_INO_SRCS  = $(wildcard *.ino)
LOCAL_AS_SRCS   = $(wildcard *.S)
LOCAL_OBJ_FILES = $(LOCAL_C_SRCS:.c=.o)   $(LOCAL_CPP_SRCS:.cpp=.o) \
		$(LOCAL_CC_SRCS:.cc=.o)   $(LOCAL_PDE_SRCS:.pde=.o) \
		$(LOCAL_INO_SRCS:.ino=.o) $(LOCAL_AS_SRCS:.S=.o)
LOCAL_OBJS	  = $(patsubst %,$(OBJDIR)/%,$(LOCAL_OBJ_FILES))

# Dependency files
DEPS			= $(LOCAL_OBJS:.o=.d)

CORE_PATH = ./lib/core
CORE_C_SRCS	 = $(wildcard $(CORE_PATH)/*.c)
CORE_CPP_SRCS   = $(wildcard $(CORE_PATH)/*.cpp)
CORE_OBJ_FILES  = $(CORE_C_SRCS:.c=.o) $(CORE_CPP_SRCS:.cpp=.o)
CORE_OBJS	   = $(patsubst $(CORE_PATH)/%,  \
			$(OBJDIR)/%,$(CORE_OBJ_FILES))


########################################################################
# Rules for making stuff

# The name of the main targets
TARGET_HEX = $(OBJDIR)/$(TARGET).hex
TARGET_ELF = $(OBJDIR)/$(TARGET).elf
TARGETS	= $(OBJDIR)/$(TARGET).*
CORE_LIB   = $(OBJDIR)/libcore.a

# A list of dependencies
DEP_FILE   = $(OBJDIR)/depends.mk

# Names of executables
CC	  = $(AVR_TOOLS_PATH)/avr-gcc
CXX	 = $(AVR_TOOLS_PATH)/avr-g++
OBJCOPY = $(AVR_TOOLS_PATH)/avr-objcopy
OBJDUMP = $(AVR_TOOLS_PATH)/avr-objdump
AR	  = $(AVR_TOOLS_PATH)/avr-ar
SIZE	= $(AVR_TOOLS_PATH)/avr-size
NM	  = $(AVR_TOOLS_PATH)/avr-nm
REMOVE  = rm -f
MV	  = mv -f
CAT	 = cat
ECHO	= echo

# General arguments
SYS_LIBS	  = $(patsubst %,$(ARDUINO_LIB_PATH)/%,$(ARDUINO_LIBS))
SYS_INCLUDES  = $(patsubst %,-I%,$(SYS_LIBS))
LIB_C_SRCS	= $(wildcard $(patsubst %,%/*.c,$(SYS_LIBS)))
LIB_CPP_SRCS  = $(wildcard $(patsubst %,%/*.cpp,$(SYS_LIBS)))
LIB_OBJS	  = $(patsubst $(ARDUINO_LIB_PATH)/%.c,$(OBJDIR)/libs/%.o,$(LIB_C_SRCS)) \
		$(patsubst $(ARDUINO_LIB_PATH)/%.cpp,$(OBJDIR)/libs/%.o,$(LIB_CPP_SRCS))

CPPFLAGS	  = -mmcu=$(MCU) -DF_CPU=$(F_CPU) -I. -I$(CORE_PATH) \
			$(SYS_INCLUDES) -g -Os -w -Wall -ffunction-sections -fdata-sections
CFLAGS		= -std=gnu99
CXXFLAGS	  = -fno-exceptions
ASFLAGS	   = -mmcu=$(MCU) -I. -x assembler-with-cpp
LDFLAGS	   = -mmcu=$(MCU) -Wl,--gc-sections -Os

# Implicit rules for building everything (needed to get everything in
# the right directory)
#
# Rather than mess around with VPATH there are quasi-duplicate rules
# here for building e.g. a system C++ file and a local C++
# file. Besides making things simpler now, this would also make it
# easy to change the build options in future

# library sources
$(OBJDIR)/libs/%.o: $(ARDUINO_LIB_PATH)/%.c
	mkdir -p $(dir $@)
	$(CC) -c $(CPPFLAGS) $(CFLAGS) $< -o $@

$(OBJDIR)/libs/%.o: $(ARDUINO_LIB_PATH)/%.cpp
	mkdir -p $(dir $@)
	$(CC) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

# normal local sources
# .o rules are for objects, .d for dependency tracking
# there seems to be an awful lot of duplication here!!!
$(OBJDIR)/%.o: %.c
	$(CC) -c $(CPPFLAGS) $(CFLAGS) $< -o $@

$(OBJDIR)/%.o: %.cc
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

$(OBJDIR)/%.o: %.cpp
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

$(OBJDIR)/%.o: %.S
	$(CC) -c $(CPPFLAGS) $(ASFLAGS) $< -o $@

$(OBJDIR)/%.o: %.s
	$(CC) -c $(CPPFLAGS) $(ASFLAGS) $< -o $@

$(OBJDIR)/%.d: %.c
	$(CC) -MM $(CPPFLAGS) $(CFLAGS) $< -MF $@ -MT $(@:.d=.o)

$(OBJDIR)/%.d: %.cc
	$(CXX) -MM $(CPPFLAGS) $(CXXFLAGS) $< -MF $@ -MT $(@:.d=.o)

$(OBJDIR)/%.d: %.cpp
	$(CXX) -MM $(CPPFLAGS) $(CXXFLAGS) $< -MF $@ -MT $(@:.d=.o)

$(OBJDIR)/%.d: %.S
	$(CC) -MM $(CPPFLAGS) $(ASFLAGS) $< -MF $@ -MT $(@:.d=.o)

$(OBJDIR)/%.d: %.s
	$(CC) -MM $(CPPFLAGS) $(ASFLAGS) $< -MF $@ -MT $(@:.d=.o)

# the pde -> cpp -> o file
$(OBJDIR)/%.cpp: %.pde
	$(ECHO) '#include "WProgram.h"' > $@
	$(CAT)  $< >> $@

# the ino -> cpp -> o file
$(OBJDIR)/%.cpp: %.ino
	$(ECHO) '#include <Arduino.h>' > $@
	$(CAT)  $< >> $@

$(OBJDIR)/%.o: $(OBJDIR)/%.cpp
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

$(OBJDIR)/%.d: $(OBJDIR)/%.cpp
	$(CXX) -MM $(CPPFLAGS) $(CXXFLAGS) $< -MF $@ -MT $(@:.d=.o)

# core files
$(OBJDIR)/%.o: $(CORE_PATH)/%.c
	$(CC) -c $(CPPFLAGS) $(CFLAGS) $< -o $@

$(OBJDIR)/%.o: $(CORE_PATH)/%.cpp
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

# various object conversions
$(OBJDIR)/%.hex: $(OBJDIR)/%.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

$(OBJDIR)/%.eep: $(OBJDIR)/%.elf
	-$(OBJCOPY) -j .eeprom --set-section-flags=.eeprom="alloc,load" \
		--change-section-lma .eeprom=0 -O ihex $< $@

$(OBJDIR)/%.lss: $(OBJDIR)/%.elf
	$(OBJDUMP) -h -S $< > $@

$(OBJDIR)/%.sym: $(OBJDIR)/%.elf
	$(NM) -n $< > $@

########################################################################
#
# Avrdude
#
ifndef AVRDUDE
AVRDUDE		  = sudo ./tools/avrdude
endif

AVRDUDE_COM_OPTS = -q -V -p $(MCU)
ifdef AVRDUDE_CONF
AVRDUDE_COM_OPTS += -C ./tools/avrdude.conf
endif

ifndef ISP_PROG
ISP_PROG	   = -c stk500v2
endif

AVRDUDE_ISP_OPTS = -P $(ISP_PORT) $(ISP_PROG)

ifndef JTAG_PROG
JTAG_PROG	   = -c jtag3isp
endif

AVRDUDE_JTAG_OPTS = -B 0.5 $(JTAG_PROG) 

########################################################################
#
# Explicit targets start here
#

all: 		$(OBJDIR) $(TARGET_HEX)

$(OBJDIR):
		mkdir $(OBJDIR)

$(TARGET_ELF): 	$(LOCAL_OBJS) $(CORE_LIB) $(OTHER_OBJS)
		$(CC) $(LDFLAGS) -o $@ $(LOCAL_OBJS) $(CORE_LIB) $(OTHER_OBJS) -lc -lm

$(CORE_LIB):	$(CORE_OBJS) $(LIB_OBJS)
		$(AR) rcs $@ $(CORE_OBJS) $(LIB_OBJS)

$(DEP_FILE):	$(OBJDIR) $(DEPS)
		cat $(DEPS) > $(DEP_FILE)

upload:		jtag

ispload:	$(TARGET_HEX)
		$(AVRDUDE) $(AVRDUDE_COM_OPTS) $(AVRDUDE_ISP_OPTS) -D \
			-U flash:w:$(TARGET_HEX):i

jtag:	$(TARGET_HEX)
		$(AVRDUDE) $(AVRDUDE_COM_OPTS) $(AVRDUDE_JTAG_OPTS) -D \
			-U flash:w:$(TARGET_HEX):i

clean:
		$(REMOVE) $(LOCAL_OBJS) $(CORE_OBJS) $(LIB_OBJS) $(CORE_LIB) $(TARGETS) $(DEP_FILE) $(DEPS)

depends:	$(DEPS)
		cat $(DEPS) > $(DEP_FILE)

size:		$(OBJDIR) $(TARGET_HEX)
		$(SIZE) $(TARGET_HEX)

.PHONY:	all clean depends upload raw_upload reset size show_boards

include $(DEP_FILE)
