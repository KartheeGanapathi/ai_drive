from google.cloud import storage
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import time

# Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def download_blob(blob, destination_folder):
    # Download a single blob from GCS to the local directory.
    try:
        destination_path = os.path.join(destination_folder, blob.name)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        blob.download_to_filename(destination_path)
        # logging.info(f"Downloaded {blob.name} to {destination_path}")
    except Exception as e:
        # logging.error(f"Error downloading {blob.name}: {e}")
        pass

def download_from_gcs(bucket_name, source_folder, destination_folder):
    # Download all files from the specified GCS folder to a local directory.
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_folder)
    
    # Hyperparameter - Concurrency, set to 16
    # can be adjusted based on trial and error
    max_workers = 16 
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the executor for each blob in the blobs list.
        # Each task will call the download_blob function for a given blob and its destination folder.
        # We use a dictionary to map each Future object to its corresponding blob.
        future_to_blob = {executor.submit(download_blob, blob, destination_folder): blob for blob in blobs}
        for future in as_completed(future_to_blob):
            try: # Retrieve the result of the completed future. This will raise an exception if the task failed.
                future.result()
            except Exception as e: # Retrieve the blob associated with the failed future from the dictionary.
                blob = future_to_blob[future]
                logging.error(f"Error processing {blob.name}: {e}")

def main():
    gcs_folders = sys.argv[1].split(',')
    destination_folder = "/mnt/disks/local_disk_1"

    # Iterate over each GCS folder specified in the input.
    for gcs_folder in gcs_folders:
        startTime = time.time()
        gcs_folder = gcs_folder.replace("gs://", "")
        # Remove the 'gs://' prefix from the GCS folder URL and split it into bucket and source folder components.
        bucket_name = gcs_folder.split("/")[0]
        source_folder = gcs_folder.split("/")[1]
        # Call the download function to download files from the specified GCS bucket and source folder.
        download_from_gcs(bucket_name, source_folder, destination_folder)
        endTime = time.time()
        print('Completed downloading -> ', gcs_folder)
        print('it took ', round(endTime-startTime, 2), 's\n')

if __name__ == "__main__":
    main()