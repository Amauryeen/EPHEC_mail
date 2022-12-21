from lib.App import *
from lib.Exceptions import *
from lib.Tester import *

if __name__ == "__main__":
    unittest.main(exit=False)

    App.menu()
    while True:
        try:
            App.menu_choice()
            break

        except NotAValidChoice as error:
            print(f"[!] : {error}")
        except ValueError as error:
            print(f"[!] : {error}")
