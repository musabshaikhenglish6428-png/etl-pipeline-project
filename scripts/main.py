import os
import logging

from load import (load_data, is_file_processed)
from transform import transform_data

def main():
    try:
        print("Pipeline Started")

        data_folder = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data"
        )
        files_loaded = 0
        for file_name in os.listdir(data_folder):
            if file_name.endswith(".csv"):
                if is_file_processed(file_name):
                    print(f"Skipping {file_name} already processed")
                    continue
                csv_path = os.path.join(
                    data_folder,
                    file_name
                )
                print(f"Processing {file_name}")
                try:
                    load_data(csv_path)
                    files_loaded += 1
                except Exception as file_error:
                    print(f"Failed Processing {file_name} : {file_error}")
                    logging.error(f"Failed Processing {file_name} : {file_error}")
                    continue

        print("Load Completed")

        if files_loaded > 0:
            transform_data()
            print("Transform Completed")

        else:
            print("No new files to process")
        
        print("Pipeline Finished")
    except Exception as e:
        print(f"Pipeline Failed: {e}")

if __name__ == "__main__":
    main()