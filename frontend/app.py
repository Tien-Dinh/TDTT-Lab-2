import streamlit as st
from datetime import datetime, timedelta
from api_client import signup, login, get_notes, create_note, delete_note_api, update_note_api

st.set_page_config(page_title="My Notes", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None
if "notes" not in st.session_state:
    st.session_state.notes = []
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

def load_data():
    if not st.session_state.user:
        return
    try:
        st.session_state.notes = get_notes(st.session_state.user["idToken"])
    except Exception as e:
        st.session_state.user = None
        st.rerun()

def login_form():
    st.subheader("Đăng nhập")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
        goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký ngay")

    if goto_signup:
        st.session_state.show_signup = True
        st.rerun()

    if submitted:
        try:
            user = login(email, password)
            st.session_state.user = user
            load_data()
            st.success("Đăng nhập thành công!")
            st.rerun()
        except Exception as e:
            msg = e.response.json().get('detail') if hasattr(e, 'response') else str(e)
            st.error(f"Thất bại: {msg}")

def signup_form():
    st.subheader("Đăng ký tài khoản")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu (tối thiểu 6 ký tự)", type="password")
        submitted = st.form_submit_button("Tạo tài khoản", use_container_width=True)
        goto_login = st.form_submit_button("Đã có tài khoản? Đăng nhập")

    if goto_login:
        st.session_state.show_signup = False
        st.rerun()

    if submitted:
        try:
            signup(email, password)
            st.success("Đăng ký thành công! Hãy đăng nhập để tiếp tục.")
            st.session_state.show_signup = False
            st.rerun()
        except Exception as e:
            msg = e.response.json().get('detail') if hasattr(e, 'response') else str(e)
            st.error(f"Không thể đăng ký: {msg}")

st.title("Quản lý ghi chú cá nhân")

if st.session_state.user:
    st.info(f"👤 Tài khoản: {st.session_state.user['email']}")
    if st.button("Đăng xuất"):
        st.session_state.user = None
        st.session_state.notes = []
        st.rerun()
else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()

st.divider()

if st.session_state.user:
    st.subheader("Thêm ghi chú")
    with st.form("add_note_form", clear_on_submit=True):
        new_note = st.text_area("Nội dung ghi chú mới...", placeholder="Nhập gì đó vào đây...")
        submitted = st.form_submit_button("Lưu ghi chú")
        if submitted:
            if new_note.strip():
                try:
                    create_note(st.session_state.user["idToken"], new_note)
                    st.success("Đã lưu ghi chú mới thành công!")
                    load_data()
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi lưu: {str(e)}")
            else:
                st.warning("Vui lòng không để trống nội dung!")

    st.divider()
    
    st.subheader("Ghi chú của bạn")
    if not st.session_state.notes:
        st.write("Bạn chưa có ghi chú nào. Hãy tạo một cái nhé!")
    else:
        for note in st.session_state.notes:
            with st.container(border=True):
                if st.session_state.editing_id == note["id"]:
                    edited_content = st.text_area("Chỉnh sửa nội dung", value=note["content"], key=f"area_{note['id']}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Cập nhật", key=f"save_{note['id']}", use_container_width=True):
                            try:
                                update_note_api(st.session_state.user["idToken"], note["id"], edited_content)
                                st.session_state.editing_id = None
                                load_data()
                                st.success("Đã cập nhật thành công!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Lỗi cập nhật: {str(e)}")
                    with c2:
                        if st.button("Hủy", key=f"cancel_{note['id']}", use_container_width=True):
                            st.session_state.editing_id = None
                            st.rerun()
                
                else:
                    text_col, edit_col, del_col = st.columns([4, 1, 1])
                    with text_col:
                        st.write(note["content"])
                        if note.get("ts"):
                            try:
                                utc_time = datetime.fromisoformat(note["ts"].replace("Z", "+00:00"))
                                vn_time = utc_time + timedelta(hours=7)
                                st.caption(f"{vn_time.strftime('%I:%M:%S %p %d/%m/%Y')}")
                            except:
                                st.caption(f"{note['ts']}")
                    
                    with edit_col:
                        if st.button("Sửa", key=f"edit_{note['id']}", use_container_width=True):
                            st.session_state.editing_id = note["id"]
                            st.rerun()
                            
                    with del_col:
                        if st.button("Xóa", key=f"del_{note['id']}", use_container_width=True):
                            try:
                                delete_note_api(st.session_state.user["idToken"], note["id"])
                                load_data()
                                st.success("Đã xóa ghi chú.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Không thể xóa: {str(e)}")