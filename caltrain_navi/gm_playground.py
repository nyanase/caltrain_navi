from caltrain_navi.cn_client import CN_Client, get_coords_from_str
from caltrain_navi.constants import google_maps_key
cn_client = CN_Client(gm_key=google_maps_key,
                      trains_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/trains.json",
                      stations_path="/Users/naoyanase/Desktop/caltrain_navi/caltrain_scraper/scraped_data/stations.json"
            )
