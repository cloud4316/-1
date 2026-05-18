import time
import sys

text = input("Р'РІРµРґРёС‚Рµ С‚РµРєСЃС‚ РґР»СЏ Р±РµРіСѓС‰РµР№ СЃС‚СЂРѕРєРё: ")

while True:
    for i in range(len(text)):
        sys.stdout.write('\r' + text[i:] + text[:i])
        time.sleep(0.1)
        sys.stdout.flush()