import sys
import time
from smartcard.scard import *
import pyautogui

oldresponse = 0
readers = None
hresult = None
hcontext = None
reader = None

argv = sys.argv[1:]

try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)

    assert hresult == SCARD_S_SUCCESS

    hresult, readers = SCardListReaders(hcontext, [])

    assert len(readers) > 0

    r = 0
    for c in argv:
        if c:
            r = c
            if not r.isnumeric():
                if r == 'h' or r == 'l':
                    print(readers)
                else:
                    print("Invalid arg, using default settings.")
            else:
                pass
        else:
            pass

    reader = readers[int(r)]
except AssertionError:
    print('No readers available. Connect one and start again.')
    sys.exit()
except IndexError:
    print('Reader selected out of range.')
    sys.exit()
except ValueError:
    for c in argv:
        if c.isnumeric():
            reader = readers[int(c)]
            break
        else:
            reader = readers[0]


while True:
    try:
        if not oldresponse == 0:
            time.sleep(5)
        hresult, hcard, dwActiveProtocol = SCardConnect(
            hcontext,
            reader,
            SCARD_SHARE_SHARED,
            SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)

        hresult, response = SCardTransmit(hcard, dwActiveProtocol, [0xFF, 0xCA, 0x00, 0x00, 0x00])

        if response == oldresponse:
            pass
        else:
            z = ''
            le = 0
            for x in response:
                le = le + 1
                z = str(z) + str(hex(x))[2:]
                print('.', end='')
                if le == 4:
                    oldresponse = response
                    break
            z = int(z, 16)
            if z == 1600:
                continue
            print(z)
            pyautogui.typewrite(str(z))
            pyautogui.press('enter')
    except SystemError:
        oldresponse = 0
    except KeyboardInterrupt:
        print('Program stopped by the user.')
        sys.exit()
    except Exception as e:
        print(e)
