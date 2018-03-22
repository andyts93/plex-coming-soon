from plexcomingsoon import PlexComingSoon, logger
import schedule
import time

instance = PlexComingSoon()
logger.info("Starting script, scheduled every %d minutes" % (instance.interval))
instance.run()
# schedule.every(instance.interval).minutes.do(instance.run)
# while 1:
# 	schedule.run_pending()
# 	time.sleep(1)