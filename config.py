from datetime import datetime

# Filepaths
today_dir_path = './board_data/' + datetime.now().strftime('%Y%m%d') + '/'
data_file_path = today_dir_path + 'data.csv'