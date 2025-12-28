import os

target_uri = "mongodb+srv://n220396_db_user:hQMlKzD1Wh1YCIwg@cluster0.rrb6kw1.mongodb.net/?appName=Cluster0"
env_path = ".env"

if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
else:
    lines = []

new_lines = []
uri_set = False

for line in lines:
    if line.startswith("MONGO_URI="):
        new_lines.append(f"MONGO_URI={target_uri}\n")
        uri_set = True
    elif line.strip(): # Keep non-empty lines
        new_lines.append(line)

if not uri_set:
    if new_lines and not new_lines[-1].endswith('\n'):
        new_lines.append('\n')
    new_lines.append(f"MONGO_URI={target_uri}\n")

with open(env_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("✅ .env updated with new MONGO_URI")
