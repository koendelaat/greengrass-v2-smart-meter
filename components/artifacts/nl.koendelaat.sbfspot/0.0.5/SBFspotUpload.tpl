################################################################################
#  SBFspotUpload.cfg - Configuration file for SBFspotUploadService/Daemon
#  (c)2012-2018, SBF (https://github.com/SBFspot/SBFspot)
#
#  DISCLAIMER:
#  A user of SBFspotUploadService/Daemon software acknowledges that he or she is
#  receiving this software on an "as is" basis and the user is not relying on
#  the accuracy or functionality of the software for any purpose. The user
#  further acknowledges that any use of this software will be at his own risk
#  and the copyright owner accepts no responsibility whatsoever arising from
#  the use or application of the software.
#
################################################################################


################################
### Log Settings             ###
################################
# Windows: C:\Users\Public\SMAdata\Logs
# Linux  : /var/log/sbfspot.3
#LogDir=C:\Users\Public\SMAdata\Logs
LogDir=/var/smadata/logs

#LogLevel=debug|info|warning|error (default info)
LogLevel=info

################################
### PVoutput Upload Settings ###
################################
#PVoutput_SID (PVoutput_System_ID)
#Map inverters to PVoutput System ID's
#PVoutput_SID=SerialNmbrInverter_1:PVoutput_System_ID_1,SerialNmbrInverter_2:PVoutput_System_ID_2
#e.g. PVoutput_SID=200212345:4321
PVoutput_SID=$sid

#PVoutput_Key
#Sets PVoutput API Key
PVoutput_Key=$api_key

################################
### SQL DB Settings          ###
################################
SQL_Database=/var/smadata/SBFspot.db
