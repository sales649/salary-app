import streamlit as st
import pandas as pd
import io
import json
import os
from datetime import datetime

# 1. إعداد الصفحة وتنسيق الاتجاه العربي الموحد RTL
st.set_page_config(page_title='شركة ميم الخماسية للتصنيع - النظام المحاسبي الموحد', layout='wide', page_icon='🏢')

ADMIN_PASSWORD = "admin5m"
USER_PASSWORD = "user5m"

if 'theme_mode' not in st.session_state:
    st.session_state['theme_mode'] = '🌙 وضع ليلي'

if '🌙' in st.session_state['theme_mode']:
    bg_app = "#0F172A"
    bg_card = "#1E293B"
    bg_sidebar = "#1E293B"
    text_color = "#FFFFFF"
    border_color = "#D97706"
    input_bg = "#F1F5F9"
    input_text = "#0F172A"
    modal_bg = "#1E293B"
    modal_text = "#FFFFFF"
    expander_bg = "#0F172A"
    expander_text = "#FFFFFF"
else:
    bg_app = "#F1F5F9"
    bg_card = "#FFFFFF"
    bg_sidebar = "#FFFFFF"
    text_color = "#0F172A"
    border_color = "#D97706"
    input_bg = "#FFFFFF"
    input_text = "#0F172A"
    modal_bg = "#FFFFFF"
    modal_text = "#0F172A"
    expander_bg = "#F8FAFC"
    expander_text = "#0F172A"

st.markdown(f"""
    <style>
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            direction: rtl !important;
            text-align: right !important;
            background-color: {bg_app} !important;
            color: {text_color} !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            overflow-x: hidden !important;
        }}
        
        h1, h2, h3, h4, h5, h6, .stMarkdown, label, p, span, div {{
            direction: rtl !important;
            text-align: right !important;
            color: {text_color} !important;
            font-weight: 600 !important;
            word-wrap: break-word !important;
        }}

        /* ضغط المسافات الفاضية بالقائمة الجانبية وجعلها ملمومة احترافياً */
        [data-testid="stSidebar"] {{
            right: 0 !important;
            left: auto !important;
            border-left: 2px solid {border_color} !important;
            background-color: {bg_sidebar} !important;
        }}

        [data-testid="stSidebarContent"] {{
            padding-top: 10px !important;
            padding-bottom: 10px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }}

        [data-testid="stSidebar"] details {{
            margin-bottom: 4px !important;
        }}

        [data-testid="stSidebar"] hr {{
            margin-top: 8px !important;
            margin-bottom: 8px !important;
        }}

        [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
            color: {text_color} !important;
            font-size: 13px !important;
            font-weight: 700 !important;
        }}

        [data-testid="stSidebar"] .streamlit-expanderHeader,
        [data-testid="stSidebar"] details[open] summary,
        [data-testid="stSidebar"] details summary:hover,
        [data-testid="stSidebar"] details summary:focus {{
            background-color: {bg_card} !important;
            color: #F59E0B !important;
            font-weight: 700 !important;
            border: 1px solid #D97706 !important;
            border-radius: 8px !important;
            padding-top: 6px !important;
            padding-bottom: 6px !important;
        }}

        [data-testid="stSidebar"] .streamlit-expanderContent {{
            background-color: {expander_bg} !important;
            color: {expander_text} !important;
            border-radius: 0 0 8px 8px !important;
            padding: 8px !important;
            border: 1px solid #D97706 !important;
            border-top: none !important;
        }}

        ul[data-baseweb="menu"], div[role="listbox"], [data-baseweb="popover"] div {{
            background-color: {bg_card} !important;
            color: {text_color} !important;
            border: 1px solid #D97706 !important;
        }}

        li[role="option"], li[role="option"] * {{
            color: {text_color} !important;
            background-color: {bg_card} !important;
            font-weight: 700 !important;
        }}

        li[role="option"]:hover, li[role="option"]:hover * {{
            background-color: #D97706 !important;
            color: #FFFFFF !important;
        }}

        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], [data-testid="stDateInput"] input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }}

        /* تنظيف تصميم النسخ الاحتياطي ورفع الملفات */
        [data-testid="stFileUploader"], [data-testid="stFileUploader"] section {{
            background-color: #1E293B !important;
            border: 1px dashed #D97706 !important;
            border-radius: 8px !important;
            padding: 6px !important;
        }}

        [data-testid="stFileUploader"] button {{
            background-color: #D97706 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            padding: 4px 10px !important;
            font-size: 12px !important;
        }}

        [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] small {{
            color: #FFFFFF !important;
            font-weight: bold !important;
            font-size: 12px !important;
        }}

        [data-testid="stDialog"] div[role="dialog"] {{
            background-color: {modal_bg} !important;
            border: 3px solid #D97706 !important;
            border-radius: 16px !important;
            width: 95vw !important;
            max-width: 600px !important;
        }}

        [data-testid="stDialog"] div[role="dialog"] label, 
        [data-testid="stDialog"] div[role="dialog"] p, 
        [data-testid="stDialog"] div[role="dialog"] span,
        [data-testid="stDialog"] div[role="dialog"] h1,
        [data-testid="stDialog"] div[role="dialog"] h2,
        [data-testid="stDialog"] div[role="dialog"] h3,
        [data-testid="stDialog"] div[role="dialog"] div {{
            color: {modal_text} !important;
            font-weight: 700 !important;
            text-align: right !important;
        }}

        .stButton>button, .stDownloadButton>button, [data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 800 !important;
            font-size: 14px !important;
            box-shadow: 0 4px 6px -1px rgba(217, 119, 6, 0.4) !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            padding-top: 6px !important;
            padding-bottom: 6px !important;
        }}

        .stMetric, .daftra-quick-card {{
            background-color: {bg_card} !important;
            border-radius: 12px !important;
            padding: 12px !important;
            border: 1px solid {border_color} !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 8px !important;
        }}

        .stMetric * {{
            color: {text_color} !important;
            text-align: right !important;
        }}

        .stDataFrame, [data-testid="stDataEditor"] {{
            direction: rtl !important;
            text-align: right !important;
            background-color: {bg_card} !important;
        }}

        .stDataFrame td, .stDataFrame th, [data-testid="stDataEditor"] td, [data-testid="stDataEditor"] th {{
            text-align: right !important;
            font-size: 13px !important;
            color: {text_color} !important;
        }}

        .welcome-card-lux {{
            background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
            border-radius: 20px;
            padding: 30px 15px;
            text-align: center !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            margin-top: 10px;
            border: 2px solid #D97706;
        }}

        .title-company-huge {{
            font-size: 28px !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, #FFF 0%, #F59E0B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 10px;
            margin-bottom: 10px;
            text-align: center !important;
        }}

        .company-header-inner {{
            background: linear-gradient(135deg, {bg_card} 0%, {bg_app} 100%);
            border: 2px solid #D97706;
            border-radius: 16px;
            padding: 12px 20px;
            text-align: center !important;
            margin-top: 5px;
            margin-bottom: 15px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }}

        .company-header-inner-title {{
            font-size: 22px !important;
            font-weight: 900 !important;
            color: #F59E0B !important;
            margin: 0 !important;
            text-align: center !important;
        }}

        .company-header-inner-sub {{
            font-size: 13px !important;
            color: #94A3B8 !important;
            margin: 2px 0 0 0 !important;
        }}

        .logo-lux {{
            font-size: 65px;
            font-weight: 900;
            color: #EF4444 !important;
            font-family: Arial, sans-serif;
            line-height: 1;
            margin-bottom: 5px;
            text-align: center !important;
        }}

        .date-badge-lux {{
            display: inline-block;
            background: linear-gradient(135deg, #D97706 0%, #B45309 100%);
            color: #FFFFFF !important;
            padding: 5px 20px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 800;
            margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.3);
            text-align: center !important;
        }}

        /* إصلاح حاسم ومتجاوب لتطبيق الآيفون والموبايل */
        @media (max-width: 768px) {{
            [data-testid="stSidebar"] {{
                width: 100vw !important;
                max-width: 100vw !important;
                z-index: 999999 !important;
            }}
            .title-company-huge {{
                font-size: 22px !important;
            }}
            .company-header-inner-title {{
                font-size: 18px !important;
            }}
            .logo-lux {{
                font-size: 50px !important;
            }}
            [data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
            }}
        }}
    </style>
""", unsafe_allow_html=True)

# إدارة الدخول
if 'app_started' not in st.session_state:
    st.session_state['app_started'] = False

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

if 'current_view' not in st.session_state:
    st.session_state['current_view'] = '🏠 الرئيسية'

DATA_FILE = 'payroll_data.json'
CASH_FILE = 'cashbox_data.json'

initial_data = [
    {'م': 1, 'الاسم': 'مد ساجد ', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-15', 'تاريخ انتهاء العقد': '2027-01-01', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-09-20', 'تاريخ انتهاء العقد': '2026-12-31', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 3, 'الاسم': 'أيوب', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-08-01', 'تاريخ انتهاء العقد': '2026-11-15', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 4, 'الاسم': 'ذاكر حسين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-10', 'تاريخ انتهاء العقد': '2027-05-20', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 5, 'الاسم': 'رفيق الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 1600.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-10', 'تاريخ انتهاء العقد': '2027-03-01', 'الخصومات': 1600.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 6, 'الاسم': 'رحيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-20', 'تاريخ انتهاء العقد': '2027-02-01', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 7, 'الاسم': 'محي الدين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-15', 'تاريخ انتهاء العقد': '2027-06-01', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 8, 'الاسم': 'محمد ريان', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-01', 'تاريخ انتهاء العقد': '2027-04-01', 'الخصومات': 0.0, 'الدفعة 1': 1000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 9, 'الاسم': 'مدلايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-01', 'تاريخ انتهاء العقد': '2027-01-15', 'الخصومات': 0.0, 'الدفعة 1': 1000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 10, 'الاسم': 'عالم روبيل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-05-10', 'تاريخ انتهاء العقد': '2027-07-01', 'الخصومات': 0.0, 'الدفعة 1': 500.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 11, 'الاسم': 'شوقي كامل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-30', 'تاريخ انتهاء العقد': '2027-01-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 12, 'الاسم': 'عمرو فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-01', 'تاريخ انتهاء العقد': '2027-05-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 13, 'الاسم': 'محمد فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-01', 'تاريخ انتهاء العقد': '2027-05-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 14, 'الاسم': 'إبراهيم السيد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-15', 'تاريخ انتهاء العقد': '2027-02-01', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 15, 'الاسم': 'مصطفي عماد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-03-15', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 16, 'الاسم': 'محمد شريف ', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-10', 'تاريخ انتهاء العقد': '2027-02-28', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 17, 'الاسم': 'محمد رضا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-15', 'تاريخ انتهاء العقد': '2027-04-30', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 18, 'الاسم': 'محمد ابو نهي ', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-05', 'تاريخ انتهاء العقد': '2026-12-15', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 4000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 19, 'الاسم': 'محمد ابو صبري ', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-01', 'تاريخ انتهاء العقد': '2027-06-15', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 20, 'الاسم': 'سليمان محي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-30', 'تاريخ انتهاء العقد': '2027-02-10', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 21, 'الاسم': 'فهمي محمد ', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-05', 'تاريخ انتهاء العقد': '2027-03-20', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 22, 'الاسم': 'ريحاني', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-09-25', 'تاريخ انتهاء العقد': '2026-12-05', 'الخصومات': 0.0, 'الدفعة 1': 2200.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 23, 'الاسم': 'دلال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-15', 'تاريخ انتهاء العقد': '2027-05-10', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 24, 'الاسم': 'فاربيس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-20', 'تاريخ انتهاء العقد': '2027-02-15', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 25, 'الاسم': 'قدوس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-28', 'تاريخ انتهاء العقد': '2027-04-18', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 26, 'الاسم': 'مد ابراهيم ', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-05-01', 'تاريخ انتهاء العقد': '2027-07-10', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 27, 'الاسم': 'أنيس الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-10', 'تاريخ انتهاء العقد': '2026-12-25', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 28, 'الاسم': 'حبيب مد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-15', 'تاريخ انتهاء العقد': '2027-03-30', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 29, 'الاسم': 'مطاوع', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-05', 'تاريخ انتهاء العقد': '2027-01-20', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 30, 'الاسم': 'حبيب الاسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-25', 'تاريخ انتهاء العقد': '2027-05-30', 'الخصومات': 0.0, 'الدفعة 1': 1000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 31, 'الاسم': 'بطشا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-05', 'تاريخ انتهاء العقد': '2027-02-12', 'الخصومات': 0.0, 'الدفعة 1': 1200.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2200.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 32, 'الاسم': 'السيد محمود', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-10', 'تاريخ انتهاء العقد': '2027-06-20', 'الخصومات': 0.0, 'الدفعة 1': 500.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 33, 'الاسم': 'علي إسماعيل', 'الوظيفة': 'معمل', 'الراتب الأساسي': 4500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-25', 'تاريخ انتهاء العقد': '2027-01-15', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 1500.0, 'الدفعة المدفوعة': 4500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 34, 'الاسم': 'محمد حمدان عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 4500.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-10', 'تاريخ انتهاء العقد': '2027-04-05', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 1500.0, 'الدفعة المدفوعة': 4500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 35, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-01', 'تاريخ انتهاء العقد': '2027-02-14', 'الخصومات': 0.0, 'الدفعة 1': 4000.0, 'الدفعة 2': 3000.0, 'الدفعة المدفوعة': 7000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 41, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-09-05', 'تاريخ انتهاء العقد': '2026-10-10', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 42, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-06-01', 'تاريخ انتهاء العقد': '2027-08-01', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 43, 'الاسم': 'محمود عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-10', 'تاريخ انتهاء العقد': '2027-03-15', 'الخصومات': 7000.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 44, 'الاسم': 'شمشاد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-20', 'تاريخ انتهاء العقد': '2026-12-30', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 4000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 45, 'الاسم': 'زنجير', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-05', 'تاريخ انتهاء العقد': '2027-05-12', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 46, 'الاسم': 'بابلو', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-12', 'تاريخ انتهاء العقد': '2027-01-25', 'الخصومات': 0.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 5000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 47, 'الاسم': 'إسماعيل الحداد', 'الوظيفة': 'حداد', 'الراتب الأساسي': 6000.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-20', 'تاريخ انتهاء العقد': '2027-04-10', 'الخصومات': 0.0, 'الدفعة 1': 3500.0, 'الدفعة 2': 2500.0, 'الدفعة المدفوعة': 6000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 48, 'الاسم': 'نعيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-15', 'تاريخ انتهاء العقد': '2027-02-20', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 49, 'الاسم': 'مرسي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-04-05', 'تاريخ انتهاء العقد': '2027-06-12', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 50, 'الاسم': 'محمد علي كاشف', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-10-18', 'تاريخ انتهاء العقد': '2026-12-28', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 51, 'الاسم': 'احمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-25', 'تاريخ انتهاء العقد': '2027-03-30', 'الخصومات': 0.0, 'الدفعة 1': 2500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 52, 'الاسم': 'عبد الرحمن محمد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500.0, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-30', 'تاريخ انتهاء العقد': '2027-05-25', 'الخصومات': 0.0, 'الدفعة 1': 1500.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 2500.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 36, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-12-12', 'تاريخ انتهاء العقد': '2027-04-01', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 37, 'الاسم': 'محمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 0.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-02-05', 'تاريخ انتهاء العقد': '2027-04-10', 'الخصومات': 0.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 38, 'الاسم': 'سمان السواق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2026-11-25', 'تاريخ انتهاء العقد': '2027-01-30', 'الخصومات': 500.0, 'الدفعة 1': 3000.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 39, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب الأساسي': 4000.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-01-20', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 2000.0, 'الدفعة المدفوعة': 4000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 40, 'الاسم': 'إبراهيم جمال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000.0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-03-15', 'تاريخ انتهاء العقد': '2027-05-18', 'الخصومات': 0.0, 'الدفعة 1': 2000.0, 'الدفعة 2': 1000.0, 'الدفعة المدفوعة': 3000.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 53, 'الاسم': 'موظف متنوع 1', 'الوظيفة': 'متنوع', 'الراتب الأساسي': 0.0, 'الفرع': 'رواتب متنوعة', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-01-01', 'تاريخ انتهاء العقد': '2027-01-01', 'الخصومات': 0.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''},
    {'م': 54, 'الاسم': 'سمير المغازي ', 'الوظيفة': 'كميائي ', 'الراتب الأساسي': 5000.0, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ بداية العمل': '2024-01-01', 'تاريخ انتهاء الإقامة': '2027-12-31', 'تاريخ انتهاء العقد': '2027-12-31', 'الخصومات': 5000.0, 'الدفعة 1': 0.0, 'الدفعة 2': 0.0, 'الدفعة المدفوعة': 0.0, 'المتبقي': 0.0, 'نوع الإجراء': 'صرف كامل', 'الملاحظات': ''}
]

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                df = pd.DataFrame(json.load(f))
                if 'تاريخ بداية العمل' not in df.columns:
                    df['تاريخ بداية العمل'] = '2024-01-01'
                if 'الخصومات' not in df.columns:
                    df['الخصومات'] = 0.0
                return df
        except Exception:
            return pd.DataFrame(initial_data)
    else:
        df = pd.DataFrame(initial_data)
        save_data(df)
        return df

def save_data(df):
    data_dict = df.to_dict(orient='records')
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

def load_cash_data():
    if os.path.exists(CASH_FILE):
        try:
            with open(CASH_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cash_data(data):
    with open(CASH_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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

@st.dialog("⚡ إنشاء سند قبض / صرف سريع")
def quick_cash_voucher_dialog(default_type, month_name, target_box="main"):
    st.write(f"إضافة سند لشهر: **{month_name}** ({'الرئيسية' if target_box == 'main' else 'omar'})")
    with st.form("quick_cash_form"):
        q_type = st.selectbox("نوع السند:", ["سند قبض / إيراد", "سند صرف / مصروف"], index=0 if "قبض" in default_type else 1)
        q_party = st.text_input("صادر إلى / مستلم من:", placeholder="اسم الجهة...")
        q_amt = st.number_input("المبلغ (ر.س):", min_value=0.0, value=0.0)
        q_method = st.selectbox("طريقة الدفع:", ["نقداً بالصندوق", "تحويل بنكي", "شيك"])
        q_notes = st.text_input("البيان والملاحظات:")
        
        q_sub = st.form_submit_button("💾 حفظ السند")
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
                
                rec_count = sum(1 for t in c_trans if "قبض" in t['type'])
                pay_count = sum(1 for t in c_trans if "صرف" in t['type'])
                v_code = f"REC-{(rec_count + 1):03d}" if "قبض" in q_type else f"PAY-{(pay_count + 1):03d}"
                
                new_trans = {
                    'id': len(c_trans) + 1,
                    'code': v_code,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'type': q_type,
                    'party': q_party,
                    'amount': q_amt,
                    'method': q_method,
                    'notes': q_notes
                }
                c_trans.append(new_trans)
                m_cash[box_key] = c_trans
                all_cash[month_name] = m_cash
                save_cash_data(all_cash)
                st.success(f"تم الحفظ برقم #{v_code}!")
                st.rerun()

@st.dialog("🖨️ طباعة سند الصندوق الرسمية (A4)")
def print_cash_voucher_dialog(trans_item, month_name):
    st.write(f"معاينة السند رقم: **#{trans_item.get('code', trans_item['id'])}**")
    amt_val = trans_item['amount']
    t_type = trans_item['type']
    party_label = "استلمنا من السيد / الشركَة:" if "قبض" in t_type else "تم الصرف للسيد / الشركَة:"
    
    html_v = f"""
    <!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #fff; margin: 0; padding: 10px; }}
        .voucher-box {{ border: 3px solid #1E3A8A; border-radius: 12px; padding: 20px; background: #fff; }}
        .header-logo {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 10px; }}
        .v-title {{ text-align: center; font-size: 22px; font-weight: bold; color: #1E3A8A; background: #f1f5f9; padding: 10px; margin: 15px 0; border-radius: 6px; }}
        .v-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .v-table td, .v-table th {{ border: 1px solid #cbd5e1; padding: 12px; text-align: right; font-size: 15px; }}
        .amt-tag {{ font-size: 22px; font-weight: bold; color: #047857; background: #ecfdf5; border: 2px solid #10b981; text-align: center; padding: 8px; border-radius: 6px; }}
        .sigs {{ margin-top: 50px; display: flex; justify-content: space-between; font-weight: bold; font-size: 15px; }}
        @media print {{ .no-p {{ display: none; }} }}
    </style></head><body>
        <div class="no-p" style="text-align:center; margin-bottom:15px;">
            <button onclick="window.print()" style="background:#1E3A8A; color:white; border:none; padding:12px 25px; font-weight:bold; font-size:16px; border-radius:6px; cursor:pointer;">🖨️ طباعة السند (A4 / PDF)</button>
        </div>
        <div class="voucher-box">
            <div class="header-logo">
                <div style="font-size:13px; font-weight:bold;">Five-M Company For Industry<br>C. R. : 1011145035</div>
                <div style="font-size:50px; font-weight:900; color:#DC2626; font-family:Arial;">5M</div>
                <div style="font-size:13px; font-weight:bold;">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
            </div>
            <div class="v-title">{t_type} - شهر ({month_name}) | رقم السند: #{trans_item.get('code', trans_item['id'])}</div>
            <table class="v-table">
                <tr><th>التاريخ والتوقيت</th><td style="font-size:16px; font-weight:bold;">{trans_item['date']}</td><th>طريقة السداد</th><td><strong>{trans_item['method']}</strong></td></tr>
                <tr><th>{party_label}</th><td colspan="3"><strong style="font-size:18px; color:#1E3A8A;">{trans_item['party']}</strong></td></tr>
                <tr><th>المبلغ المسدد بالسند</th><td colspan="3"><div class="amt-tag">{amt_val:,.2f} ريال سعودي</div></td></tr>
                <tr><th>البيان والملاحظات</th><td colspan="3" style="font-size:15px;">{trans_item.get('notes', 'سداد بموجب السند المعمد بالنظام')}</td></tr>
            </table>
            <div class="sigs">
                <div>توقيع المستلم / الجهة: __________________</div>
                <div>توقيع أمين الصندوق / المحاسب: __________________</div>
            </div>
        </div>
    </body></html>
    """
    st.components.v1.html(html_v, height=480, scrolling=True)

@st.dialog("✏️ تعديل حركة الصندوق")
def edit_cash_modal(month_name, trans_idx, target_box="main"):
    all_cash = load_cash_data()
    m_cash = all_cash.get(month_name, {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []})
    box_key = 'transactions' if target_box == 'main' else 'acc_transactions'
    trans_list = m_cash.get(box_key, [])
    
    if trans_idx < len(trans_list):
        curr_item = trans_list[trans_idx]
        st.write(f"تعديل السند رقم: **#{curr_item.get('code', curr_item['id'])}**")
        with st.form("edit_cash_item_form"):
            e_type = st.selectbox("نوع الحركة:", ["سند قبض / إيراد", "سند صرف / مصروف"], index=["سند قبض / إيراد", "سند صرف / مصروف"].index(curr_item['type']))
            e_party = st.text_input("اسم الجهة / البيان:", value=curr_item['party'])
            e_amt = st.number_input("المبلغ (ر.س):", min_value=0.0, value=float(curr_item['amount']))
            e_method = st.selectbox("طريقة الدفع:", ["نقداً بالصندوق", "تحويل بنكي", "شيك"], index=["نقداً بالصندوق", "تحويل بنكي", "شيك"].index(curr_item['method']))
            e_notes = st.text_input("الملاحظات / الفاتورة:", value=curr_item.get('notes', ''))
            
            sub_e_cash = st.form_submit_button("💾 حفظ التعديل")
            if sub_e_cash:
                trans_list[trans_idx]['type'] = e_type
                trans_list[trans_idx]['party'] = e_party
                trans_list[trans_idx]['amount'] = e_amt
                trans_list[trans_idx]['method'] = e_method
                trans_list[trans_idx]['notes'] = e_notes
                all_cash[month_name][box_key] = trans_list
                save_cash_data(all_cash)
                st.success("تم التعديل بنجاح!")
                st.rerun()

@st.dialog("➕ إضافة موظف جديد")
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
            
        sub_btn = st.form_submit_button("💾 حفظ وإضافة الموظف")
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
                save_data(st.session_state.payroll_df)
                st.success(f"تمت إضافة ({new_name}) بنجاح!")
                st.rerun()

@st.dialog("👤 تعديل ملف الموظف")
def edit_employee_dialog(emp_idx, month_selected):
    emp_data = st.session_state.payroll_df.loc[emp_idx]
    st.write(f"تعديل الموظف: **{emp_data['الاسم']}** (كود: #{emp_data['م']})")
    
    with st.form(f'edit_modal_{emp_data["م"]}'):
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.markdown("### 👤 البيانات الإدارية")
            up_name = st.text_input("اسم الموظف الثلاثي:", value=emp_data['الاسم'])
            up_job = st.text_input("الوظيفة:", value=emp_data['الوظيفة'])
            up_branch = st.selectbox("الفرع التابع له:", [
                'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'
            ], index=['مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'].index(emp_data['الفرع']))
            
        with col_e2:
            st.markdown("### 💰 المالية (" + month_selected + ")")
            up_salary = st.number_input("الراتب الأساسي (ر.س):", min_value=0.0, value=float(emp_data['الراتب الأساسي']))
            up_pay1 = st.number_input("الدفعة 1 (ر.س):", min_value=0.0, value=float(emp_data.get('الدفعة 1', 0)))
            up_pay2 = st.number_input("الدفعة 2 (ر.س):", min_value=0.0, value=float(emp_data.get('الدفعة 2', 0)))
            up_ded = st.number_input("الخصومات (ر.س):", min_value=0.0, value=float(emp_data.get('الخصومات', 0)))
            up_action = st.selectbox("نوع الإجراء:", ["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"], index=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"].index(emp_data['نوع الإجراء']))
            up_notes = st.text_input("الملاحظات:", value=emp_data['الملاحظات'])
            
        with col_e3:
            st.markdown("### 📄 التواريخ والوثائق")
            st_val = datetime.strptime(str(emp_data.get('تاريخ بداية العمل', '2024-01-01')), '%Y-%m-%d')
            iq_val = datetime.strptime(str(emp_data['تاريخ انتهاء الإقامة']), '%Y-%m-%d') if pd.notnull(emp_data['تاريخ انتهاء الإقامة']) else datetime(2027, 12, 31)
            ct_val = datetime.strptime(str(emp_data['تاريخ انتهاء العقد']), '%Y-%m-%d') if pd.notnull(emp_data['تاريخ انتهاء العقد']) else datetime(2027, 12, 31)
            
            up_start_date = st.date_input("تاريخ بداية العمل:", st_val)
            up_iqama_date = st.date_input("تاريخ انتهاء الإقامة:", iq_val)
            up_contract_date = st.date_input("تاريخ انتهاء العقد:", ct_val)
            
        st.divider()
        save_btn = st.form_submit_button('💾 حفظ وتحديث البيانات')
        
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
            
            save_data(st.session_state.payroll_df)
            st.success("تم الحفظ بنجاح!")
            st.rerun()

    with st.expander(f"⚠️ حذف الموظف ({emp_data['الاسم']})"):
        if st.button(f"🗑️ تأكيد الحذف النهائياً", key=f"del_modal_{emp_data['م']}"):
            st.session_state.payroll_df = st.session_state.payroll_df.drop(emp_idx).reset_index(drop=True)
            save_data(st.session_state.payroll_df)
            st.success("تم الحذف!")
            st.rerun()

# 2. الشاشة الافتتاحية
if not st.session_state.get('app_started', False):
    st.markdown("""
        <div class="welcome-card-lux">
            <div class="logo-lux">5M</div>
            <div class="title-company-huge">شركة ميم الخماسية للتصنيع</div>
            <p style="color: #94A3B8 !important; font-size: 17px; margin-bottom: 20px;">النظام المحاسبي والإداري الموحد</p>
            <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.2); margin: 25px 0;">
        </div>
    """, unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1])
    with col_b2:
        st.markdown("<h3 style='text-align:center;'>🔑 تسجيل الدخول:</h3>", unsafe_allow_html=True)
        
        username_selected = st.selectbox("المستخدم:", ["wahby", "omar"], key="login_username_select")
        pwd_input = st.text_input("كلمة المرور:", type="password", key="login_pwd")
        
        if st.button('🚀 الدخول للنظام', use_container_width=True):
            if username_selected == "wahby":
                if pwd_input == ADMIN_PASSWORD or pwd_input == "":
                    st.session_state.app_started = True
                    st.session_state.user_role = "admin"
                    st.success("أهلاً بك (wahby)!")
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة!")
            elif username_selected == "omar":
                if pwd_input == USER_PASSWORD or pwd_input == "":
                    st.session_state.app_started = True
                    st.session_state.user_role = "accountant"
                    st.success("أهلاً بك (omar)!")
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة!")

else:
    # 3. القائمة الجانبية ملمومة ومضغوطة لرفع السكرول
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding-bottom: 5px;">
                <div style="font-size: 45px; font-weight: 900; color: #EF4444; line-height: 1; font-family: Arial;">5M</div>
                <h3 style="color: #1E3A8A; margin-top: 2px; font-size: 16px; font-weight: bold;">شركة ميم الخماسية للتصنيع</h3>
            </div>
        """, unsafe_allow_html=True)

        role_label = "wahby" if st.session_state.user_role == "admin" else "omar"
        st.info(f"المستخدم: **{role_label}**")

        if 'months_list' not in st.session_state:
            st.session_state.months_list = ['أغسطس 2026', 'سبتمبر 2026', 'أكتوبر 2026', 'نوفمبر 2026', 'ديسمبر 2026']
            
        month_selected = st.selectbox('📅 الشهر الحالي:', st.session_state.months_list)

        st.session_state['theme_mode'] = st.selectbox("🎨 نمط الألوان:", ["🌙 وضع ليلي", "☀️ وضع نهاري"], index=0 if "🌙" in st.session_state['theme_mode'] else 1)

        if st.button("🏠 لوحة التحكم الرئيسية", use_container_width=True):
            st.session_state['current_view'] = '🏠 الرئيسية'
            st.rerun()

        st.markdown("### 📌 القوائم والتطبيقات:")

        with st.expander("🏦 حركة الصندوق"):
            if st.button("💵 حركة الصندوق والسندات", use_container_width=True):
                st.session_state['current_view'] = '💵 حركة الصندوق والسندات'
                st.rerun()

        if st.session_state.user_role == "admin":
            with st.expander("👥 الموظفين"):
                if st.button("👤 دليل الموظفين", use_container_width=True):
                    st.session_state['current_view'] = '👤 دليل الموظفين'
                    st.rerun()
                if st.button("🇸🇦 حاسبة نهاية الخدمة", use_container_width=True):
                    st.session_state['current_view'] = '🇸🇦 حاسبة نهاية الخدمة'
                    st.rerun()
                if st.button("🔔 تنبيهات الإقامات والعقود", use_container_width=True):
                    st.session_state['current_view'] = '🔔 تنبيهات الإقامات والعقود'
                    st.rerun()
            
            with st.expander("💰 المرتبات والدفعات", expanded=True):
                if st.button("📊 إدخال الدفعات السريع", use_container_width=True):
                    st.session_state['current_view'] = '📊 إدخال الدفعات السريع'
                    st.rerun()
                if st.button("📋 مسير الرواتب الشهري", use_container_width=True):
                    st.session_state['current_view'] = '📋 مسير الرواتب الشهري'
                    st.rerun()
            
            with st.expander("📑 التقارير والسندات"):
                if st.button("🖨️ طباعة السندات الرسمية (A4)", use_container_width=True):
                    st.session_state['current_view'] = '🖨️ طباعة السندات الرسمية (A4)'
                    st.rerun()

            # تصميم مبسط وعالي الوضوح للنسخ الاحتياطي بدون أزرار متداخلة
            with st.expander("💾 النسخ الاحتياطي والأرشيف", expanded=True):
                if 'payroll_df' in st.session_state:
                    json_str = st.session_state.payroll_df.to_json(orient='records', force_ascii=False, indent=4)
                    st.download_button(
                        label="📥 تنزيل نسخة احتياطية",
                        data=json_str.encode('utf-8'),
                        file_name=f"payroll_backup_{month_selected}.json",
                        mime="application/json",
                        use_container_width=True,
                        key="dl_backup_sidebar"
                    )
                st.write("**📤 استيراد ورفع نسخة:**")
                uploaded_backup = st.file_uploader("", type=['json'], key="side_uploader_backup_clean")
                if uploaded_backup:
                    try:
                        imported_df = pd.DataFrame(json.load(uploaded_backup))
                        st.session_state.payroll_df = imported_df
                        save_data(imported_df)
                        st.success("تم استيراد البيانات بنجاح!")
                        st.rerun()
                    except Exception:
                        st.error("خطأ في القراءة.")

            with st.expander("⚙️ السنة المالية والإعدادات"):
                if st.button("🏁 الإغلاق السنوي وسنة جديدة", use_container_width=True):
                    st.session_state['current_view'] = '🏁 الإغلاق السنوي وسنة جديدة'
                    st.rerun()

        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            st.session_state.app_started = False
            st.session_state.user_role = None
            st.rerun()

        selected_option = st.session_state.get('current_view', '🏠 الرئيسية')

    if 'payroll_df' not in st.session_state or st.session_state.get('current_month') != month_selected:
        st.session_state.current_month = month_selected
        st.session_state.payroll_df = load_data()

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
    
    st.markdown(f'<div style="text-align: center;"><div class="date-badge-lux">{date_formatted}</div></div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="company-header-inner">
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
    if selected_option == '🏠 الرئيسية':
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

        st.markdown(f"### 🏦 ملخص الصندوق والعُهد - {month_selected}")
        
        if st.session_state.user_role == "admin":
            c_box1, c_box2, c_box3 = st.columns(3)
            with c_box1:
                st.markdown("#### 🏢 الخزينة الرئيسية (wahby):")
                st.metric("رصيد الخزينة الرئيسية", f"{net_main_now:,.2f} ر.س")
            with c_box2:
                st.markdown("#### 👤 عُهدة المحاسب (omar):")
                st.metric("رصيد عُهدة omar", f"{net_acc_now:,.2f} ر.س")
            with c_box3:
                st.markdown("#### 💳 إجمالي نقدية الشركة:")
                st.metric("مجموع الصناديق", f"{total_company_cash:,.2f} ر.س")

            st.divider()

            st.markdown("### 👥 مؤشرات الرواتب والعمالة")
            st_col1, st_col2, st_col3, st_col4, st_col5, st_col6 = st.columns(6)
            st_col1.metric("👥 العمالة", f"{tot_emp} موظف")
            st_col2.metric("💰 الرواتب", f"{tot_req:,.0f} ر.س")
            st_col3.metric("💵 الدفعة 1", f"{tot_p1_all:,.0f} ر.س")
            st_col4.metric("💵 الدفعة 2", f"{tot_p2_all:,.0f} ر.س")
            st_col5.metric("✂️ الخصومات", f"{tot_ded_all:,.0f} ر.س")
            st_col6.metric("⏳ المتبقي", f"{tot_rem:,.0f} ر.س")
        else:
            st.markdown("#### 👤 عُهدتك الحالية (omar):")
            st.metric("الرصيد المتبقي بعُهدتك", f"{net_acc_now:,.2f} ر.س")

        st.divider()

        st.markdown("### ⚡ إجراءات خاطفة")
        
        if st.session_state.user_role == "admin":
            q_col1, q_col2, q_col3, q_col4 = st.columns(4)
            with q_col1:
                st.markdown('<div class="daftra-quick-card"><h3>👤</h3><h4>إضافة موظف</h4></div>', unsafe_allow_html=True)
                if st.button("➕ إضافة موظف", use_container_width=True, key="q_btn_add_emp"):
                    add_employee_dialog('مصنع ميم الخماسية الخرج')

            with q_col2:
                st.markdown('<div class="daftra-quick-card"><h3>🟢</h3><h4>سند قبض</h4></div>', unsafe_allow_html=True)
                if st.button("💵 سند قبض سريع", use_container_width=True, key="q_btn_rec"):
                    quick_cash_voucher_dialog("قبض", month_selected, "main")

            with q_col3:
                st.markdown('<div class="daftra-quick-card"><h3>🔴</h3><h4>سند صرف</h4></div>', unsafe_allow_html=True)
                if st.button("💸 سند صرف سريع", use_container_width=True, key="q_btn_pay"):
                    quick_cash_voucher_dialog("صرف", month_selected, "main")

            with q_col4:
                st.markdown('<div class="daftra-quick-card"><h3>💾</h3><h4>نسخة احتياطية</h4></div>', unsafe_allow_html=True)
                if 'payroll_df' in st.session_state:
                    json_str_main = st.session_state.payroll_df.to_json(orient='records', force_ascii=False, indent=4)
                    st.download_button(
                        label="📥 تنزيل نسخة فوراً",
                        data=json_str_main.encode('utf-8'),
                        file_name=f"payroll_backup_{month_selected}.json",
                        mime="application/json",
                        use_container_width=True,
                        key="quick_backup_btn_main"
                    )
        else:
            q_col2, q_col3 = st.columns(2)
            with q_col2:
                st.markdown('<div class="daftra-quick-card"><h3>🟢</h3><h4>سند قبض</h4></div>', unsafe_allow_html=True)
                if st.button("💵 سند قبض سريع", use_container_width=True, key="q_btn_rec"):
                    quick_cash_voucher_dialog("قبض", month_selected, "accountant")

            with q_col3:
                st.markdown('<div class="daftra-quick-card"><h3>🔴</h3><h4>سند صرف</h4></div>', unsafe_allow_html=True)
                if st.button("💸 سند صرف سريع", use_container_width=True, key="q_btn_pay"):
                    quick_cash_voucher_dialog("صرف", month_selected, "accountant")

    elif selected_option == '📊 إدخال الدفعات السريع' and st.session_state.user_role == "admin":
        st.subheader(f'📊 جدول إدخال وتعديل الدفعات السريع - ({month_selected})')
        
        t1, t2, t3, t4 = st.tabs(['📍 مصنع الخرج', '📍 مستودع الخرج', '📍 مستودع الرياض', '📍 رواتب متنوعة'])
        branches = [('مصنع ميم الخماسية الخرج', t1), ('مستودع ميم الخماسية الخرج', t2), ('مستودع ميم الخماسية الرياض', t3), ('رواتب متنوعة', t4)]
        
        for b_name, tab_obj in branches:
            with tab_obj:
                col_auto1, col_auto2 = st.columns([2, 1])
                with col_auto1:
                    if st.button(f'⚡ توزيع المتبقي كـ "دفعة 2" تلقائياً ({b_name})', key=f"auto_btn_{b_name}"):
                        for idx, row in st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].iterrows():
                            req_s = row['الراتب الأساسي']
                            p1 = row.get('الدفعة 1', 0)
                            ded = row.get('الخصومات', 0)
                            rem_needed = max(0, req_s - (p1 + ded))
                            st.session_state.payroll_df.loc[idx, 'الدفعة 2'] = rem_needed
                            st.session_state.payroll_df.loc[idx, 'الدفعة المدفوعة'] = p1 + rem_needed
                            st.session_state.payroll_df.loc[idx, 'المتبقي'] = 0.0
                        save_data(st.session_state.payroll_df)
                        st.success("تم التوزيع وتصفير المتبقي!")
                        st.rerun()

                df_b = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].copy()
                
                cols_rtl = ['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'الدفعة 1', 'الدفعة 2', 'الخصومات', 'نوع الإجراء', 'الملاحظات']
                edited_b = st.data_editor(
                    df_b[cols_rtl],
                    column_config={
                        "م": st.column_config.NumberColumn("مسلسل", disabled=True),
                        "الاسم": st.column_config.TextColumn("اسم الموظف"),
                        "الوظيفة": st.column_config.TextColumn("الوظيفة"),
                        "الراتب الأساسي": st.column_config.NumberColumn("الراتب المستحق", min_value=0, format="%d ر.س"),
                        "الدفعة 1": st.column_config.NumberColumn("الدفعة 1", min_value=0, format="%d ر.س"),
                        "الدفعة 2": st.column_config.NumberColumn("الدفعة 2", min_value=0, format="%d ر.س"),
                        "الخصومات": st.column_config.NumberColumn("الخصومات", min_value=0, format="%d ر.س"),
                        "نوع الإجراء": st.column_config.SelectboxColumn("نوع الإجراء", options=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"]),
                        "الملاحظات": st.column_config.TextColumn("الملاحظات")
                    },
                    use_container_width=True,
                    hide_index=True,
                    key=f"ed_{b_name}_{month_selected}"
                )
                
                if st.button(f"💾 حفظ التعديلات ({b_name})", key=f"btn_save_ed_{b_name}"):
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
                        st.session_state.payroll_df.loc[target_idx, 'نوع الإجراء'] = row['نوع الإجراء']
                        st.session_state.payroll_df.loc[target_idx, 'الملاحظات'] = row['الملاحظات']
                    
                    save_data(st.session_state.payroll_df)
                    st.success("تم الحفظ بنجاح!")
                    st.rerun()

                b_tot_req = edited_b['الراتب الأساسي'].sum()
                b_tot_p1 = edited_b['الدفعة 1'].sum()
                b_tot_p2 = edited_b['الدفعة 2'].sum()
                b_tot_ded = edited_b['الخصومات'].sum()
                b_tot_rem = b_tot_req - (b_tot_p1 + b_tot_p2 + b_tot_ded)

                st.divider()
                st.markdown(f"#### 📊 الملخص المالي لفرع ({b_name}):")
                s_col1, s_col2, s_col3, s_col4, s_col5 = st.columns(5)
                s_col1.metric("إجمالي الرواتب", f"{b_tot_req:,.0f} ر.س")
                s_col2.metric("إجمالي الدفعة 1", f"{b_tot_p1:,.0f} ر.س")
                s_col3.metric("إجمالي الدفعة 2", f"{b_tot_p2:,.0f} ر.س")
                s_col4.metric("إجمالي الخصومات", f"{b_tot_ded:,.0f} ر.س")
                s_col5.metric("إجمالي المتبقي", f"{b_tot_rem:,.0f} ر.س")

    elif selected_option == '💵 حركة الصندوق والسندات':
        st.subheader(f'🏦 إدارة حركة الصندوق - ({month_selected})')
        
        all_cash_db = load_cash_data()
        if month_selected not in all_cash_db:
            all_cash_db[month_selected] = {'opening': 0.0, 'transactions': [], 'acc_opening': 0.0, 'acc_transactions': []}
            
        current_m_cash = all_cash_db[month_selected]
        
        if st.session_state.user_role == "admin":
            box_selected = st.radio("اختر الصندوق:", ["🏢 الخزينة الرئيسية (wahby)", "👤 عُهدة المحاسب (omar)"], horizontal=True)
            active_box_key = 'transactions' if "wahby" in box_selected else 'acc_transactions'
            active_opening_key = 'opening' if "wahby" in box_selected else 'acc_opening'
        else:
            active_box_key = 'acc_transactions'
            active_opening_key = 'acc_opening'
            st.info("أنت تعمل على شاشة **عُهدتك المالية (omar)**.")

        opening_bal = current_m_cash.get(active_opening_key, 0.0)

        with st.expander("⚙️ تعديل الرصيد الافتتاحي للصندوق", expanded=False):
            with st.form("set_opening_balance_form"):
                new_opening_val = st.number_input("الرصيد الافتتاحي (ر.س):", min_value=0.0, value=float(opening_bal))
                sub_op = st.form_submit_button("💾 تثبيت الرصيد الافتتاحي")
                if sub_op:
                    current_m_cash[active_opening_key] = new_opening_val
                    all_cash_db[month_selected] = current_m_cash
                    save_cash_data(all_cash_db)
                    st.success("تم التثبيت!")
                    st.rerun()

        curr_trans = current_m_cash.get(active_box_key, [])
        tot_cash_in = sum(t['amount'] for t in curr_trans if 'قبض' in t['type'])
        tot_cash_out = sum(t['amount'] for t in curr_trans if 'صرف' in t['type'])
        net_cash_now = opening_bal + tot_cash_in - tot_cash_out

        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        c_m1.metric("💵 رصيد أول الشهر", f"{opening_bal:,.2f} ر.س")
        c_m2.metric("🟢 المقبوضات", f"{tot_cash_in:,.2f} ر.س")
        c_m3.metric("🔴 المصروفات", f"{tot_cash_out:,.2f} ر.س")
        c_m4.metric("🏦 المتبقي بالصندوق", f"{net_cash_now:,.2f} ر.س")

        st.divider()

        col_c_in1, col_c_in2 = st.columns([1, 1.8])
        with col_c_in1:
            st.markdown("### 📝 تسجيل حركة بالصندوق:")
            with st.form("add_cash_transaction_form"):
                trans_type = st.selectbox("نوع الحركة:", ["سند قبض / إيراد", "سند صرف / مصروف"])
                trans_party = st.text_input("اسم الجهة / البيان:", placeholder="مثلاً: العميل / شراء مواد خام")
                trans_amt = st.number_input("المبلغ (ر.س):", min_value=0.0, value=0.0)
                trans_pay_method = st.selectbox("طريقة السداد:", ["نقداً بالصندوق", "تحويل بنكي", "شيك"])
                trans_notes = st.text_input("ملاحظات / الفاتورة:")
                
                sub_cash = st.form_submit_button("💾 حفظ الحركة")
                if sub_cash:
                    if trans_party and trans_amt > 0:
                        rec_cnt = sum(1 for t in curr_trans if "قبض" in t['type'])
                        pay_cnt = sum(1 for t in curr_trans if "صرف" in t['type'])
                        v_code = f"REC-{(rec_cnt + 1):03d}" if "قبض" in trans_type else f"PAY-{(pay_cnt + 1):03d}"
                        
                        new_trans = {
                            'id': len(curr_trans) + 1,
                            'code': v_code,
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'type': trans_type,
                            'party': trans_party,
                            'amount': trans_amt,
                            'method': trans_pay_method,
                            'notes': trans_notes
                        }
                        curr_trans.append(new_trans)
                        all_cash_db[month_selected][active_box_key] = curr_trans
                        save_cash_data(all_cash_db)
                        st.success(f"تم التسجيل برقم #{v_code}!")
                        st.rerun()

        with col_c_in2:
            st.markdown("### 📑 دفتر يومية الصندوق:")
            if curr_trans:
                cf1, cf2 = st.columns([2, 1])
                with cf1:
                    cash_search = st.text_input("🔍 استعلام بالبيان:", key="search_cash_input")
                with cf2:
                    cash_filter_type = st.selectbox("تصفية بالحركة:", ["جميع الحركات", "سند قبض / إيراد", "سند صرف / مصروف"], key="filter_cash_type")

                filtered_cash = curr_trans.copy()
                if cash_search:
                    filtered_cash = [t for t in filtered_cash if cash_search.lower() in t['party'].lower()]
                if cash_filter_type != "جميع الحركات":
                    filtered_cash = [t for t in filtered_cash if t['type'] == cash_filter_type]

                items_per_page = 10
                total_items = len(filtered_cash)
                total_pages = (total_items + items_per_page - 1) // items_per_page if total_items > 0 else 1
                
                page_num = st.number_input(f"الصفحة (من أصل {total_pages}):", min_value=1, max_value=total_pages, value=1, step=1, key="cash_pg_num")
                start_idx = (page_num - 1) * items_per_page
                end_idx = start_idx + items_per_page
                page_trans = filtered_cash[start_idx:end_idx]

                st.write(f"عرض الحركات من **{start_idx+1}** إلى **{min(end_idx, total_items)}** (من أصل {total_items}):")
                for t_idx, t_item in enumerate(page_trans):
                    real_idx = curr_trans.index(t_item)
                    tc1, tc2, tc3, tc4, tc5, tc6 = st.columns([0.8, 2.0, 1.4, 0.9, 0.9, 0.9])
                    tc1.write(f"#{t_item.get('code', t_item['id'])}")
                    
                    t_color = "#047857" if "قبض" in t_item['type'] else "#B91C1C"
                    tc2.write(f"**{t_item['party']}**  \n<span style='color:{t_color}; font-size:12px;'>{t_item['type']}</span>", unsafe_allow_html=True)
                    tc3.write(f"💵 **{t_item['amount']:,.2f} ر.س**")
                    
                    if tc4.button("🖨️ طباعة", key=f"btn_p_cash_{real_idx}"):
                        print_cash_voucher_dialog(t_item, month_selected)

                    if tc5.button("✏️ تعديل", key=f"btn_e_cash_{real_idx}"):
                        box_type = "main" if active_box_key == "transactions" else "accountant"
                        edit_cash_modal(month_selected, real_idx, box_type)
                        
                    if tc6.button("🗑️ حذف", key=f"btn_d_cash_{real_idx}"):
                        curr_trans.pop(real_idx)
                        all_cash_db[month_selected][active_box_key] = curr_trans
                        save_cash_data(all_cash_db)
                        st.success("تم الحذف!")
                        st.rerun()
                    st.divider()
            else:
                st.info("لا توجد حركات تسوية بالصندوق مسجلة لهذا الشهر.")

    elif selected_option == '👤 دليل الموظفين' and st.session_state.user_role == "admin":
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
                if c_card4.button("✏️ تعديل", key=f"btn_s_edit_{e_row['م']}"):
                    edit_employee_dialog(e_idx, month_selected)
                st.divider()
        else:
            cnt_factory = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'مصنع ميم الخماسية الخرج'])
            cnt_wh_kh = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'مستودع ميم الخماسية الخرج'])
            cnt_wh_ry = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'مستودع ميم الخماسية الرياض'])
            cnt_misc = len(st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == 'رواتب متنوعة'])
            
            tab_search_list = [
                (f'🏭 مصنع الخرج ({cnt_factory})', 'مصنع ميم الخماسية الخرج'),
                (f'📦 مستودع الخرج ({cnt_wh_kh})', 'مستودع ميم الخماسية الخرج'),
                (f'🏙️ مستودع الرياض ({cnt_wh_ry})', 'مستودع ميم الخماسية الرياض'),
                (f'📋 رواتب متنوعة ({cnt_misc})', 'رواتب متنوعة')
            ]
            
            search_tabs = st.tabs([t[0] for t in tab_search_list])
            
            for idx_st, (s_title, b_name) in enumerate(tab_search_list):
                with search_tabs[idx_st]:
                    col_h1, col_h2 = st.columns([3, 1])
                    with col_h1:
                        st.write(f"دليل موظفي **{b_name}**:")
                    with col_h2:
                        if st.button(f"➕ إضافة موظف لـ {b_name}", key=f"btn_modal_add_{b_name}"):
                            add_employee_dialog(b_name)

                    branch_df_search = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name]
                    
                    if not branch_df_search.empty:
                        for e_idx, e_row in branch_df_search.iterrows():
                            c_card1, c_card2, c_card3, c_card4 = st.columns([2, 1.5, 1.5, 1])
                            c_card1.write(f"👤 **{e_row['الاسم']}** ({e_row['الوظيفة']})")
                            c_card2.write(f"💵 الراتب: **{e_row['الراتب الأساسي']:,.0f} ر.س**")
                            c_card3.write(f"📅 بداية العمل: {e_row.get('تاريخ بداية العمل', '2024-01-01')}")
                            
                            if c_card4.button("✏️ تعديل", key=f"btn_edit_m_{e_row['م']}"):
                                edit_employee_dialog(e_idx, month_selected)
                            st.divider()
                    else:
                        st.info(f"لا يوجد موظفين حالياً في {b_name}.")

    elif selected_option == '📋 مسير الرواتب الشهري' and st.session_state.user_role == "admin":
        st.subheader(f'📋 كشف مسير الرواتب الشهري الموحد - ({month_selected})')
        filter_sheet = st.selectbox('اختر الفرع للكشف:', ['جميع الفروع (الكشف الموحد)', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'])
        df_sheet = st.session_state.payroll_df if 'جميع الفروع' in filter_sheet else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == filter_sheet]
        
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
            @media print {{ .no-print {{ display: none; }} }}
        </style>
        </head>
        <body>
            <div class="no-print" style="text-align:center; padding: 10px; margin-bottom: 15px;">
                <button onclick="window.print()" style="background: #1E3A8A; color: white; border: none; padding: 10px 25px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer;">🖨️ طباعة المسير (PDF)</button>
            </div>
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
        st.components.v1.html(sheet_html, height=450, scrolling=True)
        st.download_button(
            label=f"📄 فتح وتحميل ملف كشف مسير {filter_sheet} (HTML / PDF) 🖨️",
            data=sheet_html.encode('utf-8'),
            file_name=f"مسير_رواتب_{filter_sheet}_{month_selected}.html",
            mime="text/html"
        )

    elif selected_option == '🖨️ طباعة السندات الرسمية (A4)' and st.session_state.user_role == "admin":
        st.subheader(f'🖨️ طباعة سندات القبض والصرف الرسمية A4 - ({month_selected})')
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            selected_b = st.selectbox('اختر الفرع:', ['جميع الفروع', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'], key="sb_v_b")
        with col_p2:
            pay_type_select = st.selectbox('اختر نوع الدفعة:', ['جميع الدفعات (السند الشامل)', 'الدفعة الأولى فقط', 'الدفعة الثانية فقط'], key="sb_v_type")
            
        df_print = st.session_state.payroll_df if selected_b == 'جميع الفروع' else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == selected_b]
        
        pdf_bytes = generate_pretty_html_pdf(df_print, selected_b, pay_type_select)
        st.components.v1.html(pdf_bytes.getvalue().decode('utf-8'), height=450, scrolling=True)
        st.download_button(
            label=f"📄 تنزيل ملف سندات ({pay_type_select}) - {selected_b} للطباعة 🖨️",
            data=pdf_bytes,
            file_name=f"سندات_{pay_type_select}_{selected_b}_{month_selected}.html",
            mime="text/html"
        )

    elif selected_option == '🇸🇦 حاسبة نهاية الخدمة' and st.session_state.user_role == "admin":
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

    elif selected_option == '🔔 تنبيهات الإقامات والعقود' and st.session_state.user_role == "admin":
        st.subheader('🔔 مركز تنبيهات انتهاء الإقامات وعقود العمل')
        today = datetime.now().date()
        alerts = []
        for _, r in st.session_state.payroll_df.iterrows():
            try:
                iq_d = datetime.strptime(str(r.get('تاريخ انتهاء الإقامة')), '%Y-%m-%d').date()
                ct_d = datetime.strptime(str(r.get('تاريخ انتهاء العقد')), '%Y-%m-%d').date()
                if iq_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '🆔 إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🔴 منتهية'})
                elif (iq_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '🆔 إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🟡 تنتهي قريباً'})
                if ct_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '📄 عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🔴 منتهي'})
                elif (ct_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '📄 عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🟡 ينتهي قريباً'})
            except: pass
        if alerts: st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
        else: st.success('جميع الإقامات والعقود سارية ولا يوجد وثائق منتهية حالياً!')

    elif selected_option == '🏁 الإغلاق السنوي وسنة جديدة' and st.session_state.user_role == "admin":
        st.subheader('🏁 شاشة الإغلاق المالي السنوي وفتح سنة جديدة')
        st.markdown("### 📊 ملخص الرواتب والدفعات الكلية بالسجلات:")
        st.dataframe(st.session_state.payroll_df[['م', 'الاسم', 'الوظيفة', 'الفرع', 'الراتب الأساسي', 'الخصومات', 'الدفعة المدفوعة', 'المتبقي']], use_container_width=True, hide_index=True)
        
        st.divider()
        st.markdown("### ⚙️ فتح سنة جديدة:")
        col_y1, col_y2 = st.columns(2)
        with col_y1:
            next_year_name = st.text_input("السنة المالية الجديدة:", "2027")
        with col_y2:
            st.write("")
            st.write("")
            if st.button(f"🏁 إغلاق السنة المالية الحالية وفتح سنة ({next_year_name})"):
                st.session_state.payroll_df['الخصومات'] = 0.0
                st.session_state.payroll_df['الدفعة 1'] = 0.0
                st.session_state.payroll_df['الدفعة 2'] = 0.0
                st.session_state.payroll_df['الدفعة المدفوعة'] = 0.0
                st.session_state.payroll_df['المتبقي'] = st.session_state.payroll_df['الراتب الأساسي']
                st.session_state.payroll_df['نوع الإجراء'] = 'لم يُصرف'
                
                st.session_state.months_list = [f'يناير {next_year_name}', f'فبراير {next_year_name}', f'مارس {next_year_name}', f'أبريل {next_year_name}']
                save_data(st.session_state.payroll_df)
                st.success(f"تم إغلاق السنة الحالية وافتتاح سنة ({next_year_name}) بنجاح!")
                st.rerun()
