import arrow

def datetimeformat():
  dt = arrow.get(date_str)
  return dt.humanize()