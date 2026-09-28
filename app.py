import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

# -----------------------------------------------------------------------------
# CONFIG & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo dữ liệu mẫu trong Session State nếu chưa có
if "rooms" not in st.cookies and "rooms" not in st.session_state:
    st.session_state.rooms = pd.DataFrame([
        {"room_num": "101", "type": "Standard", "price": 500000, "status": "Trống", "clean_status": "Sạch"},
        {"room_num": "102", "type": "Standard", "price": 500000, "status": "Có khách", "clean_status": "Sạch"},
        {"room_num": "103", "type": "Deluxe", "price": 800000, "status": "Trống", "clean_status": "Bẩn"},
        {"room_num": "201", "type": "Deluxe", "price": 800000, "status": "Đã đặt", "clean_status": "Sạch"},
        {"room_num": "202", "type": "Suite", "price": 1500000, "status": "Có khách", "clean_status": "Sạch"},
        {"room_num": "203", "type": "Suite", "price": 1500000, "status": "Bảo trì", "clean_status": "Bẩn"},
    ])

if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame([
        {
            "booking_id": "BK001",
            "guest_name": "Nguyễn Văn A",
            "phone": "0901234567",
            "room_num": "102",
            "check_in": date.today(),
            "check_out": date.today(),
            "status": "Check-in",
            "total_price": 500000
        },
        {
            "booking_id": "BK002",
            "guest_name": "Trần Thị B",
            "phone": "0987654321",
            "room_num": "202",
            "check_in": date.today(),
            "check_out": date.today(),
            "status": "Check-in",
            "total_price": 1500000
        }
    ])

if "revenue_history" not in st.session_state:
    st.session_state.revenue_history = pd.DataFrame([
        {"date": date.today(), "amount": 2000000, "room_num": "102", "guest_name": "Nguyễn Văn A"},
    ])

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("🏨 HOTEL PMS")
st.sidebar.caption("Hệ thống Quản lý Khách sạn Vận hành")

menu = st.sidebar.radio(
    "Danh mục quản lý",
    ["Sơ đồ phòng (Room Rack)", "Lễ tân & Đặt phòng", "Buồng phòng (Housekeeping)", "Báo cáo Doanh thu & KPIs"]
)

# -----------------------------------------------------------------------------
# MODULE 1: SƠ ĐỒ PHÒNG (ROOM RACK)
# -----------------------------------------------------------------------------
if menu == "Sơ đồ phòng (Room Rack)":
