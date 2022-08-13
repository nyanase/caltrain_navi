from caltrain_navi.cn_client import CN_Client
cn_client = CN_Client(gm_key="AIzaSyDzI35ioLvXsqs5ruAUjuxu12aRUwo1r9c",
                      trains_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json",
                      stations_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json"
            )

duration = cn_client.get_durations("319 Eleanor Ave, Los Altos, CA 94022",
  "600 W Evelyn Ave, Mountain View, CA 94041", 
  mode="walking"
)
print(duration)

# closests = cn_client.get_closest_times_stations("319 Eleanor Ave, Los Altos, CA 94022")