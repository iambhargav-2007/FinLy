import os

file_path = ".env"

if os.path.exists(file_path):
    print(f"Reading {file_path}...")
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Strip null bytes caused by PowerShell UTF-16 append
    clean_content = content.replace(b'\x00', b'')
    
    try:
        text = clean_content.decode('utf-8', errors='ignore')
        # Normalize newlines
        text = text.replace('\r\n', '\n').strip()
        
        print("Recovered Content Preview:")
        print(text[:50] + "...")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("✅ .env file fixed and saved as UTF-8")
    except Exception as e:
        print(f"❌ Failed to decode: {e}")
else:
    print("❌ .env file not found")
