################################################################################
#                     ____  ____  _____                _
#                    / ___|| __ )|  ___|__ _ __   ___ | |_
#                    \___ \|  _ \| |_ / __| '_ \ / _ \| __|
#                     ___) | |_) |  _|\__ \ |_) | (_) | |_
#                    |____/|____/|_|  |___/ .__/ \___/ \__|
#                                         |_|
#
#  SBFspot.cfg - Configuration file for SBFspot.exe
#  SBFspot - Yet another tool to read power production of SMA® solar inverters
#  (c)2012-2018, SBF
#
#  DISCLAIMER:
#  A user of SBFspot software acknowledges that he or she is receiving this
#  software on an "as is" basis and the user is not relying on the accuracy
#  or functionality of the software for any purpose. The user further
#  acknowledges that any use of this software will be at his own risk
#  and the copyright owner accepts no responsibility whatsoever arising from
#  the use or application of the software.
#
#  	SMA and Speedwire are registered trademarks of SMA Solar Technology AG
################################################################################

# SMA Inverter's Bluetooth address
# Windows: smaspot -scan
# Linux  : hcitool scan
# IMPORTANT FOR SPEEDWIRE USERS: COMMENT OUT BTADDRESS (PUT # IN FRONT)
#BTAddress=00:00:00:00:00:00

# SMA Inverter's Speedwire IP address
# If IP_Address is not set or is 0.0.0.0 SBFspot will try to detect the speedwire inverter by broadcast
# If IP_Address is set to a valid IP, SBFspot will try to connect directly to that IP without broadcast detection
# Multiple IP addresses can be provided (comma separated)
IP_Address=$ip_address

# User password (default 0000)
Password=$password

# MIS_Enabled (Multi Inverter Support: Default=0 Disabled)
# +------------+-------+-------------+
# | #Inverters | NetID | MIS_Enabled |
# +------------+-------+-------------+
# |      1     |   1   | Don't Care  |
# +------------+-------+-------------+
# |      1     |   >1  |      0      |
# +------------+-------+-------------+
# |      >1    |   >1  |      1      |
# +------------+-------+-------------+
MIS_Enabled=0

# Plantname
Plantname=$thing_name

# OutputPath (Place to store CSV files)
#
# Windows: C:\Users\Public\SMAdata\%Y
# Linux  : /home/pi/smadata/%Y
# %Y %m and %d will be expanded to Year Month and Day
OutputPath=/var/smadata/%Y

# OutputPathEvents (Place to store CSV files for events)
# If omitted, OutputPath is used
OutputPathEvents=/var/smadata/%Y/Events

# Position of pv-plant http://itouchmap.com/latlong.html
# Example for Ukkel, Belgium
Latitude=51.606
Longitude=5.138

# Calculate Missing SpotValues
# If set to 1, values not provided by inverter will be calculated
# eg: Pdc1 = Idc1 * Udc1
CalculateMissingSpotValues=1

# DateTimeFormat (default %d/%m/%Y %H:%M:%S)
# For details see strftime() function
# http://www.cplusplus.com/reference/clibrary/ctime/strftime/
DateTimeFormat=%d/%m/%Y %H:%M:%S

# DateFormat (default %d/%m/%Y)
DateFormat=%d/%m/%Y

# DecimalPoint (comma/point default comma)
DecimalPoint=comma

# TimeFormat (default %H:%M:%S)
TimeFormat=%H:%M:%S

# SynchTime (0-30 - 0=disabled, 1=once a day (default), 7=once a week, 30=once a month)
# If set to non-zero value, the plant time is synchronised with local host time
# Some inverters don't have a real-time clock
SynchTime=1

# SynchTimeLow (1-120 - default 1)
# SynchTimeHigh (1200-3600 - default 3600)
# Plant time is adjusted to local host time when SynchTime=1 and
# time difference is between SynchTimeLow and SynchTimeHigh limits
SynchTimeLow=1
SynchTimeHigh=3600

# SunRSOffset
# Offset to start before sunrise and end after sunset (0-3600 - default 900 seconds)
SunRSOffset=900

# Locale
# Translate Entries in CSV files
# Supported locales: de-DE;en-US;fr-FR;nl-NL;es-ES;it-IT
# Default en-US
Locale=en-US

# Timezone
# Select the right timezone in date_time_zonespec.csv
# e.g. Timezone=Europe/Brussels
Timezone=Europe/Amsterdam

# BTConnectRetries
# Number of Bluetooth Connection attempts (1-15; Default=10)
BTConnectRetries=10

###########################
### CSV Export Settings ###
###########################
# With CSV_* settings you can define the CSV file format

# CSV_Export (default 1 = Enabled)
# Enables or disables the CSV Export functionality
#CSV_Export=1

# CSV_ExtendedHeader (default 1 = On)
# Enables or disables the SMA extended header info (8 lines)
# isep=;
# Version CSV1|Tool SBFspot|Linebreaks CR/LF|Delimiter semicolon|Decimalpoint comma|Precision 3
# etc...
# This is usefull for manual data upload to pvoutput.org
#CSV_ExtendedHeader=1

# CSV_Header (default 1 = On)
# Enables or disables the CSV data header info (1 line)
# dd/MM/yyyy HH:mm:ss;kWh;kW
# This is usefull for manual data upload to pvoutput.org
# If CSV_ExtendedHeader is enabled, CSV_Header is also enabled
#CSV_Header=1

# CSV_SaveZeroPower (default 1 = On)
# When enabled, daily csv files contain all data from 00:00 to 23:55
# This is usefull for manual data upload to pvoutput.org
#CSV_SaveZeroPower=1

# CSV_Delimiter (comma/semicolon default semicolon)
#CSV_Delimiter=semicolon

# CSV_Spot_TimeSource (Inverter|Computer default Inverter)
#CSV_Spot_TimeSource=Inverter

# CSV_Spot_WebboxHeader (Default 0 = Off)
# When enabled, use Webbox style header (DcMs.Watt[A];DcMs.Watt[B]...)
#CSV_Spot_WebboxHeader=0

###########################
###   SQL DB Settings   ###
###########################

# SQLite
SQL_Database=/var/smadata/SBFspot.db
