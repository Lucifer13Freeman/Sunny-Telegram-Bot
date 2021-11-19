import os


"""User settings"""

async def check_user_settings(settings_path):
    
    check_file = os.path.exists(settings_path) 
    text = ""

    if check_file == False: 
        with open(settings_path, encoding = 'utf-8', mode = '+w') as f: f.write(text)


async def get_user_settings_text(settings_path):
    
    await check_user_settings(settings_path)
    with open(settings_path, encoding = 'utf-8') as f: is_text = f.readline() 
    return bool(is_text)


async def set_user_settings_text(settings_path, is_text):

    await check_user_settings(settings_path)

    text = ""
    if is_text == True: text = str(is_text)

    with open(settings_path, encoding = 'utf-8', mode = 'w') as f: f.write(text)


async def set_user_settings_text(settings_path, is_text):

    await check_user_settings(settings_path)

    text = ""
    if is_text == True: text = str(is_text)

    with open(settings_path, encoding = 'utf-8', mode = 'w') as f: f.write(text)