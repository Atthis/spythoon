def secondsToMinutesSeconds(s):
   min = s // 60
   sec = s % 60
   return "%02d:%02d" % (min, sec)

def test_timeStampToTimer():
   time1 = 300
   assert secondsToMinutesSeconds(time1) == "05:00"
   
   time2 = 4225
   assert secondsToMinutesSeconds(time2) == "70:25"

# def calcRelScore():
   