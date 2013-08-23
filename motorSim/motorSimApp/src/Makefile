TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = mtrSim
# mtrSim.dbd will be created and installed
DBD += mtrSim.dbd

# mtrSim.dbd will be made up from these files:
mtrSim_DBD += base.dbd

# Include dbd files from all support applications:
mtrSim_DBD += asyn.dbd
mtrSim_DBD += motorSupport.dbd
mtrSim_DBD += devSoftMotor.dbd
mtrSim_DBD += motorRecord.dbd
mtrSim_DBD += motorSimSupport.dbd
mtrSim_DBD += asSupport.dbd

# Add all the support libraries needed by this IOC
mtrSim_LIBS += softMotor motorSimSupport motor asyn autosave

# mtrSim_registerRecordDeviceDriver.cpp derives from mtrSim.dbd
mtrSim_SRCS += mtrSim_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
mtrSim_SRCS_DEFAULT += mtrSimMain.cpp
mtrSim_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#mtrSim_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
mtrSim_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

