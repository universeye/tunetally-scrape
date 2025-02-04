from scrapeMelon import getList
import json
from supabase import create_client, Client
import asyncio

url: str = "https://echedhjmjjdujlorygmj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjaGVkaGptampkdWpsb3J5Z21qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzYxNTM1MTEsImV4cCI6MjA1MTcyOTUxMX0.KUOogu2gnxzyogMoqjZR22xlN3IWDfavbjBhHyTCILk"
supabase: Client = create_client(url, key)


# Test different chart types
chart_types = ["LIVE", "DAY", "WEEK", "MONTH"]

# Test one chart type
result = getList("LIVE")
# Convert bytes to string and load as JSON
data = json.loads(result.decode('utf-8'))
#print data count
print(f"Data count: {len(data)}")
# Print the first entry nicely formatted

async def delete_records():
    print("Deleting existing records...")
    try:
        deletion_response = supabase.table("latest").delete().in_("ranking", list(range(1, 51))).execute()
        print(f"Deletion response: {deletion_response}")
        return deletion_response
    except Exception as exception:
        print(f"Deletion error: {exception}")
        raise exception

async def batch_insert():
    print("Batch inserting...")
    try:
        songs_to_insert = []
        for i in range(50):
            song = data[str(i+1)]  # data keys start from '1'
            songs_to_insert.append({
                "name": song['name'],
                "artists": song['artists'],
                "ranking": song['ranking'],
                "songId": song['songId'],
                "albumId": song['albumId'],
                "albumImageUrl": song['albumImageUrl'],
                "albumTitle": song['albumTitle']
            })
        
        response = supabase.table("latest").insert(songs_to_insert).execute()
        print(f"Inserted {len(songs_to_insert)} songs")
        return response
    except Exception as exception:
        print(f"Insertion error: {exception}")
        raise exception

async def main():
    try:
        # First delete existing records
        await delete_records()
        # Then insert new records
        response = await batch_insert()
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"Error in main: {e}")

# Run the async main function
asyncio.run(main())