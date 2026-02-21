import requests
import concurrent.futures
import time

VALID_ROOMS = [
    'b201','b202','b205','b215','b216','b218','b219','b220','b221','b222','b223',
    'b301','b302','b306','b307','b308','b309','b310','b312','b313','b318',
    'b401','b402','b404','b405','b406','b407','b408','b409','b411','b412','b421',
    'b501','b502','b512','b517','b518','b520','b522','b521','b524','b523','b525'
]

def check_room(room_code):
    url = f"https://www.hesge.ch/heg/salle/{room_code}"
    try:
        response = requests.get(url, timeout=5)
        html = response.text
        if "Salle libre" in html:
            return "free"
        if "Salle occupée" in html:
            return "occupied"
        return "unknown"
    except Exception:
        return "error"

def scan_rooms(progress_callback=None, log_callback=None):
    free_rooms = []
    occupied_rooms = []
    total = len(VALID_ROOMS)
    completed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_room, room): room for room in VALID_ROOMS}
        for future in concurrent.futures.as_completed(futures):
            room = futures[future]
            status = future.result()

            if log_callback:
                log_callback(f"{room.upper()} : {status}")

            if status == "free":
                free_rooms.append(room)
            elif status == "occupied":
                occupied_rooms.append(room)

            completed += 1
            if progress_callback:
                progress_callback(completed / total * 100)

            time.sleep(0.005)

    return free_rooms, occupied_rooms
