import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title='شركة ميم الخماسية للتصنيع - إدارة الرواتب والـ HR', layout='wide', page_icon='🏢')

# إدارة حالة الشاشة الافتتاحية
if 'app_started' not in st.session_state:
    st.session_state.app_started = False

if not st.session_state.app_started:
    st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%); color: white; }
            .welcome-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 40px; text-align: center; margin-top: 50px; }
            .logo-header { font-size: 70px; font-weight: 900; color: #EF4444; letter-spacing: -2px; font-family: Arial, sans-serif; }
            .title-ar { font-size: 32px; font-weight: bold; color: #FFFFFF; margin-top: 10px; }
            .subtitle-ar { font-size: 18px; color: #94A3B8; margin-bottom: 30px; }
        </style>
        <div class="welcome-card">
            <div class="logo-header">5M</div>
            <div class="title-ar">🏢 شركة ميم الخماسية للتصنيع</div>
            <div class="subtitle-ar">النظام المحاسبي والإداري الشامل للرواتب وإدارة وثائق الموظفين</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1])
    with col_b2:
        st.write("")
        if st.button('🚀 الدخول للنظام الإداري والمالي', use_container_width=True):
            st.session_state.app_started = True
            st.rerun()

else:
    # القائمة الجانبية والشهر
    with st.sidebar:
        st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🏢 شركة ميم الخماسية</h2>', unsafe_allow_html=True)
        st.divider()
        menu = st.radio('📌 التنقل الرئيسي:', [
            '🔍 بحث وتعديل ملف موظف',
            '📊 شاشة إدخال الدفعات (حسب الفرع)',
            '💼 سجل الموظفين وتدقيق الوثائق',
            '➕ إضافة موظف جديد للنظام',
            '📈 شاشة التقارير وإدارة التجديدات',
            '📑 مسير الرواتب الشهري (معاينة وطباعة)',
            '🖨️ طباعة سندات القبض (PDF A4)'
        ])
        st.divider()
        
        if 'months_list' not in st.session_state:
            st.session_state.months_list = ['أغسطس 2026', 'سبتمبر 2026', 'أكتوبر 2026', 'نوفمبر 2026']
            
        month_selected = st.selectbox('📅 اختر شهر العمليات:', st.session_state.months_list)
        
        st.markdown("---")
        with st.expander("➕ إضافة شهر جديد"):
            new_m_input = st.text_input("اسم الشهر الجديد:", placeholder="مثلاً: ديسمبر 2026")
            if st.button("تأكيد إضافة الشهر"):
                if new_m_input and new_m_input not in st.session_state.months_list:
                    st.session_state.months_list.append(new_m_input)
                    st.success(f"تم إضافة {new_m_input} بنجاح!")
                    st.rerun()

    # قاعدة البيانات الأساسية لجميع الموظفين (52 موظف)
    initial_data = [
        # مصنع ميم الخماسية الخرج (35 موظف)
        {'م': 1, 'الاسم': 'مد ماجد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-15', 'تاريخ انتهاء العقد': '2027-01-01'},
        {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-09-20', 'تاريخ انتهاء العقد': '2026-12-31'},
        {'م': 3, 'الاسم': 'أيوب', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-08-01', 'تاريخ انتهاء العقد': '2026-11-15'},
        {'م': 4, 'الاسم': 'ذاكر حسين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-10', 'تاريخ انتهاء العقد': '2027-05-20'},
        {'م': 5, 'الاسم': 'رفيق الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 1600, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-01-10', 'تاريخ انتهاء العقد': '2027-03-01'},
        {'م': 6, 'الاسم': 'رحيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-20', 'تاريخ انتهاء العقد': '2027-02-01'},
        {'م': 7, 'الاسم': 'محي الدين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-04-15', 'تاريخ انتهاء العقد': '2027-06-01'},
        {'م': 8, 'الاسم': 'محمد ريان', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-02-01', 'تاريخ انتهاء العقد': '2027-04-01'},
        {'م': 9, 'الاسم': 'مدلايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-12-01', 'تاريخ انتهاء العقد': '2027-01-15'},
        {'م': 10, 'الاسم': 'عالم روبيل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-05-10', 'تاريخ انتهاء العقد': '2027-07-01'},
        {'م': 11, 'الاسم': 'شوقي كامل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-30', 'تاريخ انتهاء العقد': '2027-01-01'},
        {'م': 12, 'الاسم': 'عمرو فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-01', 'تاريخ انتهاء العقد': '2027-05-01'},
        {'م': 13, 'الاسم': 'محمد فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-01', 'تاريخ انتهاء العقد': '2027-05-01'},
        {'م': 14, 'الاسم': 'إبراهيم السيد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-15', 'تاريخ انتهاء العقد': '2027-02-01'},
        {'م': 15, 'الاسم': 'مصطفي عماد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-03-15'},
        {'م': 16, 'الاسم': 'محمد شريف دتة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-12-10', 'تاريخ انتهاء العقد': '2027-02-28'},
        {'م': 17, 'الاسم': 'محمد رضا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-02-15', 'تاريخ انتهاء العقد': '2027-04-30'},
        {'م': 18, 'الاسم': 'أبو نوح', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-05', 'تاريخ انتهاء العقد': '2026-12-15'},
        {'م': 19, 'الاسم': 'أبو صبري', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-04-01', 'تاريخ انتهاء العقد': '2027-06-15'},
        {'م': 20, 'الاسم': 'سليمان محي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-30', 'تاريخ انتهاء العقد': '2027-02-10'},
        {'م': 21, 'الاسم': 'حمزة داهما', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-01-05', 'تاريخ انتهاء العقد': '2027-03-20'},
        {'م': 22, 'الاسم': 'ريحاني', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-09-25', 'تاريخ انتهاء العقد': '2026-12-05'},
        {'م': 23, 'الاسم': 'دلال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-15', 'تاريخ انتهاء العقد': '2027-05-10'},
        {'م': 24, 'الاسم': 'فاربيس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-12-20', 'تاريخ انتهاء العقد': '2027-02-15'},
        {'م': 25, 'الاسم': 'قدوس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-02-28', 'تاريخ انتهاء العقد': '2027-04-18'},
        {'م': 26, 'الاسم': 'مد أبو بكر الصديق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-05-01', 'تاريخ انتهاء العقد': '2027-07-10'},
        {'م': 27, 'الاسم': 'أنيس الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-10', 'تاريخ انتهاء العقد': '2026-12-25'},
        {'م': 28, 'الاسم': 'حبيب مد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-01-15', 'تاريخ انتهاء العقد': '2027-03-30'},
        {'م': 29, 'الاسم': 'مطيع الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-05', 'تاريخ انتهاء العقد': '2027-01-20'},
        {'م': 30, 'الاسم': 'حبيب آل ملايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-25', 'تاريخ انتهاء العقد': '2027-05-30'},
        {'م': 31, 'الاسم': 'بطشا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-12-05', 'تاريخ انتهاء العقد': '2027-02-12'},
        {'م': 32, 'الاسم': 'السيد محمود', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-04-10', 'تاريخ انتهاء العقد': '2027-06-20'},
        {'م': 33, 'الاسم': 'علي إسماعيل', 'الوظيفة': 'معمل', 'الراتب الأساسي': 4500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-25', 'تاريخ انتهاء العقد': '2027-01-15'},
        {'م': 34, 'الاسم': 'محمد حمدان عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 4500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-02-10', 'تاريخ انتهاء العقد': '2027-04-05'},
        {'م': 35, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-01', 'تاريخ انتهاء العقد': '2027-02-14'},

        # مستودع ميم الخماسية الخرج (12 موظف)
        {'م': 41, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-09-05', 'تاريخ انتهاء العقد': '2026-10-10'},
        {'م': 42, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-06-01', 'تاريخ انتهاء العقد': '2027-08-01'},
        {'م': 43, 'الاسم': 'محمود عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-01-10', 'تاريخ انتهاء العقد': '2027-03-15'},
        {'م': 44, 'الاسم': 'شمشاد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-20', 'تاريخ انتهاء العقد': '2026-12-30'},
        {'م': 45, 'الاسم': 'زنجير', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-05', 'تاريخ انتهاء العقد': '2027-05-12'},
        {'م': 46, 'الاسم': 'بابلو', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-12', 'تاريخ انتهاء العقد': '2027-01-25'},
        {'م': 47, 'الاسم': 'إسماعيل الحداد', 'الوظيفة': 'حداد', 'الراتب الأساسي': 6000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-02-20', 'تاريخ انتهاء العقد': '2027-04-10'},
        {'م': 48, 'الاسم': 'نعيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-12-15', 'تاريخ انتهاء العقد': '2027-02-20'},
        {'م': 49, 'الاسم': 'مرسي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-04-05', 'تاريخ انتهاء العقد': '2027-06-12'},
        {'م': 50, 'الاسم': 'محمد علي كاشف', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-18', 'تاريخ انتهاء العقد': '2026-12-28'},
        {'م': 51, 'الاسم': 'احمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-01-25', 'تاريخ انتهاء العقد': '2027-03-30'},
        {'م': 52, 'الاسم': 'عبد الرحمن محمد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-30', 'تاريخ انتهاء العقد': '2027-05-25'},

        # مستودع ميم الخماسية الرياض (5 موظفين)
        {'م': 36, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2026-12-12', 'تاريخ انتهاء العقد': '2027-04-01'},
        {'م': 37, 'الاسم': 'محمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 0, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2027-02-05', 'تاريخ انتهاء العقد': '2027-04-10'},
        {'م': 38, 'الاسم': 'سمان السواق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2026-11-25', 'تاريخ انتهاء العقد': '2027-01-30'},
        {'م': 39, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-01-20'},
        {'م': 40, 'الاسم': 'إبراهيم جمال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2027-03-15', 'تاريخ انتهاء العقد': '2027-05-18'},

        # رواتب متنوعة
        {'م': 53, 'الاسم': 'موظف متنوع 1', 'الوظيفة': 'متنوع', 'الراتب الأساسي': 0, 'الفرع': 'رواتب متنوعة', 'تاريخ انتهاء الإقامة': '2027-01-01', 'تاريخ انتهاء العقد': '2027-01-01'}
    ]

    if 'payroll_df' not in st.session_state or st.session_state.get('current_month') != month_selected:
        st.session_state.current_month = month_selected
        df_init = pd.DataFrame(initial_data)
        df_init['الدفعة المدفوعة'] = df_init['الراتب الأساسي']
        df_init['المتبقي'] = 0.0
        df_init['نوع الإجراء'] = 'صرف كامل'
        df_init['الملاحظات'] = ''
        st.session_state.payroll_df = df_init

    # دالة توليد صفحة A4 لسندات القبض
    def generate_pretty_html_pdf(df_subset, branch_name):
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
            html += f"""
            <div class="voucher-box">
                <div class="header-logo-container">
                    <div class="header-en">Five-M Company For Industry<br>C. R. : 1011145035</div>
                    <div class="header-logo">5M</div>
                    <div class="header-ar">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
                </div>
                <div class="voucher-title">سند صرف راتب شهر ({month_selected}) | رقم السند: #{v1['م']:03d}</div>
                <table class="info-table">
                    <tr><th>اسم الموظف</th><td><strong>{v1['الاسم']}</strong></td><th>الفرع المحدد</th><td><strong>{v1['الفرع']}</strong></td></tr>
                    <tr><th>الراتب الأساسي المستحق</th><td>{v1['الراتب الأساسي']:,.0f} ر.س</td><th>الدفعة المصروفة</th><td><div class="amount-box">{v1['الدفعة المدفوعة']:,.0f} ر.س</div></td></tr>
                    <tr><th>البيان والملاحظات</th><td colspan="3">سداد دفعة من راتب شهر ({month_selected}) في المسير.</td></tr>
                </table>
                <div class="signatures"><div>توقيع واستلام الموظف: __________________</div><div>اعتماد المحاسب / الإدارة: __________________</div></div>
            </div>
            """
            if i + 1 < len(rows):
                v2 = rows[i + 1]
                html += '<div class="cut-line"><span>✂️ خط القص المخصص بين السندين ✂️</span></div>'
                html += f"""
                <div class="voucher-box">
                    <div class="header-logo-container">
                        <div class="header-en">Five-M Company For Industry<br>C. R. : 1011145035</div>
                        <div class="header-logo">5M</div>
                        <div class="header-ar">شركة ميم الخماسية للتصنيع<br>سجل تجاري : ١٠١١١٤٥٠٣٥</div>
                    </div>
                    <div class="voucher-title">سند صرف راتب شهر ({month_selected}) | رقم السند: #{v2['م']:03d}</div>
                    <table class="info-table">
                        <tr><th>اسم الموظف</th><td><strong>{v2['الاسم']}</strong></td><th>الفرع المحدد</th><td><strong>{v2['الفرع']}</strong></td></tr>
                        <tr><th>الراتب الأساسي المستحق</th><td>{v2['الراتب الأساسي']:,.0f} ر.س</td><th>الدفعة المصروفة</th><td><div class="amount-box">{v2['الدفعة المدفوعة']:,.0f} ر.س</div></td></tr>
                        <tr><th>البيان والملاحظات</th><td colspan="3">سداد دفعة من راتب شهر ({month_selected}) في المسير.</td></tr>
                    </table>
                    <div class="signatures"><div>توقيع واستلام الموظف: __________________</div><div>اعتماد المحاسب / الإدارة: __________________</div></div>
                </div>
                """
            html += '</div>'
        html += "</body></html>"
        output.write(html.encode('utf-8'))
        output.seek(0)
        return output

    # 4. الشاشات
    if '🔍' in menu:
        st.title('🔍 شاشة البحث الفوري وتعديل ملف موظف')
        st.write('اكتب اسم الموظف أو جزء منه للوصول السريع إلى ملفه الكامل وتعديل كافة بياناته المالية والوظيفية والوثائق:')
        
        all_emp_names = st.session_state.payroll_df['الاسم'].tolist()
        search_query = st.selectbox('🔍 اختر أو ابحث عن اسم الموظف:', all_emp_names)
        
        if search_query:
            emp_idx = st.session_state.payroll_df[st.session_state.payroll_df['الاسم'] == search_query].index[0]
            emp_data = st.session_state.payroll_df.loc[emp_idx]
            
            st.info(f"👤 **ملف الموظف الحالي:** {emp_data['الاسم']} (رقم مالي: #{emp_data['م']})")
            
            with st.form('edit_employee_form'):
                col_e1, col_e2, col_e3 = st.columns(3)
                
                with col_e1:
                    st.markdown("### 👤 البيانات الإدارية")
                    up_name = st.text_input("اسم الموظف الثلاثي:", value=emp_data['الاسم'])
                    up_job = st.text_input("الوظيفة:", value=emp_data['الوظيفة'])
                    up_branch = st.selectbox("الفرع التابع له:", [
                        'مصنع ميم الخماسية الخرج',
                        'مستودع ميم الخماسية الخرج',
                        'مستودع ميم الخماسية الرياض',
                        'رواتب متنوعة'
                    ], index=['مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'].index(emp_data['الفرع']))
                    
                with col_e2:
                    st.markdown("### 💰 البيانات المالية لشهر (" + month_selected + ")")
                    up_salary = st.number_input("الراتب الأساسي (ر.س):", min_value=0.0, value=float(emp_data['الراتب الأساسي']))
                    up_paid = st.number_input("الدفعة المصروفة (ر.س):", min_value=0.0, value=float(emp_data['الدفعة المدفوعة']))
                    up_action = st.selectbox("نوع الإجراء:", ["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"], index=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"].index(emp_data['نوع الإجراء']))
                    up_notes = st.text_input("الملاحظات:", value=emp_data['الملاحظات'])
                    
                with col_e3:
                    st.markdown("### 📄 الإقامات والعقود")
                    iq_val = datetime.strptime(str(emp_data['تاريخ انتهاء الإقامة']), '%Y-%m-%d') if pd.notnull(emp_data['تاريخ انتهاء الإقامة']) else datetime(2027, 12, 31)
                    ct_val = datetime.strptime(str(emp_data['تاريخ انتهاء العقد']), '%Y-%m-%d') if pd.notnull(emp_data['تاريخ انتهاء العقد']) else datetime(2027, 12, 31)
                    
                    up_iqama_date = st.date_input("تاريخ انتهاء الإقامة:", iq_val)
                    up_contract_date = st.date_input("تاريخ انتهاء العقد:", ct_val)
                    st.file_uploader("تحديث صورة الإقامة (PNG/PDF):", type=['png', 'jpg', 'pdf'], key="up_iq_file")
                    st.file_uploader("تحديث صورة عقد العمل (PNG/PDF):", type=['png', 'jpg', 'pdf'], key="up_ct_file")
                    
                st.divider()
                save_btn = st.form_submit_button('💾 حفظ والتحديث الشامل لبيانات الموظف في النظام')
                
                if save_btn:
                    st.session_state.payroll_df.loc[emp_idx, 'الاسم'] = up_name
                    st.session_state.payroll_df.loc[emp_idx, 'الوظيفة'] = up_job
                    st.session_state.payroll_df.loc[emp_idx, 'الفرع'] = up_branch
                    st.session_state.payroll_df.loc[emp_idx, 'الراتب الأساسي'] = up_salary
                    st.session_state.payroll_df.loc[emp_idx, 'الدفعة المدفوعة'] = up_paid
                    st.session_state.payroll_df.loc[emp_idx, 'المتبقي'] = up_salary - up_paid
                    st.session_state.payroll_df.loc[emp_idx, 'نوع الإجراء'] = up_action
                    st.session_state.payroll_df.loc[emp_idx, 'الملاحظات'] = up_notes
                    st.session_state.payroll_df.loc[emp_idx, 'تاريخ انتهاء الإقامة'] = str(up_iqama_date)
                    st.session_state.payroll_df.loc[emp_idx, 'تاريخ انتهاء العقد'] = str(up_contract_date)
                    
                    st.success(f"تم حفظ وتحديث ملف الموظف ({up_name}) بنجاح في السجلات والسندات والمسير!")

    elif '📊' in menu:
        st.title(f'📊 شاشة إدخال وتعديل الدفعات والأسماء - ({month_selected})')
        st.write('💡 **ملحوظة:** يمكنك التعديل التفاعلي المباشر لأسماء ووظائف الموظفين في الجدول أدناه وسيتحدث تلقائياً في كامل النظام.')
        
        t1, t2, t3, t4 = st.tabs(['📍 مصنع ميم الخماسية الخرج (35)', '📍 مستودع ميم الخماسية الخرج (12)', '📍 مستودع ميم الخماسية الرياض (5)', '📍 رواتب متنوعة'])
        branches = [('مصنع ميم الخماسية الخرج', t1), ('مستودع ميم الخماسية الخرج', t2), ('مستودع ميم الخماسية الرياض', t3), ('رواتب متنوعة', t4)]
        
        for b_name, tab_obj in branches:
            with tab_obj:
                df_b = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].copy()
                edited_b = st.data_editor(
                    df_b[['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'الدفعة المدفوعة', 'نوع الإجراء', 'الملاحظات']],
                    column_config={
                        "م": st.column_config.NumberColumn("م", disabled=True),
                        "الاسم": st.column_config.TextColumn("اسم الموظف (قابل للتعديل)"),
                        "الوظيفة": st.column_config.TextColumn("الوظيفة (قابل للتعديل)"),
                        "الراتب الأساسي": st.column_config.NumberColumn("الراتب المستحق", disabled=True, format="%d ر.س"),
                        "الدفعة المدفوعة": st.column_config.NumberColumn("الدفعة المصروفة (ر.س)", min_value=0, format="%d ر.س"),
                        "نوع الإجراء": st.column_config.SelectboxColumn("نوع الإجراء", options=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"]),
                        "الملاحظات": st.column_config.TextColumn("الملاحظات")
                    },
                    use_container_width=True,
                    hide_index=True,
                    key=f"ed_{b_name}_{month_selected}"
                )
                edited_b['المتبقي'] = edited_b['الراتب الأساسي'] - edited_b['الدفعة المدفوعة']
                
                for idx, row in edited_b.iterrows():
                    m_id = row['م']
                    st.session_state.payroll_df.loc[st.session_state.payroll_df['م'] == m_id, 'الاسم'] = row['الاسم']
                    st.session_state.payroll_df.loc[st.session_state.payroll_df['م'] == m_id, 'الوظيفة'] = row['الوظيفة']
                    st.session_state.payroll_df.loc[st.session_state.payroll_df['م'] == m_id, 'الدفعة المدفوعة'] = row['الدفعة المدفوعة']
                    st.session_state.payroll_df.loc[st.session_state.payroll_df['م'] == m_id, 'المتبقي'] = row['المتبقي']
                    st.session_state.payroll_df.loc[st.session_state.payroll_df['م'] == m_id, 'نوع الإجراء'] = row['نوع الإجراء']
                    st.session_state.payroll_df.loc[st.session_state.payroll_df['م'] == m_id, 'الملاحظات'] = row['الملاحظات']
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f'مستحق {b_name}', f"{edited_b['الراتب الأساسي'].sum():,.0f} ر.س")
                c2.metric(f'مصروف {b_name}', f"{edited_b['الدفعة المدفوعة'].sum():,.0f} ر.س")
                c3.metric(f'متبقي {b_name}', f"{edited_b['المتبقي'].sum():,.0f} ر.س")

    elif '💼' in menu:
        st.title('💼 سجل الموظفين وتدقيق الوثائق (مقسم بالكامل حسب الفرع)')
        st.write('تصفح الموظفين وارفِق إقاماتهم وعقودهم بسهولة:')
        
        tab_list = [
            ('🏢 مصنع ميم الخماسية الخرج', 'مصنع ميم الخماسية الخرج'),
            ('📦 مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج'),
            ('🏙️ مستودع ميم الخماسية الرياض', 'مستودع ميم الخماسية الرياض'),
            ('📋 رواتب متنوعة', 'رواتب متنوعة')
        ]
        
        tabs = st.tabs([t[0] for t in tab_list])
        
        for idx_t, (tab_title, b_name) in enumerate(tab_list):
            with tabs[idx_t]:
                df_branch_emp = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name]
                st.dataframe(df_branch_emp[['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'تاريخ انتهاء الإقامة', 'تاريخ انتهاء العقد']], use_container_width=True, hide_index=True)
                
                st.divider()
                st.subheader(f'📑 إدارة وثائق ومستندات موظف من ({b_name}):')
                emp_branch_names = df_branch_emp['الاسم'].tolist()
                
                if emp_branch_names:
                    emp_selected = st.selectbox(f'اختر موظفاً من فرع {b_name}:', emp_branch_names, key=f"sel_{b_name}")
                    emp_row = df_branch_emp[df_branch_emp['الاسم'] == emp_selected].iloc[0]
                    
                    col_u1, col_u2 = st.columns(2)
                    with col_u1:
                        st.write('🆔 **بيانات الإقامة:**')
                        iqama_date = st.date_input('تاريخ انتهاء الإقامة:', datetime.strptime(str(emp_row.get('تاريخ انتهاء الإقامة', '2026-12-31')), '%Y-%m-%d'), key=f"iq_{emp_selected}")
                        file_iq = st.file_uploader(f'رفع صورة إقامة ({emp_selected})', type=['png', 'jpg', 'pdf'], key=f"fiq_{emp_selected}")
                        if file_iq: st.success('تم رفع صورة الإقامة بنجاح!')
                        
                    with col_u2:
                        st.write('📄 **بيانات عقد العمل:**')
                        contract_date = st.date_input('تاريخ انتهاء عقد العمل:', datetime.strptime(str(emp_row.get('تاريخ انتهاء العقد', '2027-12-31')), '%Y-%m-%d'), key=f"ct_{emp_selected}")
                        file_ct = st.file_uploader(f'رفع عقد عمل ({emp_selected})', type=['png', 'jpg', 'pdf'], key=f"fct_{emp_selected}")
                        if file_ct: st.success('تم رفع عقد العمل بنجاح!')
                        
                    if st.button('💾 حفظ وتحديث بيانات الوثائق للموظف', key=f"btn_save_{emp_selected}"):
                        row_idx = st.session_state.payroll_df[st.session_state.payroll_df['الاسم'] == emp_selected].index[0]
                        st.session_state.payroll_df.loc[row_idx, 'تاريخ انتهاء الإقامة'] = str(iqama_date)
                        st.session_state.payroll_df.loc[row_idx, 'تاريخ انتهاء العقد'] = str(contract_date)
                        st.success(f'تم حفظ تحديثات الموظف ({emp_selected}) بنجاح!')

    elif '➕' in menu:
        st.title('➕ إضافة موظف جديد للنظام آلياً')
        st.write('ادخل بيانات الموظف الجديد وسيتم إدراجه فوراً في سجل الفروع وميزانية الرواتب وسندات القبض.')
        
        with st.form('add_new_emp_form'):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                new_name = st.text_input('اسم الموظف الثلاثي:')
                new_job = st.text_input('الوظيفة:', 'عامل')
                new_branch = st.selectbox('الفرع التابع له:', [
                    'مصنع ميم الخماسية الخرج',
                    'مستودع ميم الخماسية الخرج',
                    'مستودع ميم الخماسية الرياض',
                    'رواتب متنوعة'
                ])
            with c_f2:
                new_salary = st.number_input('الراتب الأساسي (ر.س):', min_value=0.0, value=2500.0)
                new_iqama_date = st.date_input('تاريخ انتهاء الإقامة:', datetime(2027, 12, 31))
                new_contract_date = st.date_input('تاريخ انتهاء عقد العمل:', datetime(2027, 12, 31))
                
            submit_emp = st.form_submit_button('💾 حفظ وإضافة الموظف فوراً للنظام')
            
            if submit_emp:
                if new_name:
                    max_id = st.session_state.payroll_df['م'].max() + 1 if not st.session_state.payroll_df.empty else 1
                    new_emp_dict = {
                        'م': max_id,
                        'الاسم': new_name,
                        'الوظيفة': new_job,
                        'الراتب الأساسي': new_salary,
                        'الفرع': new_branch,
                        'تاريخ انتهاء الإقامة': str(new_iqama_date),
                        'تاريخ انتهاء العقد': str(new_contract_date),
                        'الدفعة المدفوعة': new_salary,
                        'المتبقي': 0.0,
                        'نوع الإجراء': 'صرف كامل',
                        'الملاحظات': ''
                    }
                    st.session_state.payroll_df = pd.concat([st.session_state.payroll_df, pd.DataFrame([new_emp_dict])], ignore_index=True)
                    st.success(f'تمت إضافة الموظف ({new_name}) بنجاح برقم مالي #{max_id}!')
                else:
                    st.error('يرجى كتابة اسم الموظف قبل الحفظ.')

    elif '📈' in menu:
        st.title('📈 شاشة التقارير الشاملة وتنبيهات التجديد')
        tot_emp = len(st.session_state.payroll_df)
        tot_req = st.session_state.payroll_df['الراتب الأساسي'].sum()
        tot_paid = st.session_state.payroll_df['الدفعة المدفوعة'].sum()
        tot_rem = st.session_state.payroll_df['المتبقي'].sum()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric('إجمالي عدد العمالة', f'{tot_emp} موظف')
        m2.metric('إجمالي الرواتب الكلية', f'{tot_req:,.0f} ر.س')
        m3.metric('إجمالي المصروف فعلياً', f'{tot_paid:,.0f} ر.س')
        m4.metric('إجمالي المتبقي الكلي', f'{tot_rem:,.0f} ر.س')
        
        st.divider()
        st.subheader('🔔 مركز تنبيهات انتهاء الإقامات والعقود:')
        today = datetime.now().date()
        alerts = []
        for _, r in st.session_state.payroll_df.iterrows():
            try:
                iq_d = datetime.strptime(str(r.get('تاريخ انتهاء الإقامة')), '%Y-%m-%d').date()
                ct_d = datetime.strptime(str(r.get('تاريخ انتهاء العقد')), '%Y-%m-%d').date()
                if iq_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '🆔 إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🔴 منتهية (تحتاج تجديد)'})
                elif (iq_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '🆔 إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🟡 تنتهي خلال أقل من شهر'})
                if ct_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '📄 عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🔴 منتهي (تحتاج تجديد)'})
                elif (ct_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '📄 عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🟡 ينتهي خلال أقل من شهر'})
            except: pass
        if alerts: st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
        else: st.success('جميع الإقامات والعقود سارية ولا يوجد وثائق منتهية حالياً!')

    elif '📑' in menu:
        st.title(f'📑 كشوفات مسير الرواتب الرسمية - ({month_selected})')
        filter_sheet = st.selectbox('اختر الفرع للتقرير والطباعة:', ['جميع الفروع (الكشف الموحد)', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'])
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
                <button onclick="window.print()" style="background: #1E3A8A; color: white; border: none; padding: 10px 25px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer;">🖨️ اضغط هنا للطباعة المباشرة أو الحفظ كـ PDF</button>
            </div>
            <div class="header">
                <h2>🏢 شركة ميم الخماسية للتصنيع</h2>
                <h3>كشف مسير الرواتب والدفعات - {filter_sheet} ({month_selected})</h3>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>م</th>
                        <th>اسم الموظف</th>
                        <th>الوظيفة</th>
                        <th>الفرع</th>
                        <th>الراتب المستحق</th>
                        <th>الدفعة المصروفة</th>
                        <th>المتبقي</th>
                        <th>نوع الإجراء</th>
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
                    <td style="color:#047857; font-weight:bold;">{r['الدفعة المدفوعة']:,.0f} ر.س</td>
                    <td style="color:#b91c1c; font-weight:bold;">{r['المتبقي']:,.0f} ر.س</td>
                    <td>{r['نوع الإجراء']}</td>
                    <td style="width: 120px;"></td>
                </tr>
            """
        sheet_html += f"""
                </tbody>
            </table>
            <div class="totals-box">
                <span>إجمالي الرواتب المستحقة: {df_sheet['الراتب الأساسي'].sum():,.0f} ر.س</span>
                <span>إجمالي الدفعات المصروفة: {df_sheet['الدفعة المدفوعة'].sum():,.0f} ر.س</span>
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
        
        st.subheader("👁️ معاينة شكل كشف المسير الرسمي قبل الطباعة:")
        st.components.v1.html(sheet_html, height=450, scrolling=True)
        
        st.download_button(
            label=f"📄 فتح وتحميل ملف كشف مسير {filter_sheet} (HTML / PDF) 🖨️",
            data=sheet_html.encode('utf-8'),
            file_name=f"مسير_رواتب_{filter_sheet}_{month_selected}.html",
            mime="text/html"
        )

    elif '🖨️' in menu:
        st.title(f'🖨️ طباعة سندات القبض - ({month_selected})')
        selected_b = st.selectbox('اختر الفرع للتصدير والطباعة:', ['جميع الفروع', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'])
        df_print = st.session_state.payroll_df if selected_b == 'جميع الفروع' else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == selected_b]
        
        pdf_bytes = generate_pretty_html_pdf(df_print, selected_b)
        
        st.subheader("👁️ معاينة شكل سندات القبض (A4) قبل الطباعة:")
        st.components.v1.html(pdf_bytes.getvalue().decode('utf-8'), height=500, scrolling=True)
        
        st.download_button(
            label=f"📄 فتح وتنزيل ملف سندات صرف {selected_b} للطباعة 🖨️",
            data=pdf_bytes,
            file_name=f"سندات_صرف_راتب_{selected_b}_{month_selected}.html",
            mime="text/html"
        )
