from scrapeMelon import getList
import json
from supabase import create_client, Client

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

first_song = data['3']
print("\nFirst song details:")
for key, value in first_song.items():
    print(f"{key}: {value}")

#INSERT
response = (
    supabase.table("latest")
    .insert({
        "name": first_song['name'],
        "artists": first_song['artists'],
        "ranking": first_song['ranking'],
        "songId": first_song['songId'],
        "albumId": first_song['albumId'],
        "albumImageUrl": first_song['albumImageUrl'],
        "albumTitle": first_song['albumTitle']
    })
    .execute()
)

#UPDATE
# print("\nUpdating...")
# response = (
#     supabase.table("latest")
#     .update({"name": "test"})
#     .eq("ranking", 1)
#     .execute()
# )


print("\nResponse:")
print(response)