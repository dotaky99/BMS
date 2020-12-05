import sys
from Registry import Registry
SYSTEM = sys.argv[1]
SOFTWARE = sys.argv[2]
SAM = sys.argv[3]
NTUSER = sys.argv[4]
USRCLASS = sys.argv[5]
REG = sys.argv[6]
PATH = sys.argv[7]
NAME = sys.argv[8]


# 하이브 파일과 경로를 입력받아 값을 반환하는 함수
# name이 "ALL"이라면 해당 키의 모든 값을 이중리스트로 반환
def get_reg_value(reg, path, name):
    try:
        registry = Registry.Registry(reg)
        key = registry.open(path)
        if name == "ALL":
            result = []
            for v in key.values():
                result.append([v.name(), v.value()])
            return result
        else:
            for v in key.values():
                if v.name() == name:
                    return v.value()
    except:
        return None


if __name__ == "__main__":
    if REG == "SYSTEM":
        print(get_reg_value(SYSTEM, PATH, NAME))
    elif REG == "SOFTWARE":
        print(get_reg_value(SOFTWARE, PATH, NAME))
    elif REG == "SAM":
        print(get_reg_value(SAM, PATH, NAME))
    elif REG == "NTUSER":
        print(get_reg_value(NTUSER, PATH, NAME))
    elif REG == "USRCLASS":
        print(get_reg_value(USRCLASS, PATH, NAME))