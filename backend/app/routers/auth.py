from fastapi import APIRouter, HTTPException, Request, Depends

from schemas.auth import SignupRequest, LoginRequest
from core.firebase_config import get_pyrebase_auth, init_firebase_admin
from dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

auth_client = get_pyrebase_auth()
init_firebase_admin()


@router.post("/signup")
def signup(payload: SignupRequest):
    try:
        auth_client.create_user_with_email_and_password(payload.email, payload.password)
        return {"message": "Tạo tài khoản thành công"}
    except Exception as e:
        error_json = str(e)
        if "EMAIL_EXISTS" in error_json:
            raise HTTPException(status_code=400, detail="Email này đã được đăng ký. Vui lòng sử dụng email khác.")
        if "WEAK_PASSWORD" in error_json:
            raise HTTPException(status_code=400, detail="Mật khẩu quá ngắn (tối thiểu 6 ký tự).")
        raise HTTPException(status_code=400, detail=f"Lỗi đăng ký: {error_json}")

@router.post("/login")
def login(payload: LoginRequest):
    try:
        user = auth_client.sign_in_with_email_and_password(payload.email, payload.password)
        return {
            "email": payload.email,
            "uid": user["localId"],
            "idToken": user["idToken"],
            "refreshToken": user.get("refreshToken")
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "email": user["email"],
        "uid": user["uid"]
    }