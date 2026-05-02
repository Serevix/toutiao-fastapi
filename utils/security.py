from passlib.context import CryptContext

#创建密码上下文              加密算法                自适应
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
#密码加密
def get_hash_password(password:str):
    return pwd_context.hash(password)