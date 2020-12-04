import sys
from Registry import Registry


SYSTEM = sys.argv[1]
SOFTWARE = sys.argv[2]
SAM = sys.argv[3]
NTUSER = sys.argv[4]
USRCLASS = sys.argv[5]
REG = sys.argv[6]
PATH = sys.argv[7]


# 레지스트리 키가 있는지 확인하는 함수
def exist_reg_key(reg, path):
    registry = Registry.Registry(reg)
    try:
        key = registry.open(path)
        return True
    except:
        return False


if __name__ == "__main__":
    if REG == "SYSTEM":
        print(exist_reg_key(SYSTEM, PATH))
    elif REG == "SOFTWARE":
        print(exist_reg_key(SOFTWARE, PATH))
    elif REG == "SAM":
        print(exist_reg_key(SAM, PATH))
    elif REG == "NTUSER":
        print(exist_reg_key(NTUSER, PATH))
    elif REG == "USRCLASS":
        print(exist_reg_key(USRCLASS, PATH))