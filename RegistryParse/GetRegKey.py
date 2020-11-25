import sys
from RegistryParse.Registry import Registry

SYSTEM = sys.argv[1]
SOFTWARE = sys.argv[2]
SAM = sys.argv[3]
NTUSER = sys.argv[4]
USRCLASS = sys.argv[5]


# 하이브 파일과 경로를 입력받아 값을 반환하는 함수
# name이 "ALL"이라면 해당 키의 모든 값을 이중리스트로 반환
def get_reg_value(reg, path, name):
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


# 레지스트리 키가 있는지 확인하는 함수
def exist_reg_key(reg, path):
    registry = Registry.Registry(reg)
    try:
        key = registry.open(path)
        return True
    except:
        return False


# sid 값을 받아 user명을 반환하는 함수
def sid_to_user(sid):
    registry = Registry.Registry()
    path = "Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\" + sid
    key = registry.open(path)
    user_name = None

    for v in key.values():
        if v.name() == "ProfileImagePath":
            user_name = v.value().rpartition('\\')[2]

    return user_name