from supabase import create_client, Client

url: str = "https://echedhjmjjdujlorygmj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjaGVkaGptampkdWpsb3J5Z21qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzYxNTM1MTEsImV4cCI6MjA1MTcyOTUxMX0.KUOogu2gnxzyogMoqjZR22xlN3IWDfavbjBhHyTCILk"
supabase: Client = create_client(url, key)

deletion_response = supabase.table("latest").delete().in_("ranking", list(range(1, 51))).execute()

print("\nResponse:")
print(deletion_response)