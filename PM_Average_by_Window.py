import pandas as pd
import csv

class Averager:
  # list of stations (not all supply PM2.5)
  station_list = ['Havre', 'Dillon', 'Cut Bank', 'Flathead Valley', 'Libby',
                  'Thompson Falls', 'Great Falls', 'Helena', 'Broadus', 'NCore',
                  'Sleeping Giant', 'Hamilton', 'Malta', 'Sidney', 'Bozeman',
                  'Billings', 'Billings Lockwood', 'Missoula', 'Seeley Lake',
                  'West Yellowstone', 'Lewistown', 'Frenchtown', 'Miles City', 'Butte']

  # unique dates
  unique_dates = {}

  def __init__(self, csv):
    self.csv = csv

  def createDF(self):
    lat, long, sites, rawvalues, dates, hours = [], [], [], [], [], []

    # read through CSV file and turn useful columns into lists
    with open(self.csv, 'r', newline='') as csvfile:
      reader = csv.DictReader(csvfile)

      for row in reader:

        # ignore null values and negatives
        if row['rawvalue'] == '' or float(row['rawvalue']) < 0:
          continue

        # seperate date and time
        date = row['datetime'].replace('/', '-').split(' ')[0]

        # add all important values to lists
        dates.append(date)
        hours.append(int(row['hour']))
        rawvalues.append(float(row['rawvalue']))
        lat.append(float(row['latitude']))
        long.append(float(row['longitude'])),
        sites.append(row['sitename'])

        # create distinct list of dates (dictionary keys)
        self.unique_dates[date] = row

    # convert these lists into a dataframe
    data = {
      'date': dates,
      'hour': hours,
      'sitename': sites,
      'latitude': lat,
      'longitude': long,
      'rawvalue': rawvalues}

    return pd.DataFrame(data)

  def createCSV(self, df):
    # empty lists to hold important values
    lat, long, sites, rawvalues, datetimes = [], [], [], [], []

    # filter by distinct dates and each station
    for date in self.unique_dates:
      for place in self.station_list:
        sample = df[(df['date'] == date) & (df['sitename'] == place)]

        # if there are no values for that station, go to next site
        if len(sample.index) == 0:
          continue

        # initialize pm sums and counts
        pm_sum_one = 0.0  
        pm_sum_two = 0.0
        count_one = 0
        count_two = 0

        for row in sample.iterrows():
          # raw value in this row
          pm = float(row['rawvalue'])
          hour = int(row['hour'])

          # ignore negative (invalid) values
          if pm < 0:
            continue
          
          # hour in MST
          if hour in [11, 12]:
            pm_sum_one += pm
            count_one += 1
          elif hour in [13, 14]:
            pm_sum_two += pm
            count_two += 1
        
        # calculate averages (can be null if only valid reading is from other time window)
        if count_one == 0:
          pm_ave_one = None
        else:
          pm_ave_one = pm_sum_one / count_one
        if count_two == 0:
          pm_ave_two = None
        else:
          pm_ave_two = pm_sum_two / count_two

        # add non null values to final list
        if pm_ave_one != None:
          rawvalues.append(pm_ave_one)
          lat.append(sample['latitude'].iloc[0])
          long.append(sample['longitude'].iloc[0])
          sites.append(sample['sitename'].iloc[0])
          datetimes.append(sample['date'].iloc[0] + 'T18:00')
                
        if pm_ave_two != None:
          rawvalues.append(pm_ave_two)
          lat.append(sample['latitude'].iloc[0])
          long.append(sample['longitude'].iloc[0])
          sites.append(sample['sitename'].iloc[0])
          datetimes.append(sample['date'].iloc[0] + 'T20:00')

    output_data = pd.DataFrame({
      'datetime': datetimes,
      'sitename': sites,
      'latitude': lat,
      'longitude': long,
      'rawvalue': rawvalues
    })

    # export to csv
    return output_data.to_csv('PM_TAW_AY_2b.csv', sep=',', index=True)

def main():
    # might be broken up due to oversized file
    filename = '2018-2022.csv'
    table = Averager(filename)
    df = table.createDF()
    table.createCSV(df)

if __name__ == '__main__':
    main()
