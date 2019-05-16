import os 
station_ids = ["2214","2215","2189","2190","2187","2183","2191","2192","2185","2184","2218","2149","2217","2186","2219"]
website_template = "https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/daily/start_of_period/{}:CA:SCAN%7Cid=%22%22%7Cname/-2525,0/stationId,TMAX::value,TMIN::value,PRCP::value,RHUM::value:hourly%20MEAN,WSPDX::value:hourly%20MAX,WSPDV::value:hourly%20MEAN,SRADV::value:hourly%20MEAN,LRADT::value,PVPV::value:hourly%20MEAN,SVPV::value:hourly%20MEAN,SMS:-2:value:hourly%20MEAN,SMS:-4:value:hourly%20MEAN,SMS:-8:value:hourly%20MEAN,SMS:-20:value:hourly%20MEAN,SMS:-40:value:hourly%20MEAN,STO:-2:value:hourly%20MEAN,STO:-4:value:hourly%20MEAN,STO:-8:value:hourly%20MEAN,STO:-20:value:hourly%20MEAN,STO:-40:value:hourly%20MEAN"
system_call = "curl {} -o {}"

for id in station_ids:
    site = website_template.format(id)
    file_name = id + '.csv'
    print(id)
    os.system(system_call.format(site, file_name))
