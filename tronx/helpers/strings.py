from tronx import (
	USER_NAME, 
	__python_version__, 
	__pyro_version__, 
	db_status, 
	uptime, 
	USER_BIO,
)



stat_string = f"""
**Dex:** Stats

**Location:** /home/stats

**Name:** {USER_NAME}
**Lara version:** {lara_version}
**Python version:** {__python_version__}
**Pyrogram version:** {__pyro_version__}
**Database:** {db_status}
**Uptime:** {uptime()}
**User Bio:** {USER_BIO}
"""
