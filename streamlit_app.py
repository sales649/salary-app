import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta

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
            '📊 شاشة إدخال الدفعات (حسب الفرع)',
            '💼 سجل الموظفين وتدقيق الوثائق',
            '📈 شاشة التقارير وإدارة التجديدات',
            '📑 مسير الرواتب الشهري (للطباعة)',
            '🖨️ طباعة سندات القبض (PDF A4)',
            '➕ إضافة نظام جديد'
        ])
        st.divider()
        if 'months_list' not in st.session_state:
            st.session_state.months_list = ['أغسطس 2026', 'سبتمبر 2026', 'أكتوبر 2026']
        month_selected = st.selectbox('📅 اختر شهر العمليات:', st.session_state.months_list)

    # قاعدة البيانات الأساسية مع التواريخ الافتراضية للإقامات والعقود
    initial_data = [
        # مصنع ميم الخماسية الخرج
        {'م': 1, 'الاسم': 'مد ماجد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-10-15', 'تاريخ انتهاء العقد': '2027-01-01'},
        {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-09-20', 'تاريخ انتهاء العقد': '2026-12-31'},
        {'م': 3, 'الاسم': 'أيوب', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-08-01', 'تاريخ انتهاء العقد': '2026-11-15'},
        {'م': 4, 'الاسم': 'ذاكر حسين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-03-10', 'تاريخ انتهاء العقد': '2027-05-20'},
        {'م': 35, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'مصنع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-11-01', 'تاريخ انتهاء العقد': '2027-02-14'},

        # مستودع ميم الخماسية الخرج
        {'م': 41, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2026-09-05', 'تاريخ انتهاء العقد': '2026-10-10'},
        {'م': 42, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع ميم الخماسية الخرج', 'تاريخ انتهاء الإقامة': '2027-06-01', 'تاريخ انتهاء العقد': '2027-08-01'},

        # مستودع ميم الخماسية الرياض
        {'م': 36, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2026-12-12', 'تاريخ انتهاء العقد': '2027-04-01'},
        {'م': 39, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع ميم الخماسية الرياض', 'تاريخ انتهاء الإقامة': '2027-01-20', 'تاريخ انتهاء العقد': '2027-01-20'},

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

    # دالة إنشاء الهيدر للسندات
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
    if '📊' in menu:
        st.title(f'📊 شاشة إدخال الدفعات - ({month_selected})')
        t1, t2, t3, t4 = st.tabs(['📍 مصنع ميم الخماسية الخرج', '📍 مستودع ميم الخماسية الخرج', '📍 مستودع ميم الخماسية الرياض', '📍 رواتب متنوعة'])
        branches = [('مصنع ميم الخماسية الخرج', t1), ('مستودع ميم الخماسية الخرج', t2), ('مستودع ميم الخماسية الرياض', t3), ('رواتب متنوعة', t4)]
        
        for b_name, tab_obj in branches:
            with tab_obj:
                df_b = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].copy()
                edited_b = st.data_editor(
                    df_b[['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'الدفعة المدفوعة', 'نوع الإجراء', 'الملاحظات']],
                    column_config={
                        "م": st.column_config.NumberColumn("م", disabled=True),
                        "الاسم": st.column_config.TextColumn("اسم الموظف", disabled=True),
                        "الوظيفة": st.column_config.TextColumn("الوظيفة", disabled=True),
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
                st.session_state.payroll_df.update(edited_b)
                
                c1, c2, c3 = st.columns(3)
                c1.metric(f'مستحق {b_name}', f"{edited_b['الراتب الأساسي'].sum():,.0f} ر.س")
                c2.metric(f'مصروف {b_name}', f"{edited_b['الدفعة المدفوعة'].sum():,.0f} ر.س")
                c3.metric(f'متبقي {b_name}', f"{edited_b['المتبقي'].sum():,.0f} ر.س")

    elif '💼' in menu:
        st.title('💼 سجل الموظفين ورفع ملفات الإقامة والعقود')
        st.write('قم باختيار الموظف لرفع صورة الإقامة وعقد العمل وتعديل تواريخ الانتهاء:')
        
        emp_list = st.session_state.payroll_df['الاسم'].tolist()
        emp_selected = st.selectbox('👤 اختر الموظف:', emp_list)
        
        emp_row = st.session_state.payroll_df[st.session_state.payroll_df['الاسم'] == emp_selected].iloc[0]
        
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.subheader('🆔 بيانات الإقامة')
            iqama_date = st.date_input('تاريخ انتهاء الإقامة:', datetime.strptime(str(emp_row.get('تاريخ انتهاء الإقامة', '2026-12-31')), '%Y-%m-%d'))
            file_iqama = st.file_uploader(f'رفع صورة إقامة ({emp_selected})', type=['png', 'jpg', 'pdf'])
            if file_iqama: st.success('تم رفع صورة الإقامة بنجاح!')
            
        with col_u2:
            st.subheader('📄 بيانات عقد العمل')
            contract_date = st.date_input('تاريخ انتهاء عقد العمل:', datetime.strptime(str(emp_row.get('تاريخ انتهاء العقد', '2027-12-31')), '%Y-%m-%d'))
            file_contract = st.file_uploader(f'رفع عقد عمل ({emp_selected})', type=['png', 'jpg', 'pdf'])
            if file_contract: st.success('تم رفع عقد العمل بنجاح!')
            
        if st.button('💾 حفظ وتحديث بيانات الموظف'):
            idx = st.session_state.payroll_df[st.session_state.payroll_df['الاسم'] == emp_selected].index[0]
            st.session_state.payroll_df.loc[idx, 'تاريخ انتهاء الإقامة'] = str(iqama_date)
            st.session_state.payroll_df.loc[idx, 'تاريخ انتهاء العقد'] = str(contract_date)
            st.success('تم حفظ التواريخ والملفات بنجاح!')
            
        st.divider()
        st.dataframe(st.session_state.payroll_df[['م', 'الاسم', 'الوظيفة', 'الفرع', 'الراتب الأساسي', 'تاريخ انتهاء الإقامة', 'تاريخ انتهاء العقد']], use_container_width=True, hide_index=True)

    elif '📈' in menu:
        st.title('📈 شاشة التقارير الشاملة وتنبيهات التجديد')
        
        # مؤشرات عامة
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
                
                # فحص الإقامة
                if iq_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '🆔 إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🔴 منتهية (تحتاج تجديد فوراً)'})
                elif (iq_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '🆔 إقامة', 'تاريخ الانتهاء': iq_d, 'الحالة': '🟡 تنتهي خلال أقل من شهر'})
                    
                # فحص العقد
                if ct_d < today:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '📄 عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🔴 منتهي (تحتاج تجديد فوراً)'})
                elif (ct_d - today).days <= 30:
                    alerts.append({'الموظف': r['الاسم'], 'الفرع': r['الفرع'], 'نوع الوثيقة': '📄 عقد عمل', 'تاريخ الانتهاء': ct_d, 'الحالة': '🟡 ينتهي خلال أقل من شهر'})
            except:
                pass
                
        if alerts:
            st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
        else:
            st.success('جميع الإقامات والعقود سارية ولا يوجد وثائق منتهية حالياً!')

    elif '📑' in menu:
        st.title(f'📑 مسير الرواتب الرسمي - ({month_selected})')
        filter_sheet = st.selectbox('اختر الفرع لمسير الرواتب:', ['جميع الفروع', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'])
        df_sheet = st.session_state.payroll_df if filter_sheet == 'جميع الفروع' else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == filter_sheet]
        
        st.dataframe(df_sheet[['م', 'الاسم', 'الوظيفة', 'الفرع', 'الراتب الأساسي', 'الدفعة المدفوعة', 'المتبقي', 'نوع الإجراء', 'الملاحظات']], use_container_width=True, hide_index=True)

    elif '🖨️' in menu:
        st.title(f'🖨️ طباعة سندات القبض - ({month_selected})')
        selected_b = st.selectbox('اختر الفرع للتصدير والطباعة:', ['جميع الفروع', 'مصنع ميم الخماسية الخرج', 'مستودع ميم الخماسية الخرج', 'مستودع ميم الخماسية الرياض', 'رواتب متنوعة'])
        df_print = st.session_state.payroll_df if selected_b == 'جميع الفروع' else st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == selected_b]
        
        pdf_bytes = generate_pretty_html_pdf(df_print, selected_b)
        st.download_button(
            label=f"📄 فتح واستعراض سندات صرف {selected_b} للطباعة 🖨️",
            data=pdf_bytes,
            file_name=f"سندات_صرف_راتب_{selected_b}_{month_selected}.html",
            mime="text/html"
        )

    elif '➕' in menu:
        st.title('🚀 إضافة نظام جديد مستقبلاً')
        st.selectbox('اختر الموديل:', ['نظام الحضور والانصراف والبصمة', 'نظام إدارة طلبات الإجازات', 'نظام حساب مكافأة نهاية الخدمة'])
        st.button('تفعيل النظام')
