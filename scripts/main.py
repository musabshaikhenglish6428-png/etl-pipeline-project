import os
import logging

from load import load_data, is_file_processed
from transform import transform_data


def main():
    try:
        logging.info("Pipeline Started")

        data_folder = os.path.join(
            os.path.dirname(__file__),
            "..",
            "data"
        )

        files_loaded = 0
        files_processed = 0
        files_skipped = 0
        files_failed = 0

        for file_name in os.listdir(data_folder):

            if not file_name.endswith(".csv"):
                continue

            if is_file_processed(file_name):
                logging.info(
                    f"Skipping {file_name} already processed"
                )
                files_skipped += 1
                continue

            csv_path = os.path.join(
                data_folder,
                file_name
            )

            logging.info(f"Processing {file_name}")

            try:
                load_data(csv_path)

                files_loaded += 1
                files_processed += 1

            except Exception as file_error:

                logging.error(f"Failed Processing {file_name}: {file_error}")

                files_failed += 1
                continue

        logging.info("Load Completed")

        if files_loaded > 0:
            transform_data()
            logging.info("Transform Completed")
        else:
            logging.info("No new files to process")

        logging.info("Batch Summary")
        logging.info(f"Files Processed : {files_processed}")
        logging.info(f"Files Skipped : {files_skipped}")
        logging.info(
            f"Files Failed : {files_failed}"
        )

        logging.info("Pipeline Finished")

    except Exception as e:
        logging.error(f"Pipeline Failed: {e}")


if __name__ == "__main__":
    main()