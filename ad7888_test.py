from app.ad7888_driver.ad7888 import AD7888
from app.ad7888_driver.parameters import *
from time import sleep

def main():
    ad7888 = AD7888(0, 0)
    ad7888.set_reference(EXTERNAL_REFERENCE)
    try:
        print(ad7888.read_data())
    finally:
        ad7888.close()

if __name__ == "__main__":
    main()
