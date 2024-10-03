import telnetlib
from influxdb import InfluxDBClient
import time
import logging

# Creating a logger
logger = logging.getLogger('actions_with_telnetlib_approach')
logger.setLevel(logging.DEBUG)

# Create a file handler with formatting in one step
file_handler = logging.FileHandler('actions_with_telnetlib_approach.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the handler to the logger
logger.addHandler(file_handler)

def extract_table_from_module(host, port, timeout=10, read_interval=5):
    try:
        logger.info(f"Connecting to {host}:{port}")
        
        # Step 1: Establish the Telnet connection
        tn = telnetlib.Telnet(host, port, timeout)
        logger.info("Connection established")
        
        # Step 2: Wait for the prompt (adjust the delay if needed)
        time.sleep(2)
        logger.info("Waiting for initial prompt")

        # Step 3: Send 'caen' command to set up the environment
        logger.info("Sending 'caen' command")
        tn.write(b"caen\n")
        time.sleep(2)  # Wait for the response after 'caen'

        # Step 4: Send 'c' command to enter the table state
        logger.info("Sending 'c' command to get table view")
        tn.write(b"c\n")
        time.sleep(2)  # Wait for the table to appear

        logger.info("Entering continuous table data reading mode")

        # Step 5: Continuously read the table data
        while True:
            try:
                # Send 'c' again just to refresh the table data
                logger.info("Requesting table data refresh with 'c' command")
                tn.write(b"c\n")
                time.sleep(2)  # Allow time for the table data to be refreshed

                # Read the table data from the module
                table_data = tn.read_very_eager().decode('utf-8')
                logger.info("Table data successfully read")
                
                # Process the table data (log or print it)
                print("Extracted table data:")
                print(table_data)

                # Wait for the next cycle
                time.sleep(read_interval)

            except KeyboardInterrupt:
                # Handle keyboard interruption gracefully
                logger.info("Keyboard interrupt received. Closing connection...")
                break    
        
        # Close the connection after the loop
        tn.close()
        logger.info("Connection closed")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
    
def main():
    # Example usage
    host = "172.18.4.142"
    port = 8100  # Use the appropriate port number
    extract_table_from_module(host, port, read_interval=10)  # Read the table
    
if __name__ == "__main__":  # Corrected this line
    main()
