from datetime import datetime, timedelta

dt = datetime.now() + timedelta(days=60)
print(int(dt.strftime("%S")))
