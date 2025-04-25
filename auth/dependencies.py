from fastapi import Depends , HTTPException
from auth.utils import decode_access_token , oauth2_scheme

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = decode_access_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from e
