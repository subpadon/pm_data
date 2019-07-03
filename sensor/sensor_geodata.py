import requests
import pandas as pd

url = 'http://air4thai.pcd.go.th/services/getNewAQI_JSON.php'
data = requests.request("GET", url).json()

data = data['stations']

data =pd.DataFrame(data)

# reverse column orders


columns = data.columns.tolist()
columns = columns[::-1]

data = data[columns]


outfile = 'sensor_geodata.csv';
data.to_csv(outfile, index=False)