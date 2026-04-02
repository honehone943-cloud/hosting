import os
import zipfile
from pyrogram import Client, filters

# --- CONFIGURATION ---
API_ID = 24889970  
API_HASH = "ec385e6a4bac2378bda98543ee8e22f1"
STORAGE_DIR = "hosted_files"
USAGE_IMAGE = "365265.jpg"

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

app = Client("my_userbot", api_id=API_ID, api_hash=API_HASH)

# --- .host COMMAND ---
@app.on_message(filters.me & filters.regex(r"^\.host$") & filters.reply)
async def host_zip(client, message):
    reply = message.reply_to_message
    
    if reply.document and reply.document.file_name.lower().endswith(".zip"):
        await message.edit("ZIP ဖိုင်ကို စစ်ဆေးနေသည်...")
        
        file_name = reply.document.file_name
        dest_path = os.path.join(STORAGE_DIR, file_name)
        
        # ယာယီ ဒေါင်းလုဒ်ဆွဲခြင်း
        tmp_path = await reply.download()
        
        try:
            with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                # ဖိုင်ထဲမှာ main.py နဲ့ requirements.txt ပဲ ရှိမရှိ စစ်ဆေးခြင်း
                required_files = {"main.py", "requirements.txt"}
                actual_files = {f for f in file_list if not f.endswith('/')} # folder တွေကို ဖယ်ထုတ်ပါသည်
                
                if actual_files == required_files:
                    # စစ်ဆေးမှု အောင်မြင်ရင် သိမ်းဆည်းမည်
                    os.rename(tmp_path, dest_path)
                    await message.edit(
                        f"Successfully Hosted\n\n"
                        f"File Name: {file_name}\n"
                        f"Status: main.py နှင့် requirements.txt ကို စစ်ဆေးပြီးပါပြီ။"
                    )
                else:
                    os.remove(tmp_path)
                    await message.edit("Error: ZIP ဖိုင်ထဲတွင် main.py နှင့် requirements.txt ဖိုင် (၂) ခုသာ ရှိရပါမည်။")
        except Exception as e:
            if os.path.exists(tmp_path): os.remove(tmp_path)
            await message.edit(f"Error: {str(e)}")
            
    else:
        await message.edit("ကျေးဇူးပြု၍ .zip ဖိုင်ကို Reply ပြန်ပြီး .host ဟုရေးပေးပါ။")

# --- .usage COMMAND ---
@app.on_message(filters.me & filters.regex(r"^\.usage$"))
async def show_usage(client, message):
    total_files = len(os.listdir(STORAGE_DIR))
    
    usage_text = (
        "အသုံးပြုနည်း လမ်းညွှန်\n\n"
        "၁။ မိမိ Host လုပ်လိုသော .zip ဖိုင်ကို အရင်ပို့ပါ။\n"
        "၂။ ZIP ထဲတွင် main.py နှင့် requirements.txt သာ ရှိရပါမည်။\n"
        "၃။ ထိုပို့ထားသော ဖိုင်ကို Reply လုပ်ပါ။\n"
        "၄။ .host ဟု ရေးပြီး ပို့လိုက်ပါ။\n\n"
        f"လက်ရှိအခြေအနေ: VPS Server Online\n"
        f"စုစုပေါင်းဖိုင်အရေအတွက်: {total_files}"
    )
    
    await message.delete()
    
    if os.path.exists(USAGE_IMAGE):
        await client.send_photo(
            chat_id=message.chat.id,
            photo=USAGE_IMAGE,
            caption=usage_text
        )
    else:
        await client.send_message(message.chat.id, usage_text)

if __name__ == "__main__":
    print("Userbot စတင်နေပါပြီ...")
    app.run()
  
