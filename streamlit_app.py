import streamlit as st
import pandas as pd
import io
import json
import os
from datetime import datetime
from supabase import create_client, Client

# 1. إعداد الصفحة وتنسيق الاتجاه العربي الموحد RTL
st.set_page_config(page_title='شركة ميم الخماسية للتصنيع - النظام المحاسبي الموحد', layout='wide', page_icon='🏢')

ADMIN_PASSWORD = "admin5m"
USER_PASSWORD = "user5m"

# إعدادات الربط السحابي بـ Supabase
SUPABASE_URL = "https://ohoqprtvmhyjomaavwct.supabase.co"
SUPABASE_KEY = "sb_publishable_T6YFCaos1EexLgGG9KtwCw_nNMRHjJ_"

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

if 'theme_mode' not in st.session_state:
    st.session_state['theme_mode'] = '🌙 وضع ليلي'

if '🌙' in st.session_state['theme_mode']:
    bg_app = "#0B132B"
    bg_card = "#1C2541"
    bg_sidebar = "#0B132B"
    text_color = "#FFFFFF"
    border_color = "#D97706"
    btn_sidebar_bg = "linear-gradient(135deg, #1C2541 0%, #0B132B 100%)"
    btn_sidebar_text = "#F59E0B"
    header_bg = "#0B132B"
    dialog_bg = "#1C2541"
    dialog_text = "#FFFFFF"
    stars_css = """
        body, .stApp, [data-testid="stHeader"] {
            background-color: #0B132B !important;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 40px 70px, #f59e0b, rgba(0,0,0,0)),
                radial-gradient(1px 1px at 90px 40px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 160px 120px, #ffffff, rgba(0,0,0,0)),
                radial-gradient(1.5px 1.5px at 230px 190px, #f59e0b, rgba(0,0,0,0)),
                radial-gradient(2px 2px at 300px 80px, #ffffff, rgba(0,0,0,0));
            background-repeat: repeat;
            background-size: 350px 350px;
        }
    """
else:
    bg_app = "#F8FAFC"
    bg_card = "#FFFFFF"
    bg_sidebar = "#FFFFFF"
    text_color = "#0F172A"
    border_color = "#D97706"
    btn_sidebar_bg = "linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%)"
    btn_sidebar_text = "#D97706"
    header_bg = "#F8FAFC"
    dialog_bg = "#FFFFFF"
    dialog_text = "#0F172A"
    stars_css = ""

st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

        {stars_css}

        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            direction: rtl !important;
            text-align: right !important;
            color: {text_color} !important;
            font-family: 'Cairo', sans-serif !important;
            overflow-x: hidden !important;
            -webkit-text-size-adjust: 100% !important;
        }}

        /* إظهار وتجميل زر الفتح والإغلاق للقائمة الجانبية بوضوح */
        [data-testid="stHeader"] {{
            background-color: {header_bg} !important;
            border-bottom: none !important;
        }}

        [data-testid="stSidebarCollapseButton"], [data-testid="stSidebarActionButton"] {{
            display: block !important;
            color: #F59E0B !important;
            background-color: #1C2541 !important;
            border: 1px solid #D97706 !important;
            border-radius: 8px !important;
            margin: 5px !important;
        }}

        .main .block-container {{
            padding-top: 0.2rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}

        h1, h2, h3, h4, h5, h6, .stMarkdown, label, p, span, div {{
            direction: rtl !important;
            text-align: right !important;
            color: {text_color} !important;
            font-family: 'Cairo', sans-serif !important;
            word-wrap: break-word !important;
        }}

        /* أبعاد وسلوك القائمة الجانبية الصريح للموبايل والكمبيوتر */
        [data-testid="stSidebar"] {{
            border-left: 2px solid {border_color} !important;
            background: {bg_sidebar} !important;
        }}

        [data-testid="stSidebarContent"] {{
            padding-top: 0.2rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-bottom: 0.2rem !important;
        }}

        [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
            color: {text_color} !important;
            font-size: 13px !important;
            font-weight: 800 !important;
        }}

        .sidebar-logo-card {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 2px solid #D97706;
            border-radius: 12px;
            padding: 10px 8px;
            text-align: center !important;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        .sidebar-logo-text {{
            font-size: 50px !important;
            font-weight: 900 !important;
            color: #EF4444 !important;
            font-family: Arial, sans-serif !important;
            line-height: 1 !important;
            margin: 0 !important;
            text-align: center !important;
        }}

        .sidebar-company-title {{
            color: #F59E0B !important;
            font-size: 15px !important;
            font-weight: 900 !important;
            margin-top: 4px !important;
            margin-bottom: 0 !important;
            text-align: center !important;
        }}

        .sidebar-section-title {{
            color: #F59E0B !important;
            font-size: 14px !important;
            font-weight: 900 !important;
            border-bottom: 2px solid #D97706;
            padding-bottom: 3px;
            margin-top: 12px;
            margin-bottom: 6px;
            text-align: right !important;
        }}

        [data-testid="stSidebar"] .stButton>button {{
            width: 100% !important;
            background: {btn_sidebar_bg} !important;
            color: {btn_sidebar_text} !important;
            border: 1px solid #D97706 !important;
            border-radius: 6px !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            padding: 6px 8px !important;
            margin-bottom: 3px !important;
            text-align: right !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stButton>button:hover {{
            background: #D97706 !important;
            color: #FFFFFF !important;
        }}

        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], [data-testid="stDateInput"] input {{
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 6px !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            padding: 4px 8px !important;
        }}

        ul[data-baseweb="menu"], div[role="listbox"], [data-baseweb="popover"], [data-baseweb="popover"] > div, div[data-baseweb="menu"] {{
            background-color: #1C2541 !important;
            color: #FFFFFF !important;
            border: 1px solid #D97706 !important;
            border-radius: 8px !important;
        }}

        li[role="option"], li[role="option"] *, div[role="option"], div[role="option"] * {{
            color: #FFFFFF !important;
            background-color: #1C2541 !important;
            font-weight: 800 !important;
            font-size: 13px !important;
        }}

        li[role="option"]:hover, li[role="option"]:hover *, div[role="option"]:hover, div[role="option"]:hover * {{
            background-color: #D97706 !important;
            color: #FFFFFF !important;
        }}

        [data-testid="stMetricValue"] div {{
            font-size: 22px !important;
            font-weight: 900 !important;
            text-align: center !important;
            color: #F59E0B !important;
            white-space: nowrap !important;
        }}

        [data-testid="stMetricLabel"] label, [data-testid="stMetricLabel"] div {{
            font-size: 14px !important;
            font-weight: 800 !important;
            text-align: center !important;
            white-space: nowrap !important;
        }}

        .stMetric {{
            background-color: {bg_card} !important;
            border-radius: 10px !important;
            padding: 8px 10px !important;
            border: 1px solid {border_color} !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 4px !important;
            text-align: center !important;
        }}

        div.stButton > button, div.stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {{
            background: linear-gradient(135deg, #1C2541 0%, #0B132B 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid #D97706 !important;
            border-radius: 8px !important;
            font-weight: 800 !important;
            font-size: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
            padding: 6px 10px !important;
            width: 100% !important;
        }}

        div.stButton > button:hover, div.stDownloadButton > button:hover {{
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
            color: #FFFFFF !important;
            border-color: #F59E0B !important;
        }}

        .cash-card-item {{
            background-color: {bg_card};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 6px 10px !important;
            margin-bottom: 2px !important;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .amt-pos {{
            color: #10B981 !important;
            font-weight: 900 !important;
            font-size: 17px !important;
        }}

        .amt-neg {{
            color: #EF4444 !important;
            font-weight: 900 !important;
            font-size: 17px !important;
        }}

        .welcome-card-lux {{
            background: linear-gradient(135deg, #0B132B 0%, #1E3A8A 100%);
            border-radius: 20px;
            padding: 20px 15px;
            text-align: center !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            margin-top: 5px;
            border: 2px solid #D97706;
        }}

        .title-company-royal {{
            font-size: 30px !important;
            font-weight: 900 !important;
            color: #F59E0B !important;
            text-shadow: 0 0 12px rgba(245, 158, 11, 0.4);
            margin-top: 8px;
            margin-bottom: 8px;
            text-align: center !important;
        }}

        .company-header-inner {{
            background: linear-gradient(135deg, {bg_card} 0%, {bg_app} 100%);
            border: 2px solid #D97706;
            border-radius: 12px;
            padding: 6px 12px;
            text-align: center !important;
            margin-top: 0px;
            margin-bottom: 8px;
        }}

        .company-header-inner-title {{
            font-size: 20px !important;
            font-weight: 900 !important;
            color: #F59E0B !important;
            margin: 0 !important;
            text-align: center !important;
        }}

        .company-header-inner-sub {{
            font-size: 12px !important;
            color: #94A3B8 !important;
            margin: 0 !important;
        }}

        /* ضوابط الموبايل والآيفون الصريحة لاستقرار القائمة الشاملة */
        @media screen and (max-width: 768px) {{
            [data-testid="stSidebar"] {{
                width: 82vw !important;
            }}

            .main .block-container {{
                padding-left: 4px !important;
                padding-right: 4px !important;
            }}

            [data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
            }}

            [data-testid="column"], [data-testid="stColumn"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                margin-bottom: 4px !important;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# إدارة الدخول والجلسة
if 'app_started' not in st.session_state:
    st.session_state['app_started'] = False

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'الرئيسية'

august_payroll_data = [
    # 1. رواتب الخرج (المصنع)
    {'م': 1, 'الاسم': 'حبيب مد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-15', 'تاريخ انتهاء العقد': '2027-03-30', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-09-20', 'تاريخ انتهاء العقد': '2026-12-31', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 4, 'الاسم': 'محمد أبو صبري', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-01', 'تاريخ انتهاء العقد': '2027-06-15', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 6, 'الاسم': 'رفيق الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 1600.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-10', 'تاريخ انتهاء العقد': '2027-03-01', 'الخصومات': 1600.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'لم يُصرف', 'الملاحظات': ''},
    {'م': 7, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-01', 'تاريخ انتهاء العقد': '2027-02-14', 'الخصومات': 0.0, 'الدفعة 1': 4000.0, 'الدفعة 2': 3000.0, 'الدفعة المدفوعة': 7000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 8, 'الاسم': 'ذاكر', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-10', 'تاريخ انتهاء العقد': '2027-05-20', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 9, 'الاسم': 'رحيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-20', 'تاريخ انتهاء العقد': '2027-02-01', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 10, 'الاسم': 'محمد شریف', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-10', 'تاريخ انتهاء العقد': '2027-02-28', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 11, 'الاسم': 'بطشا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-05', 'تاريخ انتهاء العقد': '2027-02-12', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 12, 'الاسم': 'السيد محمود', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-10', 'تاريخ انتهاء العقد': '2027-06-20', 'الخصومات': 0.0, 'الدفعة 1': 500.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 13, 'الاسم': 'حبيب الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-25', 'تاريخ انتهاء العقد': '2027-05-30', 'الخصومات': 0.0, 'الدفعة 1': 1000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 14, 'الاسم': 'دلال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-15', 'تاريخ انتهاء العقد': '2027-05-10', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 15, 'الاسم': 'انيس الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-10', 'تاريخ انتهاء العقد': '2026-12-25', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 16, 'الاسم': 'فاربيس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-20', 'تاريخ انتهاء العقد': '2027-02-15', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 17, 'الاسم': 'مطاوع', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-05', 'تاريخ انتهاء العقد': '2027-01-20', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 18, 'الاسم': 'قدوس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-28', 'تاريخ انتهاء العقد': '2027-04-18', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 19, 'الاسم': 'مد إبراهيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-05-01', 'تاريخ انتهاء العقد': '2027-07-10', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 20, 'الاسم': 'سلمان محي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-30', 'تاريخ انتهاء العقد': '2027-02-10', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 21, 'الاسم': 'مدلايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-01', 'تاريخ انتهاء العقد': '2027-01-15', 'الخصومات': 0.0, 'الدفعة 1': 1000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 22, 'الاسم': 'سمير المغازي', 'الوظيفة': 'كيميائي / معمل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-12-31', 'تاريخ انتهاء العقد': '2027-12-31', 'الخصومات': 5000.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'لم يُصرف', 'الملاحظات': ''},
    {'م': 23, 'الاسم': 'ريحاني', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-09-25', 'تاريخ انتهاء العقد': '2026-12-05', 'الخصومات': 0.0, 'الدفعة 1': 2200.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 24, 'الاسم': 'عمرو فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-01', 'تاريخ انتهاء العقد': '2027-05-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 25, 'الاسم': 'محمد فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-01', 'تاريخ انتهاء العقد': '2027-05-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 26, 'الاسم': 'محمد رضا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-15', 'تاريخ انتهاء العقد': '2027-04-30', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 27, 'الاسم': 'شوقي كامل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-30', 'تاريخ انتهاء العقد': '2027-01-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 28, 'الاسم': 'محمد أبو نهي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-05', 'تاريخ انتهاء العقد': '2026-12-15', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 4000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 29, 'الاسم': 'ساجد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-15', 'تاريخ انتهاء العقد': '2027-01-01', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 30, 'الاسم': 'محي الدين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-15', 'تاريخ انتهاء العقد': '2027-06-01', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 31, 'الاسم': 'أيوب', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-08-01', 'تاريخ انتهاء العقد': '2026-11-15', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 32, 'الاسم': 'علي إسماعيل', 'الوظيفة': 'معمل', 'الراتب الأساسي': 4500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-25', 'تاريخ انتهاء العقد': '2027-01-15', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 1500.0, 'الدفعة المدفوعة': 4500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 33, 'الاسم': 'إبراهيم السيد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-15', 'تاريخ انتهاء العقد': '2027-02-01', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 34, 'الاسم': 'محمد ریان', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-01', 'تاريخ انتهاء العقد': '2027-04-01', 'الخصومات': 0.0, 'الدفعة 1': 1000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 35, 'الاسم': 'فهمي محمد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-05', 'تاريخ انتهاء العقد': '2027-03-20', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 36, 'الاسم': 'مصطفي عماد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-03-15', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 37, 'الاسم': 'محمد حمدان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 4500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-10', 'تاريخ انتهاء العقد': '2027-04-05', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 1500.0, 'الدفعة المدفوعة': 4500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 38, 'الاسم': 'روبيل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-05-10', 'تاريخ انتهاء العقد': '2027-07-01', 'الخصومات': 0.0, 'الدفعة 1': 500.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    
    # 2. مستودع الرياض
    {'م': 39, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-12', 'تاريخ انتهاء العقد': '2027-04-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 40, 'الاسم': 'محمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 0.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-05', 'تاريخ انتهاء العقد': '2027-04-10', 'الخصومات': 0.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'لم يُصرف', 'الملاحظات': ''},
    {'م': 41, 'الاسم': 'سمان السواق', 'الوظيفة': 'سائق', 'الراتب الأساسي': 3500.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-25', 'تاريخ انتهاء العقد': '2027-01-30', 'الخصومات': 500.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 42, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب الأساسي': 4000.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-01-20', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 4000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 43, 'الاسم': 'إبراهيم جمال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-15', 'تاريخ انتهاء العقد': '2027-05-18', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},

    # 3. رواتب الملقة (مستودع الخرج)
    {'م': 44, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-09-05', 'تاريخ انتهاء العقد': '2026-10-10', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 45, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-06-01', 'تاريخ انتهاء العقد': '2027-08-01', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 46, 'الاسم': 'محمود عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-10', 'تاريخ انتهاء العقد': '2027-03-15', 'الخصومات': 7000.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'لم يُصرف', 'الملاحظات': ''},
    {'م': 47, 'الاسم': 'شمشاد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-20', 'تاريخ انتهاء العقد': '2026-12-30', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 4000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 48, 'الاسم': 'زنجیر', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-05', 'تاريخ انتهاء العقد': '2027-05-12', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 49, 'الاسم': 'بابلو', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-12', 'تاريخ انتهاء العقد': '2027-01-25', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 50, 'الاسم': 'إسماعيل الحداد', 'الوظيفة': 'حداد', 'الراتب الأساسي': 6000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-20', 'تاريخ انتهاء العقد': '2027-04-10', 'الخصومات': 0.0, 'الدفعة 1': 3500.0, 'الدفعة 2': 2500.0, 'الدفعة المدفوعة': 6000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 51, 'الاسم': 'نعيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-15', 'تاريخ انتهاء العقد': '2027-02-20', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 52, 'الاسم': 'مرسي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-05', 'تاريخ انتهاء العقد': '2027-06-12', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 53, 'الاسم': 'محمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-18', 'تاريخ انتهاء العقد': '2026-12-28', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 54, 'الاسم': 'احمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-25', 'تاريخ انتهاء العقد': '2027-03-30', 'الخصومات': 0.0, 'الدفعة 1': 2500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 55, 'الاسم': 'عبد الرحمن محمد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-30', 'تاريخ انتهاء العقد': '2027-05-25', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''}
]

def fetch_cloud_store(key_name, default_data):
    session_key = f"cloud_cache_{key_name}"
    if session_key in st.session_state:
        return st.session_state[session_key]
    try:
        response = supabase.table('app_stores').select('data_val').eq('store_key', key_name).execute()
        if response.data and len(response.data) > 0:
            val = response.data[0]['data_val']
            st.session_state[session_key] = val
            return val
    except Exception:
        pass
    st.session_state[session_key] = default_data
    return default_data

def save_cloud_store(key_name, data_val):
    session_key = f"cloud_cache_{key_name}"
    st.session_state[session_key] = data_val
    try:
        supabase.table('app_stores').upsert({'store_key': key_name, 'data_val': data_val}).execute()
    except Exception:
        pass

def load_last_selected_month():
    val = fetch_cloud_store('last_selected_month', {'last_month': 'أغسطس 2026'})
    return val.get('last_month', 'أغسطس 2026')

def save_last_selected_month(month_name):
    save_cloud_store('last_selected_month', {'last_month': month_name})

def load_monthly_payroll_store():
    # استكمال استدعاء المخزن المحدث المباشر لشهر أغسطس
    return fetch_cloud_store('monthly_payroll_store_v4', {})

def save_monthly_payroll_store(store_data):
    save_cloud_store('monthly_payroll_store_v4', store_data)

def get_payroll_for_month(month_name):
    store = load_monthly_payroll_store()
    if month_name in store and len(store[month_name]) > 0:
        return pd.DataFrame(store[month_name])
    else:
        if month_name == 'أغسطس 2026':
            df_base = pd.DataFrame(august_payroll_data)
        else:
            df_base = pd.DataFrame(august_payroll_data)
            df_base['الدفعة 1'] = 0.0
            df_base['الدفعة 2'] = 0.0
            df_base['الخصومات'] = 0.0
            df_base['الدفعة المدفوعة'] = 0.0
            df_base['المتبقي'] = df_base['الراتب الأساسي']
            df_base['نوع الإجراء'] = 'لم يُصرف'

        store[month_name] = df_base.to_dict(orient='records')
        save_monthly_payroll_store(store)
        return df_base

def save_payroll_for_month(df, month_name):
    store = load_monthly_payroll_store()
    store[month_name] = df.to_dict(orient='records')
    save_monthly_payroll_store(store)

def load_cash_data():
    return fetch_cloud_store('cashbox_data', {})

def save_cash_data(data):
    save_cloud_store('cashbox_data', data)

def load_audit_data():
    return fetch_cloud_store('audit_history', [])

def save_audit_data(data):
    save_cloud_store('audit_history', data)

def load_drivers_data():
    return fetch_cloud_store('driver_custody', [])

def save_drivers_data(data):
    save_cloud_store('driver_custody', data)

def calculate_saudi_gratuity_and_leave(salary, start_date_str):
    try:
        start_d = datetime.strptime(str(start_date_str), '%Y-%m-%d').date()
        today = datetime.now().date()
        diff_days = (today - start_d).days
        years = diff_days / 365.25
        
        if years <= 5:
            gratuity = years * (salary / 2.0)
        else:
            gratuity = (5 * (salary / 2.0)) + ((years - 5) * salary)
            
        annual_leave_days = 21 if years <= 5 else 30
        daily_rate = salary / 30.0
        leave_allowance = annual_leave_days * daily_rate
        
        return round(years, 2), round(gratuity, 2), round(leave_allowance, 2)
    except:
        return 0.0, 0.0, 0.0

@st.dialog("تعديل الرصيد الافتتاحي للصندوق")
def opening_balance_dialog(month_name, target_box):
    all_cash_db = load_cash_data()
    m_cash = all_cash_db.get(month_name, {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []})
    active_opening_key = 'opening' if target_box == 'main' else 'acc_opening'
    opening_bal = m_cash.get(active_opening_key, 0.0)

    st.write(f"تثبيت وتعديل الرصيد الافتتاحي لـ **{'الخزينة الرئيسية' if target_box == 'main' else 'عُهدة omar'}** لشهر ({month_name}):")
    with st.form("set_opening_balance_dialog_form"):
        new_opening_val = st.number_input("الرصيد الافتتاحي (ر.س):", min_value=0.0, value=float(opening_bal))
        sub_op = st.form_submit_button("💾 تثبيت الرصيد الافتتاحي")
        if sub_op:
            m_cash[active_opening_key] = new_opening_val
            all_cash_db[month_name] = m_cash
            save_cash_data(all_cash_db)
            st.success("تم التثبيت السحابي!")
            st.rerun()

@st.dialog("✏️ تعديل بيانات السند")
def edit_cash_voucher_dialog(trans_idx, month_name, target_box="main"):
    all_cash_db = load_cash_data()
    m_cash = all_cash_db.get(month_name, {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []})
    box_key = 'transactions' if target_box == 'main' else 'acc_transactions'
    c_trans = m_cash.get(box_key, [])
    
    if trans_idx < len(c_trans):
        t_item = c_trans[trans_idx]
        st.write(f"تعديل السند رقم: **#{t_item.get('code', t_item['id'])}**")
        
        with st.form(f"edit_voucher_form_{trans_idx}"):
            e_party = st.text_input("صادر إلى / مستلم من:", value=t_item['party'])
            e_amt = st.number_input("المبلغ (ر.س):", min_value=0.0, value=float(t_item['amount']))
            e_method = st.selectbox("طريقة الدفع:", ["نقداً بالصندوق", "تحويل بنكي", "شيك"], index=["نقداً بالصندوق", "تحويل بنكي", "شيك"].index(t_item.get('method', 'نقداً بالصندوق')))
            e_notes = st.text_input("البيان والملاحظات:", value=t_item.get('notes', ''))
            
            sub_e_voucher = st.form_submit_button("💾 حفظ تعديلات السند")
            if sub_e_voucher:
                c_trans[trans_idx]['party'] = e_party
                c_trans[trans_idx]['amount'] = e_amt
                c_trans[trans_idx]['method'] = e_method
                c_trans[trans_idx]['notes'] = e_notes
                m_cash[box_key] = c_trans
                all_cash_db[month_name] = m_cash
                save_cash_data(all_cash_db)
                st.success("تم تعديل بيانات السند بنجاح!")
                st.rerun()

@st.dialog("إنشاء سند جديد")
def quick_cash_voucher_dialog(default_type, month_name, target_box="main"):
    st.write(f"إضافة سند لشهر: **{month_name}** ({'الرئيسية' if target_box == 'main' else 'omar'})")
    
    if target_box == "main":
        type_options = ["سند قبض", "سند صرف", "🔄 تحويل عُهدة إلى (omar)"]
    else:
        type_options = ["سند قبض", "سند صرف", "🔄 تحويل عُهدة إلى (wahby)"]

    with st.form("quick_cash_form", clear_on_submit=True):
        q_type = st.selectbox("نوع السند:", type_options, index=0 if "قبض" in default_type else 1)
        q_party = st.text_input("صادر إلى / مستلم من:", placeholder="اسم الجهة...")
        q_amt = st.number_input("المبلغ (ر.س):", min_value=0.0, value=0.0)
        q_method = st.selectbox("طريقة الدفع:", ["نقداً بالصندوق", "تحويل بنكي", "شيك"])
        q_notes = st.text_input("البيان والملاحظات:")
        
        q_sub = st.form_submit_button("حفظ السند")
        if q_sub:
            if q_party and q_amt > 0:
                all_cash = load_cash_data()
                if month_name not in all_cash:
                    all_cash[month_name] = {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []}
                
                m_cash = all_cash[month_name]
                box_key = 'transactions' if target_box == 'main' else 'acc_transactions'
                if box_key not in m_cash:
                    m_cash[box_key] = []
                    
                c_trans = m_cash[box_key]
                
                if "تحويل عُهدة إلى (omar)" in q_type and target_box == "main":
                    v_code = f"TRF-{(len(c_trans) + 1):03d}"
                    c_trans.append({
                        'id': len(c_trans) + 1,
                        'code': v_code,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'type': 'سند صرف',
                        'party': f"تحويل عُهدة إلى المحاسب (omar) - {q_party}",
                        'amount': q_amt,
                        'method': q_method,
                        'notes': q_notes
                    })
                    
                    if 'acc_transactions' not in m_cash:
                        m_cash['acc_transactions'] = []
                    acc_trans = m_cash['acc_transactions']
                    acc_trans.append({
                        'id': len(acc_trans) + 1,
                        'code': f"REC-TRF-{(len(acc_trans) + 1):03d}",
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'type': 'سند قبض',
                        'party': f"استلام عُهدة محولة من الخزينة الرئيسية (wahby)",
                        'amount': q_amt,
                        'method': q_method,
                        'notes': q_notes
                    })
                    m_cash['acc_transactions'] = acc_trans

                elif "تحويل عُهدة إلى (wahby)" in q_type and target_box == "accountant":
                    v_code = f"TRF-ACC-{(len(c_trans) + 1):03d}"
                    c_trans.append({
                        'id': len(c_trans) + 1,
                        'code': v_code,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'type': 'سند صرف',
                        'party': f"تحويل نقدية واسترداد إلى الخزينة الرئيسية (wahby) - {q_party}",
                        'amount': q_amt,
                        'method': q_method,
                        'notes': q_notes
                    })
                    
                    if 'transactions' not in m_cash:
                        m_cash['transactions'] = []
                    main_trans = m_cash['transactions']
                    main_trans.append({
                        'id': len(main_trans) + 1,
                        'code': f"REC-TRF-{(len(main_trans) + 1):03d}",
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'type': 'سند قبض',
                        'party': f"استلام نقدية محولة من عُهدة المحاسب (omar)",
                        'amount': q_amt,
                        'method': q_method,
                        'notes': q_notes
                    })
                    m_cash['transactions'] = main_trans

                else:
                    rec_count = sum(1 for t in c_trans if "قبض" in t['type'])
                    pay_count = sum(1 for t in c_trans if "صرف" in t['type'])
                    v_code = f"REC-{(rec_count + 1):03d}" if "قبض" in q_type else f"PAY-{(pay_count + 1):03d}"
                    
                    c_trans.append({
                        'id': len(c_trans) + 1,
                        'code': v_code,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'type': q_type,
                        'party': q_party,
                        'amount': q_amt,
                        'method': q_method,
                        'notes': q_notes
                    })

                m_cash[box_key] = c_trans
                all_cash[month_name] = m_cash
                save_cash_data(all_cash)
                st.success(f"تم الحفظ السحابي بنجاح برقم #{v_code}!")
                st.rerun()

@st.dialog("طباعة سند الصندوق A4")
def print_cash_voucher_dialog(trans_item, month_name):
    st.write(f"معاينة السند رقم: **#{trans_item.get('code', trans_item['id'])}**")
    amt_val = trans_item['amount']
    t_type = trans_item['type']
    party_label = "استلمنا من السيد / الشركَة:" if "قبض" in t_type else "تم الصرف للسيد / الشركَة:"
    
    html_v = f"""
    <!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fff; margin: 0; padding: 5px; }}
        .voucher-box {{ border: 2px solid #1E3A8A; border-radius: 8px; padding: 12px; background: #fff; }}
        .header-logo {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 5px; }}
        .v-title {{ text-align: center; font-size: 18px; font-weight: bold; color: #1E3A8A; background: #f1f5f9; padding: 6px; margin: 8px 0; border-radius: 4px; }}
        .v-table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        .v-table td, .v-table th {{ border: 1px solid #cbd5e1; padding: 8px; text-align: right; font-size: 13px; }}
        .amt-tag {{ font-size: 18px; font-weight: bold; color: #047857; background: #ecfdf5; border: 2px solid #10b981; text-align: center; padding: 4px; border-radius: 4px; }}
        .sigs {{ margin-top: 25px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }}
    </style></head><body>
        <div class="voucher-box">
            <div class="header-logo">
                <div style="font-size:11px; font-weight:bold;">Five-M Company For Industry<br>C. R. : 1011145035</div>
                <div style="font-size:38px; font-weight:900; color:#DC2626; font-family:Arial;">5M</div>
                <div style="font-size:11px; font-weight:bold;">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
            </div>
            <div class="v-title">{t_type} | رقم السند: #{trans_item.get('code', trans_item['id'])}</div>
            <table class="v-table">
                <tr><th>التاريخ والتوقيت</th><td style="font-size:14px; font-weight:bold;">{trans_item['date']}</td><th>طريقة السداد</th><td><strong>{trans_item['method']}</strong></td></tr>
                <tr><th>{party_label}</th><td colspan="3"><strong style="font-size:16px; color:#1E3A8A;">{trans_item['party']}</strong></td></tr>
                <tr><th>المبلغ المسدد بالسند</th><td colspan="3"><div class="amt-tag">{amt_val:,.2f} ريال سعودي</div></td></tr>
                <tr><th>البيان والملاحظات</th><td colspan="3" style="font-size:13px;">{trans_item.get('notes', 'سداد بموجب السند المعمد بالنظام')}</td></tr>
            </table>
            <div class="sigs">
                <div>توقيع المستلم / الجهة: __________________</div>
                <div>توقيع أمين الصندوق / المحاسب: __________________</div>
            </div>
        </div>
    </body></html>
    """
    st.components.v1.html(html_v, height=310, scrolling=True)
    st.download_button(
        label="📄 تنزيل السند المباشر للطباعة (HTML / PDF)",
        data=html_v.encode('utf-8'),
        file_name=f"سند_{trans_item.get('code', trans_item['id'])}_{month_name}.html",
        mime="text/html",
        use_container_width=True
    )

def generate_t_account_html(trans_list, month_name, period_label, target_box_label):
    rec_list = [t for t in trans_list if "قبض" in t['type']]
    pay_list = [t for t in trans_list if "صرف" in t['type']]
    
    tot_rec = sum(t['amount'] for t in rec_list)
    tot_pay = sum(t['amount'] for t in pay_list)
    net_bal = tot_rec - tot_pay

    max_len = max(len(rec_list), len(pay_list))

    rows_html = ""
    for i in range(max_len):
        r_item = rec_list[i] if i < len(rec_list) else None
        p_item = pay_list[i] if i < len(pay_list) else None

        r_code = f"#{r_item.get('code', r_item['id'])}" if r_item else ""
        r_party = r_item['party'] if r_item else ""
        r_method = r_item['method'] if r_item else ""
        r_amt = f"{r_item['amount']:,.2f}" if r_item else ""

        p_code = f"#{p_item.get('code', p_item['id'])}" if p_item else ""
        p_party = p_item['party'] if p_item else ""
        p_method = p_item['method'] if p_item else ""
        p_amt = f"{p_item['amount']:,.2f}" if p_item else ""

        rows_html += f"""
        <tr>
            <td style="color:#047857; font-weight:bold;">{r_code}</td>
            <td style="text-align:right;">{r_party}</td>
            <td>{r_method}</td>
            <td style="color:#047857; font-weight:bold;">{r_amt}</td>
            <td style="border-right:2px solid #1E3A8A; color:#b91c1c; font-weight:bold;">{p_code}</td>
            <td style="text-align:right;">{p_party}</td>
            <td>{p_method}</td>
            <td style="color:#b91c1c; font-weight:bold;">{p_amt}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fff; margin: 0; padding: 10px; }}
        .t-box {{ border: 3px solid #1E3A8A; border-radius: 10px; padding: 15px; background: #fff; }}
        .header-logo {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 8px; }}
        .t-title {{ text-align: center; font-size: 18px; font-weight: bold; color: #1E3A8A; background: #f1f5f9; padding: 8px; margin: 10px 0; border-radius: 6px; }}
        .t-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }}
        .t-table th {{ background-color: #1E3A8A; color: white; padding: 8px; border: 1px solid #334155; text-align: center; }}
        .t-table td {{ border: 1px solid #cbd5e1; padding: 6px; text-align: center; }}
        .tot-row {{ background-color: #f8fafc; font-weight: bold; font-size: 13px; }}
        .net-summary {{ text-align: center; background: #ecfdf5; border: 2px solid #10b981; color: #047857; font-size: 16px; font-weight: bold; padding: 8px; border-radius: 6px; margin-top: 15px; }}
        .sigs {{ margin-top: 35px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }}
    </style></head><body>
        <div class="t-box">
            <div class="header-logo">
                <div style="font-size:11px; font-weight:bold;">Five-M Company For Industry<br>C. R. : 1011145035</div>
                <div style="font-size:40px; font-weight:900; color:#DC2626; font-family:Arial;">5M</div>
                <div style="font-size:11px; font-weight:bold;">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
            </div>
            <div class="v-title t-title">كشف حساب حركة الصندوق المقابل (T-Account) - {target_box_label}<br>عن الفترة: {period_label} | شهر ({month_name})</div>
            <table class="t-table">
                <thead>
                    <tr>
                        <th colspan="4" style="background:#047857;">🟢 المقبوضات</th>
                        <th colspan="4" style="background:#b91c1c; border-right:2px solid #fff;">🔴 المصروفات</th>
                    </tr>
                    <tr>
                        <th>رقم السند</th><th>البيان / الجهة</th><th>طريقة السداد</th><th>المبلغ</th>
                        <th style="border-right:2px solid #1E3A8A;">رقم السند</th><th>البيان / الجهة</th><th>طريقة السداد</th><th>المبلغ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="tot-row">
                        <td colspan="3" style="text-align:left;">إجمالي المقبوضات:</td>
                        <td style="color:#047857;">{tot_rec:,.2f} ر.س</td>
                        <td colspan="3" style="border-right:2px solid #1E3A8A; text-align:left;">إجمالي المصروفات:</td>
                        <td style="color:#b91c1c;">{tot_pay:,.2f} ر.س</td>
                    </tr>
                </tbody>
            </table>
            <div class="net-summary">
                💵 صافي الرصيد المتبقي بالصندوق في نهاية الفترة: ({net_bal:,.2f} ريال سعودي)
            </div>
            <div class="sigs">
                <div>توقيع أمين الصندوق / المحاسب: __________________</div>
                <div>توقيع المراجع / المدير العام: __________________</div>
            </div>
        </div>
    </body></html>
    """

@st.dialog("🖨️ معاينة وتنزيل كشف حساب الصندوق المقابل (T-Account)")
def print_t_account_dialog(trans_list, month_name, period_label, target_box_label):
    html_content = generate_t_account_html(trans_list, month_name, period_label, target_box_label)
    st.components.v1.html(html_content, height=380, scrolling=True)
    st.download_button(
        label="📄 تنزيل كشف الحساب المقابل المباشر للطباعة (HTML / PDF)",
        data=html_content.encode('utf-8'),
        file_name=f"كشف_حساب_الصندوق_{month_name}.html",
        mime="text/html",
        use_container_width=True
    )

@st.dialog("✏️ تعديل عُهدة سائق")
def edit_driver_custody_modal(item_idx):
    drivers_db = load_drivers_data()
    if item_idx < len(drivers_db):
        curr_d = drivers_db[item_idx]
        st.write(f"تعديل العُهدة رقم: **#{curr_d['id']} - السائق: {curr_d['driver']}**")
        with st.form("edit_driver_custody_form"):
            e_given = st.number_input("المبلغ المسلم للعُهدة (ر.س):", min_value=0.0, value=float(curr_d['given_amt']))
            e_spent = st.number_input("المصروف بالفواتير (ر.س):", min_value=0.0, value=float(curr_d.get('spent_amt', 0.0)))
            e_purpose = st.text_input("الغرض والبيان:", value=curr_d.get('purpose', ''))
            e_status = st.selectbox("حالة العُهدة:", ["مفتوحة", "تمت التصفية"], index=0 if curr_d['status'] == "مفتوحة" else 1)
            
            sub_e_driver = st.form_submit_button("💾 حفظ التعديلات")
            if sub_e_driver:
                drivers_db[item_idx]['given_amt'] = e_given
                drivers_db[item_idx]['spent_amt'] = e_spent
                drivers_db[item_idx]['diff_amt'] = e_given - e_spent
                drivers_db[item_idx]['purpose'] = e_purpose
                drivers_db[item_idx]['status'] = e_status
                save_drivers_data(drivers_db)
                st.success("تم تعديل بيانات عُهدة السائق سحابياً بنجاح!")
                st.rerun()

@st.dialog("إضافة موظف جديد")
def add_employee_dialog(default_branch):
    st.write(f"إضافة موظف لفرع: **{default_branch}**")
    with st.form("add_emp_modal_form"):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("اسم الموظف الثلاثي:")
            new_job = st.text_input("الوظيفة:", "عامل")
            new_branch = st.selectbox("الفرع:", ['مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'], index=['مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'].index(default_branch))
        with c2:
            new_sal = st.number_input("الراتب الأساسي (ر.س):", min_value=0.0, value=2500.0)
            new_start = st.date_input("تاريخ بداية العمل:", datetime(2024, 1, 1))
            new_iq = st.date_input("تاريخ انتهاء الإقامة:", datetime(2027, 12, 31))
            new_ct = st.date_input("تاريخ انتهاء العقد:", datetime(2027, 12, 31))
            
        sub_btn = st.form_submit_button("حفظ وإضافة الموظف")
        if sub_btn:
            if new_name:
                max_id = st.session_state.payroll_df['م'].max() + 1 if not st.session_state.payroll_df.empty else 1
                new_dict = {
                    'م': max_id,
                    'الاسم': new_name,
                    'الوظيفة': new_job,
                    'الراتب الأساسي': new_sal,
                    'الفرع': new_branch,
                    'تاريخ بداية العمل': str(new_start),
                    'تاريخ انتهاء الإقامة': str(new_iq),
                    'تاريخ انتهاء العقد': str(new_ct),
                    'الخصومات': 0.0,
                    'الدفعة 1': new_sal / 2.0,
                    'الدفعة 2': new_sal / 2.0,
                    'الدفعة المدفوعة': new_sal,
                    'المتبقي': 0.0,
                    'نوع الإجراء': 'صرف كامل',
                    'الملاحظات': ''
                }
                st.session_state.payroll_df = pd.concat([st.session_state.payroll_df, pd.DataFrame([new_dict])], ignore_index=True)
                save_payroll_for_month(st.session_state.payroll_df, st.session_state.current_active_month)
                st.success(f"تمت إضافة ({new_name}) بنجاح!")
                st.rerun()

@st.dialog("تعديل ملف الموظف")
def edit_employee_dialog(emp_idx, month_selected):
    emp_data = st.session_state.payroll_df.loc[emp_idx]
    st.write(f"تعديل الموظف: **{emp_data['الاسم']}** (كود: #{emp_data['م']})")
    
    with st.form(f'edit_modal_{emp_data["م"]}'):
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.markdown("### البيانات الإدارية")
            up_name = st.text_input("اسم الموظف الثلاثي:", value=emp_data['الاسم'])
            up_job = st.text_input("الوظيفة:", value=emp_data['الوظيفة'])
            up_branch = st.selectbox("الفرع التابع له:", [
                'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'
            ], index=['مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'].index(emp_data['الفرع']))
            
        with col_e2:
            st.markdown("### المالية (" + month_selected + ")")
            up_salary = st.number_input("الراتب الأساسي (ر.س):", min_value=0.0, value=float(emp_data['الراتب الأساسي']))
            up_pay1 = st.number_input("الدفعة 1 (ر.س):", min_value=0.0, value=float(emp_data.get('الدفعة 1', 0)))
            up_pay2 = st.number_input("الدفعة 2 (ر.س):", min_value=0.0, value=float(emp_data.get('الدفعة 2', 0)))
            up_ded = st.number_input("الخصومات (ر.س):", min_value=0.0, value=float(emp_data.get('الخصومات', 0)))
            up_action = st.selectbox("نوع الإجراء:", ["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"], index=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"].index(emp_data['نوع الإجراء']))
            up_notes = st.text_input("الملاحظات:", value=emp_data['الملاحظات'])
            
        with col_e3:
            st.markdown("### التواريخ والوثائق")
            st_val = datetime.strptime(str(emp_data.get('تاريخ بداية العمل', '2024-01-01')), '%Y-%m-%d')
            iq_val = datetime.strptime(str(emp_data['تاريخ انتهاء الإقامة']), '%Y-%m-%d') if pd.notnull(emp_data['تاريخ انتهاء الإقامة']) else datetime(2027, 12, 31)
            ct_val = datetime.strptime(str(emp_data['تاريخ انتهاء العقد']), '%Y-%m-%d') if pd.notnull(emp_data['تاريخ انتهاء العقد']) else datetime(2027, 12, 31)
            
            up_start_date = st.date_input("تاريخ بداية العمل:", st_val)
            up_iqama_date = st.date_input("تاريخ انتهاء الإقامة:", iq_val)
            up_contract_date = st.date_input("تاريخ انتهاء العقد:", ct_val)
            
        st.divider()
        save_btn = st.form_submit_button('حفظ وتحديث البيانات')
        
        if save_btn:
            tot_paid_emp = up_pay1 + up_pay2
            st.session_state.payroll_df.loc[emp_idx, 'الاسم'] = up_name
            st.session_state.payroll_df.loc[emp_idx, 'الوظيفة'] = up_job
            st.session_state.payroll_df.loc[emp_idx, 'الفرع'] = up_branch
            st.session_state.payroll_df.loc[emp_idx, 'الراتب الأساسي'] = up_salary
            st.session_state.payroll_df.loc[emp_idx, 'الخصومات'] = up_ded
            st.session_state.payroll_df.loc[emp_idx, 'الدفعة 1'] = up_pay1
            st.session_state.payroll_df.loc[emp_idx, 'الدفعة 2'] = up_pay2
            st.session_state.payroll_df.loc[emp_idx, 'الدفعة المدفوعة'] = tot_paid_emp
            st.session_state.payroll_df.loc[emp_idx, 'المتبقي'] = up_salary - (tot_paid_emp + up_ded)
            st.session_state.payroll_df.loc[emp_idx, 'نوع الإجراء'] = up_action
            st.session_state.payroll_df.loc[emp_idx, 'الملاحظات'] = up_notes
            st.session_state.payroll_df.loc[emp_idx, 'تاريخ بداية العمل'] = str(up_start_date)
            st.session_state.payroll_df.loc[emp_idx, 'تاريخ انتهاء الإقامة'] = str(up_iqama_date)
            st.session_state.payroll_df.loc[emp_idx, 'تاريخ انتهاء العقد'] = str(up_contract_date)
            
            save_payroll_for_month(st.session_state.payroll_df, month_selected)
            st.success("تم الحفظ بنجاح!")
            st.rerun()

    with st.expander(f"حذف الموظف ({emp_data['الاسم']})"):
        if st.button(f"تأكيد الحذف النهائياً", key=f"del_modal_{emp_data['م']}"):
            st.session_state.payroll_df = st.session_state.payroll_df.drop(emp_idx).reset_index(drop=True)
            save_payroll_for_month(st.session_state.payroll_df, month_selected)
            st.success("تم الحذف!")
            st.rerun()

# 2. الشاشة الافتتاحية الملكية بكلمة المرور المشددة
if not st.session_state.get('app_started', False):
    st.markdown("""
        <div class="welcome-card-lux">
            <div class="logo-lux">5M</div>
            <div class="title-company-royal">شركة ميم الخماسية للتصنيع</div>
            <p style="color: #94A3B8 !important; font-size: 17px; margin-bottom: 20px;">النظام المحاسبي والإداري الموحد</p>
            <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.2); margin: 25px 0;">
        </div>
    """, unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1])
    with col_b2:
        st.markdown("<h3 style='text-align:center;'>تسجيل الدخول:</h3>", unsafe_allow_html=True)
        
        username_selected = st.selectbox("المستخدم:", ["wahby", "omar"], key="login_username_select")
        pwd_input = st.text_input("كلمة المرور المطلوبة:", type="password", key="login_pwd")
        
        if st.button('الدخول للنظام', use_container_width=True):
            if username_selected == "wahby" and pwd_input == ADMIN_PASSWORD:
                st.session_state.app_started = True
                st.session_state.user_role = "admin"
                st.success("أهلاً بك (wahby)!")
                st.rerun()
            elif username_selected == "omar" and pwd_input == USER_PASSWORD:
                st.session_state.app_started = True
                st.session_state.user_role = "accountant"
                st.success("أهلاً بك (omar)!")
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة! يرجى إدخال كلمة المرور للوصول للنظام.")

else:
    # 3. القائمة الجانبية المباشرة
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-logo-card">
                <div class="sidebar-logo-text">5M</div>
                <div class="sidebar-company-title">شركة ميم الخماسية للتصنيع</div>
            </div>
        """, unsafe_allow_html=True)

        role_label = "wahby" if st.session_state.user_role == "admin" else "omar"
        st.info(f"المستخدم: {role_label}")

        if 'months_list' not in st.session_state:
            st.session_state.months_list = ['أغسطس 2026', 'سبتمبر 2026', 'أكتوبر 2026', 'نوفمبر 2026', 'ديسمبر 2026']
            
        saved_last_month = load_last_selected_month()
        default_m_index = st.session_state.months_list.index(saved_last_month) if saved_last_month in st.session_state.months_list else 0

        month_selected = st.selectbox('الشهر الحالي:', st.session_state.months_list, index=default_m_index)

        if month_selected != saved_last_month:
            save_last_selected_month(month_selected)

        st.session_state['theme_mode'] = st.selectbox("نمط الألوان:", ["🌙 وضع ليلي", "☀️ وضع نهاري"], index=0 if "🌙" in st.session_state['theme_mode'] else 1)

        st.divider()

        # 1. زر الرئيسية المباشر الخارجي المميز
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state['current_view'] = 'الرئيسية'
            st.rerun()

        # 2. قسم الخزائن والصناديق
        st.markdown('<div class="sidebar-section-title">🏦 الخزائن والصناديق</div>', unsafe_allow_html=True)
        if st.button("حركة الصندوق", use_container_width=True):
            st.session_state['current_view'] = 'حركة الصندوق'
            st.rerun()
        if st.button("عُهدة السواقين", use_container_width=True):
            st.session_state['current_view'] = 'عُهدة السواقين'
            st.rerun()
        if st.button("جرد الخزينة", use_container_width=True):
            st.session_state['current_view'] = 'جرد الخزينة'
            st.rerun()

        # 3. قسم إدارة الرواتب والدفعات
        if st.session_state.user_role == "admin":
            st.markdown('<div class="sidebar-section-title">📊 إدارة الرواتب والدفعات</div>', unsafe_allow_html=True)
            if st.button("إدخال الدفعات", use_container_width=True):
                st.session_state['current_view'] = 'إدخال الدفعات'
                st.rerun()
            if st.button("كشف مسير الرواتب", use_container_width=True):
                st.session_state['current_view'] = 'مسير الرواتب'
                st.rerun()
            if st.button("🖨️ طباعة سندات الرواتب A4", use_container_width=True):
                st.session_state['current_view'] = 'طباعة السندات'
                st.rerun()

            # 4. قسم الموارد البشرية HR
            st.markdown('<div class="sidebar-section-title">👤 الموارد البشرية (HR)</div>', unsafe_allow_html=True)
            if st.button("دليل الموظفين", use_container_width=True):
                st.session_state['current_view'] = 'دليل الموظفين'
                st.rerun()
            if st.button("حاسبة نهاية الخدمة", use_container_width=True):
                st.session_state['current_view'] = 'حاسبة الخدمة'
                st.rerun()
            if st.button("التنبيهات الإدارية", use_container_width=True):
                st.session_state['current_view'] = 'التنبيهات'
                st.rerun()

            # 5. قسم النظام والأرشيف
            st.markdown('<div class="sidebar-section-title">⚙️ أدوات النظام والأرشيف</div>', unsafe_allow_html=True)
            if st.button("النسخ الاحتياطي", use_container_width=True):
                st.session_state['current_view'] = 'النسخ الاحتياطي'
                st.rerun()
            if st.button("الإغلاق السنوي", use_container_width=True):
                st.session_state['current_view'] = 'الإغلاق السنوي'
                st.rerun()

        st.divider()

        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.app_started = False
            st.session_state.user_role = None
            st.rerun()

        selected_option = st.session_state.get('current_view', 'الرئيسية')

    st.session_state.payroll_df = get_payroll_for_month(month_selected)
    st.session_state.current_active_month = month_selected

    tot_emp = len(st.session_state.payroll_df)
    tot_req = st.session_state.payroll_df['الراتب الأساسي'].sum()
    tot_p1_all = st.session_state.payroll_df['الدفعة 1'].sum()
    tot_p2_all = st.session_state.payroll_df['الدفعة 2'].sum()
    tot_ded_all = st.session_state.payroll_df['الخصومات'].sum()
    tot_paid = st.session_state.payroll_df['الدفعة المدفوعة'].sum()
    tot_rem = st.session_state.payroll_df['المتبقي'].sum()

    now_dt = datetime.now()
    days_ar = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
    months_ar = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    
    day_name = days_ar[(now_dt.weekday() + 1) % 7]
    date_formatted = f"📅 {day_name}، {now_dt.day} {months_ar[now_dt.month - 1]} {now_dt.year}"

    # الشريحة العلوية المباشرة
    st.markdown(f"""
        <div class="company-header-inner">
            <div class="date-badge-lux">{date_formatted}</div>
            <h1 class="company-header-inner-title">🏢 شركة ميم الخماسية للتصنيع</h1>
            <p class="company-header-inner-sub">النظام المحاسبي والإداري الموحد</p>
        </div>
    """, unsafe_allow_html=True)

    def generate_pretty_html_pdf(df_subset, branch_name, payment_type="جميع الدفعات"):
        output = io.BytesIO()
        html = f"""
        <!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
        <style>
            @page {{ size: A4 portrait; margin: 8mm; }}
            body {{ font-family: Arial, sans-serif; background-color: #fff; margin: 0; }}
            .page {{ height: 275mm; page-break-after: always; display: flex; flex-direction: column; justify-content: space-between; }}
            .voucher-box {{ border: 2px solid #1E3A8A; border-radius: 8px; padding: 12px 18px; height: 128mm; box-sizing: border-box; }}
            .header-logo-container {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 6px; }}
            .header-en {{ text-align: left; font-size: 11px; color: #1E3A8A; font-weight: bold; width: 38%; }}
            .header-logo {{ text-align: center; width: 24%; font-size: 38px; font-weight: 900; color: #DC2626; }}
            .header-ar {{ text-align: right; font-size: 12px; color: #1E3A8A; font-weight: bold; width: 38%; }}
            .voucher-title {{ text-align: center; font-size: 15px; font-weight: bold; color: #1E3A8A; margin: 6px 0; background: #f1f5f9; padding: 5px; }}
            .info-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
            .info-table td, .info-table th {{ padding: 8px; font-size: 13px; border: 1px solid #cbd5e1; text-align: right; }}
            .info-table th {{ background-color: #f8fafc; color: #1E3A8A; }}
            .amount-box {{ background-color: #ecfdf5; border: 2px solid #10b981; color: #047857; font-size: 16px; font-weight: bold; text-align: center; padding: 4px; border-radius: 4px; }}
            .signatures {{ margin-top: 20px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; }}
            .cut-line {{ border-top: 2px dashed #94a3b8; text-align: center; margin: 4mm 0; }}
        </style></head><body>
        """
        rows = [row for _, row in df_subset.iterrows()]
        for i in range(0, len(rows), 2):
            html += '<div class="page">'
            v1 = rows[i]
            
            if payment_type == "الدفعة الأولى فقط":
                amt_str = f"{v1.get('الدفعة 1', 0):,.0f} ر.س"
                rem_str = f"{(v1['الراتب الأساسي'] - v1.get('الدفعة 1', 0)):,.0f} ر.س"
                note_str = f"سداد الدفعة الأولى من راتب شهر ({month_selected})"
            elif payment_type == "الدفعة الثانية فقط":
                amt_str = f"{v1.get('الدفعة 2', 0):,.0f} ر.س"
                rem_str = f"{(v1['الراتب الأساسي'] - (v1.get('الدفعة 1', 0) + v1.get('الدفعة 2', 0))):,.0f} ر.س"
                note_str = f"سداد الدفعة الثانية والنهائية من راتب شهر ({month_selected})"
            else:
                amt_str = f"{v1['الدفعة المدفوعة']:,.0f} ر.س"
                rem_str = f"{v1['المتبقي']:,.0f} ر.س"
                note_str = f"سداد إجمالي دفعات راتب شهر ({month_selected})"

            html += f"""
            <div class="voucher-box">
                <div class="header-logo-container">
                    <div class="header-en">Five-M Company For Industry<br>C. R. : 1011145035</div>
                    <div class="header-logo">5M</div>
                    <div class="header-ar">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
                </div>
                <div class="voucher-title">سند صرف {payment_type} - شهر ({month_selected}) | رقم السند: #{v1['م']:03d}</div>
                <table class="info-table">
                    <tr><th>اسم الموظف</th><td><strong>{v1['الاسم']}</strong></td><th>الفرع المحدد</th><td><strong>{v1['الفرع']}</strong></td></tr>
                    <tr><th>الراتب الأساسي</th><td>{v1['الراتب الأساسي']:,.0f} ر.س</td><th>تفاصيل الدفعات المسجلة</th><td>دفعة (1): {v1['الدفعة 1']:,.0f} ر.س | دفعة (2): {v1['الدفعة 2']:,.0f} ر.س</td></tr>
                    <tr><th>المبلغ المصروف بهذا السند</th><td><div class="amount-box">{amt_str}</div></td><th>المتبقي بالرصيد</th><td style="color:red; font-weight:bold;">{rem_str}</td></tr>
                    <tr><th>البيان والملاحظات</th><td colspan="3">{note_str}</td></tr>
                </table>
                <div class="signatures"><div>توقيع واستلام الموظف: __________________</div><div>اعتماد المحاسب / الإدارة: __________________</div></div>
            </div>
            """
            if i + 1 < len(rows):
                v2 = rows[i + 1]
                if payment_type == "الدفعة الأولى فقط":
                    amt_str2 = f"{v2.get('الدفعة 1', 0):,.0f} ر.س"
                    rem_str2 = f"{(v2['الراتب الأساسي'] - v2.get('الدفعة 1', 0)):,.0f} ر.س"
                    note_str2 = f"سداد الدفعة الأولى من راتب شهر ({month_selected})"
                elif payment_type == "الدفعة الثانية فقط":
                    amt_str2 = f"{v2.get('الدفعة 2', 0):,.0f} ر.س"
                    rem_str2 = f"{(v2['الراتب الأساسي'] - (v2.get('الدفعة 1', 0) + v2.get('الدفعة 2', 0))):,.0f} ر.س"
                    note_str2 = f"سداد الدفعة الثانية والنهائية من راتب شهر ({month_selected})"
                else:
                    amt_str2 = f"{v2['الدفعة المدفوعة']:,.0f} ر.س"
                    rem_str2 = f"{v2['المتبقي']:,.0f} ر.س"
                    note_str2 = f"سداد إجمالي دفعات راتب شهر ({month_selected})"

                html += '<div class="cut-line"><span>✂️ خط القص المخصص بين السندين ✂️</span></div>'
                html += f"""
                <div class="voucher-box">
                    <div class="header-logo-container">
                        <div class="header-en">Five-M Company For Industry<br>C. R. : 1011145035</div>
                        <div class="header-logo">5M</div>
                        <div class="header-ar">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
                    </div>
                    <div class="voucher-title">سند صرف {payment_type} - شهر ({month_selected}) | رقم السند: #{v2['م']:03d}</div>
                    <table class="info-table">
                        <tr><th>اسم الموظف</th><td><strong>{v2['الاسم']}</strong></td><th>الفرع المحدد</th><td><strong>{v2['الفرع']}</strong></td></tr>
                        <tr><th>الراتب الأساسي</th><td>{v2['الراتب الأساسي']:,.0f} ر.س</td><th>تفاصيل الدفعات المسجلة</th><td>دفعة (1): {v2['الدفعة 1']:,.0f} ر.س | دفعة (2): {v2['الدفعة 2']:,.0f} ر.س</td></tr>
                        <tr><th>المبلغ المصروف بهذا السند</th><td><div class="amount-box">{amt_str2}</div></td><th>المتبقي بالرصيد</th><td style="color:red; font-weight:bold;">{rem_str2}</td></tr>
                        <tr><th>البيان والملاحظات</th><td colspan="3">{note_str2}</td></tr>
                    </table>
                    <div class="signatures"><div>توقيع واستلام الموظف: __________________</div><div>اعتماد المحاسب / الإدارة: __________________</div></div>
                </div>
                """
            html += '</div>'
        html += "</body></html>"
        output.write(html.encode('utf-8'))
        output.seek(0)
        return output

    # 4. الواجهة الرئيسية
    if selected_option == 'الرئيسية':
        all_cash_db = load_cash_data()
        current_m_cash = all_cash_db.get(month_selected, {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []})
        
        curr_trans_main = current_m_cash.get('transactions', [])
        tot_in_main = sum(t['amount'] for t in curr_trans_main if 'قبض' in t['type'])
        tot_out_main = sum(t['amount'] for t in curr_trans_main if 'صرف' in t['type'])
        net_main_now = current_m_cash.get('opening', 0.0) + tot_in_main - tot_out_main

        curr_trans_acc = current_m_cash.get('acc_transactions', [])
        tot_in_acc = sum(t['amount'] for t in curr_trans_acc if 'قبض' in t['type'])
        tot_out_acc = sum(t['amount'] for t in curr_trans_acc if 'صرف' in t['type'])
        net_acc_now = current_m_cash.get('acc_opening', 0.0) + tot_in_acc - tot_out_acc

        total_company_cash = net_main_now + net_acc_now

        drivers_db = load_drivers_data()
        tot_given_drivers = sum(d['given_amt'] for d in drivers_db)
        tot_spent_drivers = sum(d['spent_amt'] for d in drivers_db)
        open_driver_custody_sum = max(0.0, tot_given_drivers - tot_spent_drivers)

        audit_history = load_audit_data()
        last_audit = audit_history[-1] if audit_history else None

        st.markdown(f"### ملخص الصندوق والعُهد - {month_selected}")
        
        if st.session_state.user_role == "admin":
            c_box1, c_box2, c_box3, c_box4 = st.columns(4)
            with c_box1:
                st.markdown("#### الخزينة الرئيسية (wahby):")
                st.metric("رصيد الخزينة الرئيسية", f"{net_main_now:,.2f} ر.س")
            with c_box2:
                st.markdown("#### عُهدة المحاسب (omar):")
                st.metric("رصيد عُهدة omar", f"{net_acc_now:,.2f} ر.س")
            with c_box3:
                st.markdown("#### 🚚 عُهد السائقين المترصدة:")
                st.metric("إجمالي المتبقي باليد", f"{open_driver_custody_sum:,.2f} ر.س")
            with c_box4:
                st.markdown("#### 💳 إجمالي نقدية الشركة:")
                st.metric("مجموع الصناديق", f"{total_company_cash:,.2f} ر.س")

            if last_audit:
                a_diff = last_audit['diff']
                diff_tag = "🟢 مطابقة تامة" if a_diff == 0 else (f"🔴 عجز بقيمة ({abs(a_diff):,.2f} ر.س)" if a_diff < 0 else f"🔵 زيادة بقيمة ({a_diff:,.2f} ر.س)")
                st.info(f"🔍 **آخر جرد معتمد للصندوق ({last_audit['box_name']}):** بتاريخ **{last_audit['date']}** | حالة الجرد: **{diff_tag}** | ملاحظات: {last_audit.get('notes', 'لا يوجد')}")

            st.markdown("### مؤشرات الرواتب والعمالة")
            st_col1, st_col2, st_col3, st_col4, st_col5, st_col6 = st.columns(6)
            st_col1.metric("العمالة", f"{tot_emp} موظف")
            st_col2.metric("الرواتب", f"{tot_req:,.0f} ر.س")
            st_col3.metric("الدفعة 1", f"{tot_p1_all:,.0f} ر.س")
            st_col4.metric("الدفعة 2", f"{tot_p2_all:,.0f} ر.س")
            st_col5.metric("الخصومات", f"{tot_ded_all:,.0f} ر.س")
            st_col6.metric("المتبقي", f"{tot_rem:,.0f} ر.س")

            st.markdown("### ⚡ إجراءات خاطفة وسريعة (لوحة wahby)")
            q_col1, q_col2, q_col3, q_col4, q_col5, q_col6, q_col7 = st.columns(7)
            
            with q_col1:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("👤 إضافة موظف", key="q_btn_add_emp", use_container_width=True):
                    add_employee_dialog('مصنع ميم الخماسية الخرج')
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col2:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🔄 تحويل عُهدة", key="q_btn_trf_cash", use_container_width=True):
                    quick_cash_voucher_dialog("تحويل عُهدة إلى (omar)", month_selected, "main")
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col3:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🟢 سند قبض", key="q_btn_rec", use_container_width=True):
                    quick_cash_voucher_dialog("قبض", month_selected, "main")
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col4:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🔴 سند صرف", key="q_btn_pay", use_container_width=True):
                    quick_cash_voucher_dialog("صرف", month_selected, "main")
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col5:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🚚 السائقين", key="q_btn_driver_page", use_container_width=True):
                    st.session_state['current_view'] = 'عُهدة السواقين'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col6:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🔍 الجرد", key="q_btn_audit_page", use_container_width=True):
                    st.session_state['current_view'] = 'جرد الخزينة'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col7:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("💾 الأرشيف", key="q_btn_backup_page", use_container_width=True):
                    st.session_state['current_view'] = 'النسخ الاحتياطي'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            c_box1, c_box2 = st.columns(2)
            with c_box1:
                st.markdown("#### عُهدتك الحالية (omar):")
                st.metric("الرصيد المتبقي بعُهدتك", f"{net_acc_now:,.2f} ر.س")
            with c_box2:
                st.markdown("#### 🚚 عُهد السائقين المترصدة:")
                st.metric("إجمالي المتبقي باليد", f"{open_driver_custody_sum:,.2f} ر.س")

            st.markdown("### ⚡ إجراءات خاطفة وسريعة (لوحة omar)")
            q_col1, q_col2, q_col3, q_col4 = st.columns(4)
            with q_col1:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🟢 سند قبض", use_container_width=True, key="q_btn_rec_acc"):
                    quick_cash_voucher_dialog("قبض", month_selected, "accountant")
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col2:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🔴 سند صرف", use_container_width=True, key="q_btn_pay_acc"):
                    quick_cash_voucher_dialog("صرف", month_selected, "accountant")
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col3:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🚚 تصفية السائقين", use_container_width=True, key="q_btn_driver_page_acc"):
                    st.session_state['current_view'] = 'عُهدة السواقين'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with q_col4:
                st.markdown('<div class="daftra-btn-container">', unsafe_allow_html=True)
                if st.button("🔍 جرد الخزينة", use_container_width=True, key="q_btn_audit_acc"):
                    st.session_state['current_view'] = 'جرد الخزينة'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # 5. موديول عُهدة السواقين
    elif selected_option == 'عُهدة السواقين':
        st.subheader(f'🚚 موديول إدارة عُهدة السواقين المباشر - ({month_selected})')
        st.write('يتيح هذا الموديول تسليم العُهد الموقتة للسائق **(سمان السواق)** وتصفية الفواتير والتسميع التراكمي المباشر بصندوق omar:')

        drivers_db = load_drivers_data()
        driver_selected = "سمان السواق"

        tot_given_drivers = sum(d['given_amt'] for d in drivers_db)
        tot_spent_drivers = sum(d['spent_amt'] for d in drivers_db)
        open_driver_custody_sum = max(0.0, tot_given_drivers - tot_spent_drivers)

        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("إجمالي العُهد المسلمة لـ سمان السواق", f"{tot_given_drivers:,.2f} ر.س")
        sc2.metric("إجمالي المصروفات المصفاة بالفواتير", f"{tot_spent_drivers:,.2f} ر.س")
        sc3.metric("🔴 المتبقي بذمته فعلياً للآن", f"{open_driver_custody_sum:,.2f} ر.س")

        st.divider()

        d_col1, d_col2 = st.columns([1, 1.8])
        with d_col1:
            st.markdown("### 📝 1. تسليم عُهدة جديدة لـ (سمان السواق):")
            if open_driver_custody_sum > 0:
                st.warning(f"💡 المتبقي المترصد في جيب السائق حالياً من العُهد السابقة: **{open_driver_custody_sum:,.2f} ر.س**")

            with st.form("add_driver_custody_form"):
                st.text_input("اسم السائق:", "سمان السواق", disabled=True)
                given_amt = st.number_input("المبلغ الجديد المسلم كعُهدة (ر.س):", min_value=0.0, value=0.0, step=50.0)
                purpose_txt = st.text_input("البيان / الغرض من العُهدة:", "مصاريف نقل وبنزين")
                
                sub_d = st.form_submit_button("تسليم وتأكيد العُهدة")
                if sub_d and given_amt > 0:
                    drivers_db.append({
                        'id': len(drivers_db) + 1,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'driver': driver_selected,
                        'given_amt': given_amt,
                        'purpose': purpose_txt,
                        'status': 'مفتوحة',
                        'spent_amt': 0.0,
                        'returned_amt': 0.0,
                        'diff_amt': given_amt
                    })
                    save_drivers_data(drivers_db)

                    all_cash = load_cash_data()
                    if month_selected not in all_cash:
                        all_cash[month_selected] = {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []}
                    
                    m_cash = all_cash[month_selected]
                    acc_trans = m_cash.get('acc_transactions', [])
                    acc_trans.append({
                        'id': len(acc_trans) + 1,
                        'code': f"DRV-OUT-{(len(acc_trans) + 1):03d}",
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'type': 'سند صرف',
                        'party': f"عُهدة سمان السواق",
                        'amount': given_amt,
                        'method': 'نقداً بالصندوق',
                        'notes': purpose_txt
                    })
                    m_cash['acc_transactions'] = acc_trans
                    all_cash[month_selected] = m_cash
                    save_cash_data(all_cash)

                    st.success(f"تم تسليم {given_amt:,.2f} ر.س للسائق وتوثيقها سحابياً بصندوق omar!")
                    st.rerun()

        with d_col2:
            st.markdown("### 🏁 2. تصفية عُهدة (سمان السواق) بالعودة:")
            open_custodies = [d for d in drivers_db if d['status'] == 'مفتوحة']
            
            if open_custodies:
                selected_custody_id = st.selectbox("اختر العُهدة المراد تصفيتها للعودة:", [f"#{d['id']} - {d['driver']} ({d['given_amt']} ر.س) - {d['date']}" for d in open_custodies])
                target_id = int(selected_custody_id.split('#')[1].split(' ')[0])
                target_item = [d for d in open_custodies if d['id'] == target_id][0]

                st.info(f"المبلغ المسلم بعهدته: **{target_item['given_amt']:,.2f} ر.س** | البيان: {target_item['purpose']}")
                
                spent_input_key = f"spent_inp_{target_id}"
                spent_val = st.number_input("أدخل إجمالي المصروفات والفواتير بالفعل (ر.س):", min_value=0.0, value=0.0, step=10.0, key=spent_input_key)
                settle_notes = st.text_input("تفاصيل المصروفات / أرقام الفواتير:", key=f"notes_inp_{target_id}")
                
                diff_val = target_item['given_amt'] - spent_val
                st.divider()
                if diff_val > 0:
                    st.success(f"🟢 **متبقي بجراب السائق لليوم القادم: {diff_val:,.2f} ر.س** (تترحل تلقائياً بذمته دون إعادة إدخالها للصندوق)")
                elif diff_val < 0:
                    st.error(f"🔴 **السائق صرف زيادة من جيبه يستحق ردها: ({abs(diff_val):,.2f} ر.س)**")
                else:
                    st.info("🟢 **المطابقة تامة! المصروفات تتطابق مع العُهدة.**")

                if st.button("🏁 اعتماد تصفية العُهدة وتسوية الخزينة", key=f"btn_sub_settle_{target_id}", use_container_width=True):
                    target_item['status'] = 'تمت التصفية'
                    target_item['spent_amt'] = spent_val
                    target_item['diff_amt'] = diff_val
                    target_item['settle_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    target_item['settle_notes'] = settle_notes
                    
                    save_drivers_data(drivers_db)

                    if diff_val < 0:
                        all_cash = load_cash_data()
                        if month_selected not in all_cash:
                            all_cash[month_selected] = {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []}
                        
                        m_cash = all_cash[month_selected]
                        acc_trans = m_cash.get('acc_transactions', [])
                        
                        acc_trans.append({
                            'id': len(acc_trans) + 1,
                            'code': f"DRV-REF-{(len(acc_trans) + 1):03d}",
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'type': 'سند صرف',
                            'party': f"عُهدة سمان السواق - سداد فرق مصروفات زيادة",
                            'amount': abs(diff_val),
                            'method': 'نقداً بالصندوق',
                            'notes': settle_notes
                        })

                        m_cash['acc_transactions'] = acc_trans
                        all_cash[month_selected] = m_cash
                        save_cash_data(all_cash)

                    st.success("تمت التصفية والتسميع المباشر بنجاح!")
                    st.rerun()
            else:
                st.info("لا توجد عُهد مفتوحة حالياً لـ سمان السواق بانتظار التصفية.")

        st.divider()
        st.markdown("### 📑 سجل كشف حساب وتصفية عُهد (سمان السواق):")
        if drivers_db:
            for d_idx, d_item in enumerate(reversed(drivers_db)):
                real_d_idx = drivers_db.index(d_item)
                
                col_d1, col_d2, col_d3, col_d4, col_d5, col_d6 = st.columns([0.6, 1.8, 1.5, 1.5, 0.9, 0.9])
                col_d1.write(f"#{d_item['id']}")
                col_d2.write(f"🚚 **{d_item['driver']}**\n📅 {d_item['date']}")
                col_d3.write(f"المسلم: **{d_item['given_amt']:,.2f} ر.س**\nالمصروف: **{d_item.get('spent_amt', 0.0):,.2f} ر.س**")
                
                diff_val = d_item.get('diff_amt', 0.0)
                diff_str = "🟢 تصفية كاملة" if d_item['status'] == 'تمت التصفية' and diff_val == 0 else (f"🔴 متبقي معه ({diff_val:,.2f} ر.س)" if diff_val > 0 else f"🔵 زيادة له ({abs(diff_val):,.2f} ر.س)")
                col_d4.write(f"الحالة: **{diff_str}**\n{diff_str}")
                
                if col_d5.button("✏️ تعديل", key=f"edit_drv_btn_{real_d_idx}"):
                    edit_driver_custody_modal(real_d_idx)

                if col_d6.button("🗑️ حذف", key=f"del_drv_btn_{real_d_idx}"):
                    drivers_db.pop(real_d_idx)
                    save_drivers_data(drivers_db)
                    st.success("تم حذف حركة عُهدة السائق!")
                    st.rerun()
                st.divider()
        else:
            st.info("لا يوجد سجل عُهد سابق لـ سمان السواق.")

    # 6. موديول جرد الخزينة المحدث
    elif selected_option == 'جرد الخزينة':
        st.subheader(f'🔍 موديول جرد الخزينة ومطابقة النقدية الفعلي - ({month_selected})')
        st.write('قم بمطابقة المبالغ النقدية الموجودة بيدك داخل الصندوق مع الرصيد الدفتري المسجل بالنظام واحتساب العجز أو الزيادة فوراً:')
        
        all_cash_db = load_cash_data()
        current_m_cash = all_cash_db.get(month_selected, {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []})
        
        if st.session_state.user_role == "admin":
            target_audit_box = st.radio("اختر الخزينة المراد جردها ومطابقتها الآن:", ["🏢 الخزينة الرئيسية (wahby)", "👤 عُهدة المحاسب (omar)"], horizontal=True)
        else:
            target_audit_box = "👤 عُهدة المحاسب (omar)"
            st.info("أنت تقوم الآن بـ **جرد ومطابقة الخزينة المخصصة لعُهدتك (omar)**.")

        active_box_key = 'transactions' if "wahby" in target_audit_box else 'acc_transactions'
        active_opening_key = 'opening' if "wahby" in target_audit_box else 'acc_opening'

        opening_bal = current_m_cash.get(active_opening_key, 0.0)
        curr_trans = current_m_cash.get(active_box_key, [])
        tot_cash_in = sum(t['amount'] for t in curr_trans if 'قبض' in t['type'])
        tot_cash_out = sum(t['amount'] for t in curr_trans if 'صرف' in t['type'])
        system_book_balance = opening_bal + tot_cash_in - tot_cash_out

        st.divider()

        col_aud1, col_aud2 = st.columns([1.2, 1])
        with col_aud1:
            st.markdown("### 💵 1. حاسبة مبالغ الفئات بالخزينة (بالريال):")
            st.write("أدخل **إجمالي المبلغ الموجود بيدك** لكل فئة نقدية بالريال مباشرة (مثلاً: إجمالي الـ 500 = 5000):")
            
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                v_500 = st.number_input("إجمالي فئة 500 ريال (ر.س):", min_value=0.0, value=0.0, step=500.0)
                v_200 = st.number_input("إجمالي فئة 200 ريال (ر.س):", min_value=0.0, value=0.0, step=200.0)
                v_100 = st.number_input("إجمالي فئة 100 ريال (ر.س):", min_value=0.0, value=0.0, step=100.0)
                v_50 = st.number_input("إجمالي فئة 50 ريال (ر.س):", min_value=0.0, value=0.0, step=50.0)
            with c_f2:
                v_20 = st.number_input("إجمالي فئة 20 ريال (ر.س):", min_value=0.0, value=0.0, step=20.0)
                v_10 = st.number_input("إجمالي فئة 10 ريال (ر.س):", min_value=0.0, value=0.0, step=10.0)
                v_5 = st.number_input("إجمالي فئة 5 ريال (ر.س):", min_value=0.0, value=0.0, step=5.0)
                v_coins = st.number_input("كسور / مبالغ إضافية بالريال (ر.س):", min_value=0.0, value=0.0)

            actual_counted_cash = v_500 + v_200 + v_100 + v_50 + v_20 + v_10 + v_5 + v_coins

            st.write("")
            manual_override = st.checkbox("أو كتابة المجموع الكلي الفعلي مباشرة دون تفصيل الفئات")
            if manual_override:
                actual_counted_cash = st.number_input("إجمالي النقدية الفعلية باليد كلياً (ر.س):", min_value=0.0, value=float(actual_counted_cash))

        with col_aud2:
            st.markdown("### 📊 2. نتائج المطابقة والعجز/الزيادة:")
            diff_amount = actual_counted_cash - system_book_balance

            st.metric("📖 الرصيد الدفتري المسجل بالنظام", f"{system_book_balance:,.2f} ر.س")
            st.metric("💵 إجمالي النقدية الفعلي باليد", f"{actual_counted_cash:,.2f} ر.س")

            st.divider()
            if diff_amount == 0:
                st.success("🟢 **المطابقة تامة!** النقدية الفعلية بالخزنة تتطابق 100% مع الرصيد الدفتري.")
            elif diff_amount < 0:
                st.error(f"🔴 **يوجد عجز بالخزنة بقيمة: ({abs(diff_amount):,.2f} ر.س)**")
            else:
                st.warning(f"🔵 **توجد زيادة بالخزنة بقيمة: ({diff_amount:,.2f} ر.س)**")

            audit_notes = st.text_input("ملاحظات الجرد / أسباب الفرق إن وجد:")
            if st.button("💾 اعتماد وحفظ جلسة الجرد بسجل السجلات", use_container_width=True):
                audit_records = load_audit_data()
                new_entry = {
                    'id': len(audit_records) + 1,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'month': month_selected,
                    'box_name': target_audit_box,
                    'book_bal': system_book_balance,
                    'actual_cash': actual_counted_cash,
                    'diff': diff_amount,
                    'notes': audit_notes if audit_notes else 'مطابقة معتمدة'
                }
                audit_records.append(new_entry)
                save_audit_data(audit_records)
                st.success("تم اعتماد وتوثيق الجرد بالسجلات بنجاح!")
                st.rerun()

        st.divider()
        st.markdown("### 📑 سجل تسويات وجرد الخزينة التاريخي:")
        audit_history = load_audit_data()
        if audit_history:
            for a_idx, a_item in enumerate(reversed(audit_history)):
                real_a_idx = len(audit_history) - 1 - a_idx
                col_rec1, col_rec2, col_rec3, col_rec4, col_rec5 = st.columns([1, 2, 2, 2, 1])
                col_rec1.write(f"#{a_item['id']}")
                col_rec2.write(f"📅 **{a_item['date']}**\n{a_item['box_name']}")
                
                diff_val = a_item['diff']
                diff_str = "🟢 مطابقة" if diff_val == 0 else (f"🔴 عجز ({abs(diff_val):,.2f} ر.س)" if diff_val < 0 else f"🔵 زيادة ({diff_val:,.2f} ر.س)")
                col_rec3.write(f"الفعلي: {a_item['actual_cash']:,.2f} ر.س\nالدفتري: {a_item['book_bal']:,.2f} ر.س")
                col_rec4.write(f"الحالة: **{diff_str}**\nالملاحظات: {a_item.get('notes', 'لا يوجد')}")
                
                if col_rec5.button("🗑️ حذف", key=f"del_audit_btn_{real_a_idx}"):
                    audit_history.pop(real_a_idx)
                    save_audit_data(audit_history)
                    st.success("تم حذف سجل الجرد بنجاح!")
                    st.rerun()
                st.divider()
        else:
            st.info("لا توجد جلسات جرد سابقة محفوظة بالنظام.")

    elif selected_option == 'النسخ الاحتياطي' and st.session_state.user_role == "admin":
        st.subheader(f'💾 مركز إدارة النسخ الاحتياطي والأرشيف المالي - ({month_selected})')
        st.write('💡 يتيح لك هذا المركز حفظ نسخة كاملة من بيانات النظام المالية والإدارية على جهازك أو استعادتها فوراً:')
        
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown("### 📥 1. تصدير وتنزيل نسخة احتياطية (JSON):")
            st.info("تنزيل ملف شامل لكافة بيانات الرواتب، السجلات، والسندات المسجلة بالنظام حتى تاريخ اليوم:")
            if 'payroll_df' in st.session_state:
                json_str_full = st.session_state.payroll_df.to_json(orient='records', force_ascii=False, indent=4)
                st.download_button(
                    label="💾 اضغط هنا لتنزيل النسخة الاحتياطية فوراً (JSON)",
                    data=json_str_full.encode('utf-8'),
                    file_name=f"payroll_backup_{month_selected}.json",
                    mime="application/json",
                    use_container_width=True,
                    key="full_backup_download_btn_page"
                )
                
        with bc2:
            st.markdown("### 📤 2. استيراد ورفع نسخة احتياطية سابقة:")
            st.warning("رفع ملف JSON سابق سيستبدل بيانات الموظفين والرواتب بالملف المرفوع فوراً:")
            uploaded_backup_page = st.file_uploader("اختر ملف النسخة الاحتياطية (JSON) من جهازك:", type=['json'], key="full_backup_upload_page_btn")
            if uploaded_backup_page:
                try:
                    imported_df_page = pd.DataFrame(json.load(uploaded_backup_page))
                    st.session_state.payroll_df = imported_df_page
                    save_payroll_for_month(imported_df_page, month_selected)
                    st.success("تم استيراد وحفظ النسخة الاحتياطية بنجاح بنسبة 100%!")
                    st.rerun()
                except Exception:
                    st.error("خطأ في قراءة ملف النسخة المرفوع.")

    # 7. موديول إدخال الدفعات
    elif selected_option == 'إدخال الدفعات' and st.session_state.user_role == "admin":
        st.subheader(f'📊 جدول إدخال وتعديل الدفعات - ({month_selected})')
        
        curr_m_idx = st.session_state.months_list.index(month_selected)
        prev_month_label = st.session_state.months_list[curr_m_idx - 1] if curr_m_idx > 0 else 'أغسطس 2026'

        t1, t2, t3, t4 = st.tabs(['مصنع الخرج', 'مستودع الخرج', 'مستودع الرياض', 'رواتب متنوعة'])
        branches = [('مصنع ميم الخماسية الخرج', t1), ('مستودع ميم الخماسية الخرج', t2), ('مستودع ميم الخماسية الرياض', t3), ('رواتب متنوعة', t4)]
        
        all_cash_db = load_cash_data()
        current_month_cash = all_cash_db.get(month_selected, {'transactions': [], 'acc_transactions': []})
        existing_vouchers = current_month_cash.get('transactions', []) + current_month_cash.get('acc_transactions', [])

        for b_name, tab_obj in branches:
            with tab_obj:
                df_b_curr = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].copy()

                already_settled_vouchers = [
                    v for v in existing_vouchers 
                    if "سداد رواتب ودفعات" in v.get('party', '') and b_name in v.get('party', '')
                ]
                is_already_settled = len(already_settled_vouchers) > 0

                col_auto1, col_auto2 = st.columns([1.3, 1.7])
                with col_auto1:
                    if st.button(f'توزيع المتبقي كـ "دفعة 2" تلقائياً ({b_name})', key=f"auto_btn_{b_name}"):
                        for idx, row in st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].iterrows():
                            req_s = row['الراتب الأساسي']
                            p1 = row.get('الدفعة 1', 0)
                            ded = row.get('الخصومات', 0)
                            rem_needed = max(0, req_s - (p1 + ded))
                            st.session_state.payroll_df.loc[idx, 'الدفعة 2'] = rem_needed
                            st.session_state.payroll_df.loc[idx, 'الدفعة المدفوعة'] = p1 + rem_needed
                            st.session_state.payroll_df.loc[idx, 'المتبقي'] = 0.0
                        save_payroll_for_month(st.session_state.payroll_df, month_selected)
                        st.success("تم التوزيع وتصفير المتبقي!")
                        st.rerun()

                with col_auto2:
                    if is_already_settled:
                        last_v = already_settled_vouchers[-1]
                        st.success(f"✅ **تم اعتماد وتخصيم دفعات فرع ({b_name}) كـ سند صرف بالصندوق بنجاح (سند رقم: #{last_v.get('code', last_v['id'])})!**")
                        st.button(f"🔒 تم الاعتماد بالصندوق لـ {b_name}", key=f"dis_trf_btn_{b_name}", disabled=True, use_container_width=True)
                    else:
                        source_options = [f"رواتب شهر ({month_selected}) الحالي", f"رواتب شهر ({prev_month_label}) السابق"]

                        src_choice = st.selectbox(
                            "اختر مصدر الرواتب المراد خصمها بالصندوق:",
                            source_options,
                            key=f"src_choice_select_{b_name}_{month_selected}"
                        )

                        pay_choice = st.selectbox(
                            "اختر الدفعة المراد خصمها بالصندوق:",
                            ["إجمالي الدفعات معاً", "الدفعة الأولى فقط", "الدفعة الثانية فقط"],
                            key=f"pay_choice_select_{b_name}_{month_selected}"
                        )

                        if "السابق" in src_choice:
                            target_df_calc = get_payroll_for_month(prev_month_label)
                            label_month_used = prev_month_label
                        else:
                            target_df_calc = st.session_state.payroll_df
                            label_month_used = month_selected

                        target_df_branch = target_df_calc[target_df_calc['الفرع'] == b_name]

                        if pay_choice == "الدفعة الأولى فقط":
                            amt_to_deduct = target_df_branch['الدفعة 1'].sum()
                        elif pay_choice == "الدفعة الثانية فقط":
                            amt_to_deduct = target_df_branch['الدفعة 2'].sum()
                        else:
                            amt_to_deduct = target_df_branch['الدفعة المدفوعة'].sum()

                        st.markdown(f"#### 💵 **إجمالي المبلغ المجهز للخصم بالصندوق:** `{amt_to_deduct:,.2f} ر.س`")

                        if amt_to_deduct > 0:
                            if st.button(f'🚀 تأكيد خصم المبلغ ({amt_to_deduct:,.0f} ر.س) وإنشاء سند صرف بصندوق {month_selected}', key=f"confirm_trf_sal_btn_{b_name}", use_container_width=True):
                                all_cash = load_cash_data()
                                if month_selected not in all_cash:
                                    all_cash[month_selected] = {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []}
                                
                                m_cash = all_cash[month_selected]
                                target_trans_key = 'transactions' if st.session_state.user_role == "admin" else 'acc_transactions'
                                c_trans = m_cash.get(target_trans_key, [])
                                
                                v_code = f"PAY-SAL-{(len(c_trans) + 1):03d}"
                                c_trans.append({
                                    'id': len(c_trans) + 1,
                                    'code': v_code,
                                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                    'type': 'سند صرف',
                                    'party': f"سداد رواتب ودفعات ({pay_choice}) - شهر ({label_month_used}) - فرع ({b_name})",
                                    'amount': amt_to_deduct,
                                    'method': 'نقداً بالصندوق',
                                    'notes': f"سند صرف آلي معمد لـ ({pay_choice}) بفرع {b_name}"
                                })
                                m_cash[target_trans_key] = c_trans
                                all_cash[month_selected] = m_cash
                                save_cash_data(all_cash)
                                st.success(f"تم اعتماد وتخصيم {amt_to_deduct:,.2f} ر.س كـ سند صرف (#{v_code}) بـ فرع ({b_name}) بنجاح!")
                                st.rerun()

                cols_rtl = ['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'الدفعة 1', 'الدفعة 2', 'الخصومات', 'المتبقي', 'الملاحظات']
                edited_b = st.data_editor(
                    df_b_curr[cols_rtl],
                    column_config={
                        "م": st.column_config.NumberColumn("مسلسل", disabled=True),
                        "الاسم": st.column_config.TextColumn("اسم الموظف"),
                        "الوظيفة": st.column_config.TextColumn("الوظيفة"),
                        "الراتب الأساسي": st.column_config.NumberColumn("الراتب المستحق", min_value=0, format="%d ر.س"),
                        "الدفعة 1": st.column_config.NumberColumn("الدفعة 1", min_value=0, format="%d ر.س"),
                        "الدفعة 2": st.column_config.NumberColumn("الدفعة 2", min_value=0, format="%d ر.س"),
                        "الخصومات": st.column_config.NumberColumn("الخصومات", min_value=0, format="%d ر.س"),
                        "المتبقي": st.column_config.NumberColumn("المتبقي", disabled=True, format="%d ر.س"),
                        "الملاحظات": st.column_config.TextColumn("الملاحظات")
                    },
                    use_container_width=True,
                    hide_index=True,
                    key=f"ed_{b_name}_{month_selected}"
                )
                
                if st.button(f"حفظ التعديلات ({b_name})", key=f"btn_save_ed_{b_name}"):
                    for idx, row in edited_b.iterrows():
                        m_id = row['م']
                        target_idx = st.session_state.payroll_df[st.session_state.payroll_df['م'] == m_id].index[0]
                        p1 = row['الدفعة 1']
                        p2 = row['الدفعة 2']
                        ded = row['الخصومات']
                        sal = row['الراتب الأساسي']
                        tot_p = p1 + p2
                        st.session_state.payroll_df.loc[target_idx, 'الاسم'] = row['الاسم']
                        st.session_state.payroll_df.loc[target_idx, 'الوظيفة'] = row['الوظيفة']
                        st.session_state.payroll_df.loc[target_idx, 'الراتب الأساسي'] = sal
                        st.session_state.payroll_df.loc[target_idx, 'الخصومات'] = ded
                        st.session_state.payroll_df.loc[target_idx, 'الدفعة 1'] = p1
                        st.session_state.payroll_df.loc[target_idx, 'الدفعة 2'] = p2
                        st.session_state.payroll_df.loc[target_idx, 'الدفعة المدفوعة'] = tot_p
                        st.session_state.payroll_df.loc[target_idx, 'المتبقي'] = sal - (tot_p + ded)
                        st.session_state.payroll_df.loc[target_idx, 'الملاحظات'] = row['الملاحظات']
                    
                    save_payroll_for_month(st.session_state.payroll_df, month_selected)
                    st.success("تم الحفظ بنجاح!")
                    st.rerun()

                b_tot_req = edited_b['الراتب الأساسي'].sum()
                b_tot_p1 = edited_b['الدفعة 1'].sum()
                b_tot_p2 = edited_b['الدفعة 2'].sum()
                b_tot_ded = edited_b['الخصومات'].sum()
                b_tot_rem = b_tot_req - (b_tot_p1 + b_tot_p2 + b_tot_ded)

                st.divider()
                st.markdown(f"#### الملخص المالي لفرع ({b_name}):")
                s_col1, s_col2, s_col3, s_col4, s_col5 = st.columns(5)
                s_col1.metric("إجمالي الرواتب", f"{b_tot_req:,.0f} ر.س")
                s_col2.metric("إجمالي الدفعة 1", f"{b_tot_p1:,.0f} ر.س")
                s_col3.metric("إجمالي الدفعة 2", f"{b_tot_p2:,.0f} ر.س")
                s_col4.metric("إجمالي الخصومات", f"{b_tot_ded:,.0f} ر.س")
                s_col5.metric("إجمالي المتبقي", f"{b_tot_rem:,.0f} ر.س")

    # 8. موديول حركة الصندوق مع خاصية طباعة وتصدير الكشف
    elif selected_option == 'حركة الصندوق':
        st.subheader(f'🏦 إدارة حركة الصندوق - ({month_selected})')
        
        all_cash_db = load_cash_data()
        if month_selected not in all_cash_db:
            all_cash_db[month_selected] = {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []}
            
        current_m_cash = all_cash_db[month_selected]
        
        if st.session_state.user_role == "admin":
            box_selected = st.radio("اختر الخزينة للمراجعة والتسجيل:", ["🏢 الخزينة الرئيسية (wahby)", "👤 عُهدة المحاسب (omar)"], horizontal=True)
            active_box_key = 'transactions' if "wahby" in box_selected else 'acc_transactions'
            active_opening_key = 'opening' if "wahby" in box_selected else 'acc_opening'
            active_target_box = "main" if "wahby" in box_selected else "accountant"
        else:
            active_box_key = 'acc_transactions'
            active_opening_key = 'acc_opening'
            active_target_box = "accountant"
            st.info("أنت تعمل على شاشة **عُهدتك المالية (omar)**.")

        opening_bal = current_m_cash.get(active_opening_key, 0.0)

        st.write("")
        col_top_act1, col_top_act2 = st.columns([1, 1.2])
        with col_top_act1:
            if st.button("✏️ تعديل وتثبيت الرصيد الافتتاحي للصندوق", key="btn_open_dialog_bal"):
                opening_balance_dialog(month_selected, active_target_box)

        curr_trans = current_m_cash.get(active_box_key, [])
        tot_cash_in = sum(t['amount'] for t in curr_trans if 'قبض' in t['type'])
        tot_cash_out = sum(t['amount'] for t in curr_trans if 'صرف' in t['type'])
        net_cash_now = opening_bal + tot_cash_in - tot_cash_out

        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        c_m1.metric("رصيد أول الشهر", f"{opening_bal:,.2f} ر.س")
        c_m2.metric("🟢 المقبوضات", f"{tot_cash_in:,.2f} ر.س")
        c_m3.metric("🔴 المصروفات", f"{tot_cash_out:,.2f} ر.س")
        c_m4.metric("💵 المتبقي بالصندوق", f"{net_cash_now:,.2f} ر.س")

        st.divider()

        # قسم استخراج وطباعة وتصدير كشف حساب الصندوق المقابل Excel / PDF
        st.markdown("### 🖨️ طباعة وتصدير كشف حساب الصندوق المقابل (T-Account):")
        
        t_col_p1, t_col_p2, t_col_p3, t_col_p4 = st.columns([1.2, 1.3, 1.2, 1.2])
        with t_col_p1:
            period_type_sel = st.selectbox("نطاق كشف الحساب:", ["الشهر كاملاً", "فترة مخصصة (تحديد الأيام)"], key="sel_period_t_acc")
        
        period_label_txt = f"شهر {month_selected} كاملاً"
        filtered_print_trans = curr_trans.copy()

        if period_type_sel == "فترة مخصصة (تحديد الأيام)":
            with t_col_p2:
                d_start = st.date_input("من تاريخ:", datetime.now().date(), key="d_start_t_acc")
                d_end = st.date_input("إلى تاريخ:", datetime.now().date(), key="d_end_t_acc")
                period_label_txt = f"من {d_start} إلى {d_end}"
                
                filtered_print_trans = []
                for t in curr_trans:
                    try:
                        t_dt = datetime.strptime(t['date'].split(' ')[0], '%Y-%m-%d').date()
                        if d_start <= t_dt <= d_end:
                            filtered_print_trans.append(t)
                    except:
                        filtered_print_trans.append(t)

        with t_col_p3:
            st.write("")
            st.write("")
            if st.button("🖨️ معاينة كشف الحساب المقابل (A4)", key="btn_open_t_acc_print_modal", use_container_width=True):
                if filtered_print_trans:
                    target_box_txt = "الخزينة الرئيسية (wahby)" if active_target_box == "main" else "عُهدة المحاسب (omar)"
                    print_t_account_dialog(filtered_print_trans, month_selected, period_label_txt, target_box_txt)
                else:
                    st.warning("لا توجد حركات تسوية بالصندوق مسجلة بالفترة المحددة.")

        with t_col_p4:
            st.write("")
            st.write("")
            if filtered_print_trans:
                df_export_cash = pd.DataFrame(filtered_print_trans)
                csv_cash_bytes = df_export_cash.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 تصدير سجل الصندوق إلى Excel / CSV",
                    data=csv_cash_bytes,
                    file_name=f"سجل_حركة_الصندوق_{month_selected}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="btn_export_cash_csv"
                )

        st.divider()

        col_c_in1, col_c_in2 = st.columns([1, 1.8])
        with col_c_in1:
            st.markdown("### 📝 تسجيل حركة بالصندوق:")
            type_select_options = ["سند قبض", "سند صرف", "🔄 تحويل عُهدة إلى (omar)"] if st.session_state.user_role == "admin" else ["سند قبض", "سند صرف", "🔄 تحويل عُهدة إلى (wahby)"]
            
            with st.form("add_cash_transaction_form", clear_on_submit=True):
                trans_type = st.selectbox("نوع الحركة:", type_select_options)
                trans_party = st.text_input("اسم الجهة / البيان:", placeholder="مثلاً: العميل / شراء مواد خام")
                trans_amt = st.number_input("المبلغ (ر.س):", min_value=0.0, value=0.0)
                trans_pay_method = st.selectbox("طريقة السداد:", ["نقداً بالصندوق", "تحويل بنكي", "شيك"])
                trans_notes = st.text_input("ملاحظات / الفاتورة:")
                
                sub_cash = st.form_submit_button("💾 حفظ الحركة")
                if sub_cash:
                    if trans_party and trans_amt > 0:
                        if "تحويل عُهدة إلى (omar)" in trans_type and st.session_state.user_role == "admin":
                            v_code = f"TRF-{(len(curr_trans) + 1):03d}"
                            curr_trans.append({
                                'id': len(curr_trans) + 1,
                                'code': v_code,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'type': 'سند صرف',
                                'party': f"تحويل عُهدة إلى المحاسب (omar) - {trans_party}",
                                'amount': trans_amt,
                                'method': trans_pay_method,
                                'notes': trans_notes
                            })
                            
                            acc_trans = current_m_cash.get('acc_transactions', [])
                            acc_trans.append({
                                'id': len(acc_trans) + 1,
                                'code': f"REC-TRF-{(len(acc_trans) + 1):03d}",
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'type': 'سند قبض',
                                'party': f"استلام عُهدة محولة من الخزينة الرئيسية (wahby)",
                                'amount': trans_amt,
                                'method': trans_pay_method,
                                'notes': trans_notes
                            })
                            current_m_cash['acc_transactions'] = acc_trans

                        elif "تحويل عُهدة إلى (wahby)" in trans_type and st.session_state.user_role != "admin":
                            v_code = f"TRF-ACC-{(len(curr_trans) + 1):03d}"
                            curr_trans.append({
                                'id': len(curr_trans) + 1,
                                'code': v_code,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'type': 'سند صرف',
                                'party': f"تحويل نقدية واسترداد إلى الخزينة الرئيسية (wahby) - {trans_party}",
                                'amount': trans_amt,
                                'method': trans_pay_method,
                                'notes': trans_notes
                            })
                            
                            main_trans = current_m_cash.get('transactions', [])
                            main_trans.append({
                                'id': len(main_trans) + 1,
                                'code': f"REC-TRF-{(len(main_trans) + 1):03d}",
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'type': 'سند قبض',
                                'party': f"استلام نقدية محولة من عُهدة المحاسب (omar)",
                                'amount': trans_amt,
                                'method': trans_pay_method,
                                'notes': trans_notes
                            })
                            current_m_cash['transactions'] = main_trans

                        else:
                            rec_cnt = sum(1 for t in curr_trans if "قبض" in t['type'])
                            pay_cnt = sum(1 for t in curr_trans if "صرف" in t['type'])
                            v_code = f"REC-{(rec_cnt + 1):03d}" if "قبض" in trans_type else f"PAY-{(pay_cnt + 1):03d}"
                            
                            curr_trans.append({
                                'id': len(curr_trans) + 1,
                                'code': v_code,
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                'type': trans_type,
                                'party': trans_party,
                                'amount': trans_amt,
                                'method': trans_pay_method,
                                'notes': trans_notes
                            })

                        all_cash_db[month_selected][active_box_key] = curr_trans
                        save_cash_data(all_cash_db)
                        st.success(f"تم التسجيل بنجاح برقم #{v_code}!")
                        st.rerun()

        with col_c_in2:
            st.markdown("### 📊 دفتر يومية الصندوق:")
            if curr_trans:
                cf1, cf2 = st.columns([2, 1])
                with cf1:
                    cash_search = st.text_input("🔍 استعلام بالبيان:", key="search_cash_input")
                with cf2:
                    cash_filter_type = st.selectbox("تصفية بالحركة:", ["جميع الحركات", "سند قبض", "سند صرف"], key="filter_cash_type")

                filtered_cash = curr_trans.copy()
                if cash_search:
                    filtered_cash = [t for t in filtered_cash if cash_search.lower() in t['party'].lower()]
                if cash_filter_type != "جميع الحركات":
                    filtered_cash = [t for t in filtered_cash if t['type'] == cash_filter_type]

                items_per_page = 15
                total_items = len(filtered_cash)
                total_pages = (total_items + items_per_page - 1) // items_per_page if total_items > 0 else 1
                
                page_num = st.number_input(f"الصفحة (من أصل {total_pages}):", min_value=1, max_value=total_pages, value=1, step=1, key="cash_pg_num")
                start_idx = (page_num - 1) * items_per_page
                end_idx = start_idx + items_per_page
                page_trans = filtered_cash[start_idx:end_idx]

                for t_idx, t_item in enumerate(page_trans):
                    real_idx = curr_trans.index(t_item)
                    
                    is_rec = "قبض" in t_item['type']
                    amt_cls = "amt-pos" if is_rec else "amt-neg"
                    t_sign = "+" if is_rec else "-"
                    border_c = "#10B981" if is_rec else "#EF4444"

                    st.markdown(f"""
                        <div class="cash-card-item" style="border-right: 5px solid {border_c};">
                            <div>
                                <span style="font-weight:bold; font-size:14px;">#{t_item.get('code', t_item['id'])} - {t_item['party']}</span><br>
                                <span style="font-size:11px; color:#94A3B8;">📅 {t_item['date']} | 💳 {t_item['method']} | 📝 {t_item.get('notes','')}</span>
                            </div>
                            <div class="{amt_cls}">
                                {t_sign} {t_item['amount']:,.2f} ر.س
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    b_p, b_e, b_d = st.columns(3)
                    if b_p.button("🖨️ طباعة", key=f"btn_p_c_{real_idx}"):
                        print_cash_voucher_dialog(t_item, month_selected)

                    if b_e.button("✏️ تعديل", key=f"btn_e_c_{real_idx}"):
                        edit_cash_voucher_dialog(real_idx, month_selected, active_target_box)

                    if b_d.button("🗑️ حذف", key=f"btn_d_c_{real_idx}"):
                        curr_trans.pop(real_idx)
                        all_cash_db[month_selected][active_box_key] = curr_trans
                        save_cash_data(all_cash_db)
                        st.success("تم الحذف!")
                        st.rerun()

            else:
                st.info("لا توجد حركات تسوية بالصندوق مسجلة لهذا الشهر.")

    elif selected_option == 'دليل الموظفين' and st.session_state.user_role == "admin":
        st.subheader('👤 دليل الموظفين والملفات الإدارية')
        
        search_kw = st.text_input("🔍 استعلام باسم الموظف أو الوظيفة:", placeholder="اكتب جزءاً من الاسم...")
        if search_kw:
            search_df = st.session_state.payroll_df[st.session_state.payroll_df['الاسم'].str.contains(search_kw, case=False, na=False) | st.session_state.payroll_df['الوظيفة'].str.contains(search_kw, case=False, na=False)]
            st.write(f"نتائج البحث عن (**{search_kw}**):")
            for e_idx, e_row in search_df.iterrows():
                c_card1, c_card2, c_card3, c_card4 = st.columns([2, 1.5, 1.5, 1])
                c_card1.write(f"👤 **{e_row['الاسم']}** ({e_row['الوظيفة']}) - {e_row['الفرع']}")
                c_card2.write(f"💵 الراتب: **{e_row['الراتب الأساسي']:,.0f} ر.س**")
                c_card3.write(f"📅 بداية العمل: {e_row.get('تاريخ بداية العمل', '2024-01-01')}")
                if c_card4.button("تعديل", key=f"btn_s_edit_{e_row['م']}"):
                    edit_employee_dialog(e_idx, month_selected)
                st.divider()
        else:
            cnt_factory = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'مصنع ميم الخماسية الخرج'])
            cnt_wh_kh = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'مستودع ميم الخماسية الخرج'])
            cnt_wh_ry = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'مستودع ميم الخماسية الرياض'])
            cnt_misc = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'رواتب متنوعة'])
            
            tab_search_list = [
                (f'مصنع الخرج ({cnt_factory})', 'مصنع ميم الخماسية الخرج'),
                (f'مستودع الخرج ({cnt_wh_kh})', 'مستودع ميم الخماسية الخرج'),
                (f'مستودع الرياض ({cnt_wh_ry})', 'مستودع ميم الخماسية الرياض'),
                (f'رواتب متنوعة ({cnt_misc})', 'رواتب متنوعة')
            ]
            
            search_tabs = st.tabs([t[0] for t in tab_search_list])
            
            for idx_st, (s_title, b_name) in enumerate(tab_search_list):
                with search_tabs[idx_st]:
                    col_h1, col_h2 = st.columns([3, 1])
                    with col_h1:
                        st.write(f"دليل موظفي **{b_name}**:")
                    with col_h2:
                        if st.button(f"إضافة موظف لـ {b_name}", key=f"btn_modal_add_{b_name}"):
                            add_employee_dialog(b_name)

                    branch_df_search = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name]
                    
                    if not branch_df_search.empty:
                        for e_idx, e_row in branch_df_search.iterrows():
                            c_card1, c_card2, c_card3, c_card4 = st.columns([2, 1.5, 1.5, 1])
                            c_card1.write(f"👤 **{e_row['الاسم']}** ({e_row['الوظيفة']})")
                            c_card2.write(f"💵 الراتب: **{e_row['الراتب الأساسي']:,.0f} ر.س**")
                            c_card3.write(f"📅 بداية العمل: {e_row.get('تاريخ بداية العمل', '2024-01-01')}")
                            
                            if c_card4.button("تعديل", key=f"btn_edit_m_{e_row['م']}"):
                                edit_employee_dialog(e_idx, month_selected)
                            st.divider()
                    else:
                        st.info(f"لا يوجد موظفين حالياً في {b_name}.")

    elif selected_option == 'مسير الرواتب' and st.session_state.user_role == "admin":
        st.subheader(f'📋 كشف مسير الرواتب الشهري الموحد - ({month_selected})')
        filter_sheet = st.selectbox('اختر الفرع للكشف:', ['جميع الفروع (الكشف الموحد)', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'])
        df_sheet = st.session_state.payroll_df if 'جميع الفروع' in filter_sheet else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == filter_sheet]
        
        # تصدير جدول مسير الرواتب الموحد بملف Excel مباشر
        csv_payroll_bytes = df_sheet.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=f"📊 تصدير كشف المسير إلى Excel / CSV ({filter_sheet})",
            data=csv_payroll_bytes,
            file_name=f"كشف_مسير_رواتب_{filter_sheet}_{month_selected}.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_export_payroll_excel"
        )
        st.write("")

        sheet_html = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
        <meta charset="utf-8">
        <title>كشف مسير رواتب - شركة ميم الخماسية للتصنيع</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 10px; background: #fff; color: #111; }}
            .header {{ text-align: center; color: #1E3A8A; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; margin-bottom: 15px; }}
            .header h2 {{ margin: 0; font-size: 24px; }}
            .header h3 {{ margin: 5px 0 0 0; font-size: 18px; color: #475569; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #334155; padding: 6px 8px; text-align: center; font-size: 13px; }}
            th {{ background-color: #1E3A8A; color: white; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #f8fafc; }}
            .totals-box {{ margin-top: 15px; padding: 10px; background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 5px; font-weight: bold; display: flex; justify-content: space-around; font-size: 14px; }}
            .signatures {{ margin-top: 30px; display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; padding: 0 30px; }}
        </style>
        </head>
        <body>
            <div class="header">
                <h2>🏢 شركة ميم الخماسية للتصنيع</h2>
                <h3>كشف مسير الرواتب - {filter_sheet} ({month_selected})</h3>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>م</th>
                        <th>اسم الموظف</th>
                        <th>الوظيفة</th>
                        <th>الفرع</th>
                        <th>الراتب المستحق</th>
                        <th>الدفعة 1</th>
                        <th>الدفعة 2</th>
                        <th>الخصومات</th>
                        <th>إجمالي المصروف</th>
                        <th>المتبقي</th>
                        <th>التوقيع / الاستلام</th>
                    </tr>
                </thead>
                <tbody>
        """
        for idx, r in df_sheet.iterrows():
            sheet_html += f"""
                <tr>
                    <td>{r['م']}</td>
                    <td><strong>{r['الاسم']}</strong></td>
                    <td>{r['الوظيفة']}</td>
                    <td>{r['الفرع']}</td>
                    <td>{r['الراتب الأساسي']:,.0f} ر.س</td>
                    <td>{r.get('الدفعة 1', 0):,.0f} ر.س</td>
                    <td>{r.get('الدفعة 2', 0):,.0f} ر.س</td>
                    <td style="color:#b91c1c;">{r.get('الخصومات', 0):,.0f} ر.س</td>
                    <td style="color:#047857; font-weight:bold;">{r['الدفعة المدفوعة']:,.0f} ر.س</td>
                    <td style="color:#b91c1c; font-weight:bold;">{r['المتبقي']:,.0f} ر.س</td>
                    <td style="width: 120px;"></td>
                </tr>
            """
        sheet_html += f"""
                </tbody>
            </table>
            <div class="totals-box">
                <span>إجمالي الرواتب: {df_sheet['الراتب الأساسي'].sum():,.0f} ر.س</span>
                <span>إجمالي الخصومات: {df_sheet.get('الخصومات', pd.Series([0])).sum():,.0f} ر.س</span>
                <span>إجمالي المصروف: {df_sheet['الدفعة المدفوعة'].sum():,.0f} ر.س</span>
                <span>إجمالي المتبقي: {df_sheet['المتبقي'].sum():,.0f} ر.س</span>
            </div>
            <div class="signatures">
                <div>إعداد المحاسب: __________________</div>
                <div>مراجعة الموارد البشرية: __________________</div>
                <div>اعتماد المدير العام: __________________</div>
            </div>
        </body>
        </html>
        """
        st.components.v1.html(sheet_html, height=400, scrolling=True)
        st.download_button(
            label=f"📄 فتح وتحميل ملف كشف مسير {filter_sheet} (HTML / PDF) 🖨️",
            data=sheet_html.encode('utf-8'),
            file_name=f"مسير_رواتب_{filter_sheet}_{month_selected}.html",
            mime="text/html",
            use_container_width=True
        )

    elif selected_option == 'طباعة السندات' and st.session_state.user_role == "admin":
        st.subheader(f'🖨️ طباعة سندات القبض والصرف الرسمية A4 - ({month_selected})')
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            selected_b = st.selectbox('اختر الفرع:', ['جميع الفروع', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'], key="sb_v_b")
        with col_p2:
            pay_type_select = st.selectbox('اختر نوع الدفعة:', ['جميع الدفعات (السند الشامل)', 'الدفعة الأولى فقط', 'الدفعة الثانية فقط'], key="sb_v_type")
            
        df_print = st.session_state.payroll_df if selected_b == 'جميع الفروع' else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == selected_b]
        
        pdf_bytes = generate_pretty_html_pdf(df_print, selected_b, pay_type_select)
        st.components.v1.html(pdf_bytes.getvalue().decode('utf-8'), height=400, scrolling=True)
        st.download_button(
            label=f"📄 تنزيل ملف سندات ({pay_type_select}) - {selected_b} للطباعة 🖨️",
            data=pdf_bytes,
            file_name=f"سندات_{pay_type_select}_{selected_b}_{month_selected}.html",
            mime="text/html",
            use_container_width=True
        )

    elif selected_option == 'حاسبة الخدمة' and st.session_state.user_role == "admin":
        st.subheader('🇸🇦 حاسبة مستحقات نهاية الخدمة وبدل الإجازات (نظام العمل السعودي)')
        saudi_reports = []
        for _, r in st.session_state.payroll_df.iterrows():
            yrs, grat, leave_allow = calculate_saudi_gratuity_and_leave(r['الراتب الأساسي'], r.get('تاريخ بداية العمل', '2024-01-01'))
            saudi_reports.append({
                'مسلسل': r['م'],
                'اسم الموظف': r['الاسم'],
                'الفرع': r['الفرع'],
                'تاريخ بداية العمل': r.get('تاريخ بداية العمل', '2024-01-01'),
                'الخدمة (سنة)': yrs,
                'مكافأة نهاية الخدمة': f"{grat:,.2f} ر.س",
                'بدل الإجازة السنوية': f"{leave_allow:,.2f} ر.س",
                'إجمالي المستحقات': f"{(grat + leave_allow):,.2f} ر.س"
            })
            
        df_saudi = pd.DataFrame(saudi_reports)
        st.dataframe(df_saudi, use_container_width=True, hide_index=True)

    elif selected_option == 'التنبيهات' and st.session_state.user_role == "admin":
        st.subheader('🔔 مركز تنبيهات انتهاء الإقامات وعقود العمل')
        today = datetime.now().date()
        alerts = []
        for _, r in st.session_state.payroll_df.iterrows():
            try:
                iq_d = datetime.strptime(str(r.get('تاريخ انتهاء الإقامة')), '%Y-%m-%d').date()
                ct_d = datetime.strptime(str(r.get('تاريخ انتهاء العقد')), '%Y-%m-%d').date()
                if iq_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': 'إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🔴 منتهية'})
                elif (iq_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': 'إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🟡 تنتهي قريباً'})
                if ct_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': 'عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🔴 منتهي'})
                elif (ct_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': 'عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🟡 ينتهي قريباً'})
            except: pass
        if alerts: st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
        else: st.success('جميع الإقامات والعقود سارية ولا يوجد وثائق منتهية حالياً!')

    elif selected_option == 'الإغلاق السنوي' and st.session_state.user_role == "admin":
        st.subheader('🏁 شاشة الإغلاق المالي السنوي وفتح سنة جديدة')
        st.markdown("### ملخص الرواتب والدفعات الكلية بالسجلات:")
        st.dataframe(st.session_state.payroll_df[['م', 'الاسم', 'الوظيفة', 'الفرع', 'الراتب الأساسي', 'الخصومات', 'الدفعة المدفوعة', 'المتبقي']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.markdown("### فتح سنة جديدة:")
        col_y1, col_y2 = st.columns(2)
        with col_y1:
            next_year_name = st.text_input("السنة المالية الجديدة:", "2027")
        with col_y2:
            st.write("")
            st.write("")
            if st.button(f"إغلاق السنة المالية الحالية وفتح سنة ({next_year_name})"):
                st.session_state.months_list = [f'يناير {next_year_name}', f'فبراير {next_year_name}', f'مارس {next_year_name}', f'أبريل {next_year_name}']
                st.success(f"تم إغلاق السنة الحالية وافتتاح سنة ({next_year_name}) بنجاح!")
                st.rerun()
