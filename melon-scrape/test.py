from scrapeMelon import getList
import json

# Test different chart types
chart_types = ["LIVE", "DAY", "WEEK", "MONTH"]

# Test one chart type
result = getList("LIVE")
# Convert bytes to string and load as JSON
data = json.loads(result.decode('utf-8'))

# Print the first entry nicely formatted
first_song = data['1']
print("\nFirst song details:")
for key, value in first_song.items():
    print(f"{key}: {value}")