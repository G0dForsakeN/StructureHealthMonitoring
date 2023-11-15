from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import matplotlib.pyplot as plt

uri = "mongodb+srv://admin:W176xRINyYUOZCKE@cluster0.r000trc.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Access the "Cluster0" database
db = client["Cluster0"]

# Access the "Accl_Data" collection
collection = db["Accl_Data"]

# Use find() to retrieve documents
cursor = collection.find()

for document in cursor:
    csv_data = document['csv_data']
    metadata = document['metadata']
    print(metadata)

    # Get the data for "Channel 0" and "Channel 1"
    channel0_data = csv_data['Channel 0']
    channel1_data = csv_data['Channel 1']

    # Get the length of data in "Channel 0" and "Channel 1"
    channel0_length = len(channel0_data)
    channel1_length = len(channel1_data)

    # Create an index list for the x-axis
    index = list(range(channel0_length))

    # Plot both channels in one graph with different colors
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(index, channel0_data, label='Channel 0', color='blue')
    ax.plot(index, channel1_data, label='Channel 1', color='orange')
    ax.set_xlabel('Time - Datapoints')
    ax.set_ylabel('Acceleration m/s^2')
    ax.set_title('Channel 0 and Channel 1 Data')
    ax.legend()

    # Show metadata on top of the graph
    fig.suptitle(f"Metadata: {metadata}", fontsize=12)
    
    # Adjust spacing
    plt.subplots_adjust(top=0.92)

    plt.show()
