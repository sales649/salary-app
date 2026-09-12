import streamlit as st
import pandas as pd
import io

# 1. إعداد الصفحة
st.set_page_config(page_title='شركة ميم الخماسية للتصنيع - إدارة الرواتب والدفعات', layout='wide', page_icon='🏢')

# 2. القائمة الجانبية والشهر
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🏢 شركة ميم الخماسية للتصنيع</h2>', unsafe_allow_html=True)
    logo = st.file_uploader('رفع لوجو الشركة الرسمي', type=['png', 'jpg', 'jpeg'])
    if logo:
        st.image(logo, use_container_width=True)
    st.divider()
    menu = st.radio('📌 التنقل الرئيسي:', [
        '📊 شاشة إدخال الدفعات (حسب الفرع)',
        '💼 سجل الموظفين والإجماليات',
        '📑 مسير الرواتب الشهري (للطباعة)',
        '🖨️ طباعة سندات القبض (PDF A4)',
        '➕ إضافة نظام جديد'
    ])
    st.divider()
    month_selected = st.selectbox('📅 اختر شهر العمليات:', ['أغسطس 2026', 'سبتمبر 2026', 'أكتوبر 2026', 'نوفمبر 2026'])

# 3. قاعدة البيانات الأساسية لـ 52 موظفاً بالفروع المحدثة
initial_data = [
    # مستودع الخرج (الموظفين السابقين في الخرج + الملقة)
    {'م': 1, 'الاسم': 'مد ماجد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع الخرج'},
    {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 3, 'الاسم': 'أيوب', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 4, 'الاسم': 'ذاكر حسين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 5, 'الاسم': 'رفيق الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 1600, 'الفرع': 'مستودع الخرج'},
    {'م': 6, 'الاسم': 'رحيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 7, 'الاسم': 'محي الدين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 8, 'الاسم': 'محمد ريان', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'مستودع الخرج'},
    {'م': 9, 'الاسم': 'مدلايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'مستودع الخرج'},
    {'م': 10, 'الاسم': 'عالم روبيل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500, 'الفرع': 'مستودع الخرج'},
    {'م': 11, 'الاسم': 'شوقي كامل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الخرج'},
    {'م': 12, 'الاسم': 'عمرو فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الخرج'},
    {'م': 13, 'الاسم': 'محمد فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الخرج'},
    {'م': 14, 'الاسم': 'إبراهيم السيد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 15, 'الاسم': 'مصطفي عماد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 16, 'الاسم': 'محمد شريف دتة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 17, 'الاسم': 'محمد رضا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 18, 'الاسم': 'أبو نوح', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع الخرج'},
    {'م': 19, 'الاسم': 'أبو صبري', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع الخرج'},
    {'م': 20, 'الاسم': 'سليمان محي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الخرج'},
    {'م': 21, 'الاسم': 'حمزة داهما', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 22, 'الاسم': 'ريحاني', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 23, 'الاسم': 'دلال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 24, 'الاسم': 'فاربيس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 25, 'الاسم': 'قدوس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 26, 'الاسم': 'مد أبو بكر الصديق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 27, 'الاسم': 'أنيس الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 28, 'الاسم': 'حبيب مد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 29, 'الاسم': 'مطيع الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 30, 'الاسم': 'حبيب آل ملايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'مستودع الخرج'},
    {'م': 31, 'الاسم': 'بطشا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'مستودع الخرج'},
    {'م': 32, 'الاسم': 'السيد محمود', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500, 'الفرع': 'مستودع الخرج'},
    {'م': 33, 'الاسم': 'علي إسماعيل', 'الوظيفة': 'معمل', 'الراتب الأساسي': 4500, 'الفرع': 'مستودع الخرج'},
    {'م': 34, 'الاسم': 'محمد حمدان عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 4500, 'الفرع': 'مستودع الخرج'},
    {'م': 35, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'مستودع الخرج'},
    {'م': 41, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الخرج'},
    {'م': 42, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع الخرج'},
    {'م': 43, 'الاسم': 'محمود عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'مستودع الخرج'},
    {'م': 44, 'الاسم': 'شمشاد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع الخرج'},
    {'م': 45, 'الاسم': 'زنجير', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع الخرج'},
    {'م': 46, 'الاسم': 'بابلو', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'مستودع الخرج'},
    {'م': 47, 'الاسم': 'إسماعيل الحداد', 'الوظيفة': 'حداد', 'الراتب الأساسي': 6000, 'الفرع': 'مستودع الخرج'},
    {'م': 48, 'الاسم': 'نعيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 49, 'الاسم': 'مرسي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 50, 'الاسم': 'محمد علي كاشف', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},
    {'م': 51, 'الاسم': 'احمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500, 'الفرع': 'مستودع الخرج'},
    {'م': 52, 'الاسم': 'عبد الرحمن محمد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'مستودع الخرج'},

    # مستودع الرياض (5 موظفين)
    {'م': 36, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الرياض'},
    {'م': 37, 'الاسم': 'محمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 0, 'الفرع': 'مستودع الرياض'},
    {'م': 38, 'الاسم': 'سمان السواق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500, 'الفرع': 'مستودع الرياض'},
    {'م': 39, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب الأساسي': 4000, 'الفرع': 'مستودع الرياض'},
    {'م': 40, 'الاسم': 'إبراهيم جمال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'مستودع الرياض'},

    # رواتب متنوعة
    {'م': 53, 'الاسم': 'موظف متنوع 1 (قيد الإضافة)', 'الوظيفة': 'متنوع', 'الراتب الأساسي': 0, 'الفرع': 'رواتب متنوعة'}
]

# التحكم في بيانات الشهر والتجديد
if 'current_month' not in st.session_state or st.session_state.current_month != month_selected:
    st.session_state.current_month = month_selected
    df_init = pd.DataFrame(initial_data)
    df_init['الدفعة المدفوعة'] = df_init['الراتب الأساسي']
    df_init['المتبقي'] = 0.0
    df_init['نوع الإجراء'] = 'صرف كامل'
    df_init['الملاحظات'] = ''
    st.session_state.payroll_df = df_init

# دالة توليد صفحة A4 لسندات صرف الرواتب
def generate_pretty_html_pdf(df_subset, branch_name):
    output = io.BytesIO()
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
    <meta charset="utf-8">
    <title>سندات صرف الرواتب - شركة ميم الخماسية للتصنيع</title>
    <style>
        @page {{ size: A4 portrait; margin: 8mm; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #ffffff; color: #111; margin: 0; padding: 0; }}
        .page {{ height: 275mm; page-break-after: always; display: flex; flex-direction: column; justify-content: space-between; }}
        .voucher-box {{ border: 2px solid #1E3A8A; border-radius: 8px; padding: 12px 18px; background: #fff; height: 128mm; box-sizing: border-box; position: relative; }}
        .header-logo-container {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1E3A8A; padding-bottom: 6px; margin-bottom: 8px; }}
        .header-en {{ text-align: left; font-size: 11px; color: #1E3A8A; font-weight: bold; width: 38%; }}
        .header-logo {{ text-align: center; width: 24%; }}
        .header-logo span {{ font-size: 40px; font-weight: 900; color: #DC2626; letter-spacing: -2px; font-family: Arial, sans-serif; }}
        .header-ar {{ text-align: right; font-size: 12px; color: #1E3A8A; font-weight: bold; width: 38%; }}
        .voucher-title {{ text-align: center; font-size: 16px; font-weight: bold; color: #1E3A8A; margin: 6px 0; background: #f1f5f9; padding: 6px; border-radius: 4px; }}
        .info-table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
        .info-table td {{ padding: 8px 12px; font-size: 14px; border: 1px solid #e0e0e0; }}
        .info-table th {{ background-color: #f8fafc; color: #1E3A8A; padding: 8px 12px; font-size: 14px; border: 1px solid #cbd5e1; text-align: right; width: 25%; }}
        .amount-box {{ background-color: #ecfdf5; border: 2px solid #10b981; color: #047857; font-size: 18px; font-weight: bold; text-align: center; padding: 6px 12px; border-radius: 6px; display: inline-block; }}
        .signatures {{ margin-top: 22px; display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; padding: 0 20px; }}
        .cut-line {{ border-top: 2px dashed #94a3b8; text-align: center; margin: 4mm 0; position: relative; }}
        .cut-line span {{ background: #fff; padding: 0 10px; position: relative; top: -12px; color: #64748b; font-size: 11px; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
    </head>
    <body>
        <div class="no-print" style="text-align:center; padding: 12px; background: #f8fafc; border-bottom: 1px solid #ddd;">
            <button onclick="window.print()" style="background: #1E3A8A; color: white; border: none; padding: 10px 25px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer;">🖨️ اضغط هنا لطباعة السندات الرسمية أو الحفظ كـ PDF</button>
        </div>
    """
    
    rows = [row for _, row in df_subset.iterrows()]
    for i in range(0, len(rows), 2):
        html += '<div class="page">'
        v1 = rows[i]
        html += f"""
        <div class="voucher-box">
            <div class="header-logo-container">
                <div class="header-en">Five-M Company For Industry<br>A limited liability company<br>C. R. : 1011145035<br>Investment R. : 99376</div>
                <div class="header-logo"><span>5M</span></div>
                <div class="header-ar">شركة ميم الخماسية للتصنيع<br>شركة ذات مسئولية محدودة<br>سجل تجاري : ١٠١١١٤٥٠٣٥<br>سجل استثماري : ٩٩٣٧٦</div>
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
                    <div class="header-en">Five-M Company For Industry<br>A limited liability company<br>C. R. : 1011145035<br>Investment R. : 99376</div>
                    <div class="header-logo"><span>5M</span></div>
                    <div class="header-ar">شركة ميم الخماسية للتصنيع<br>شركة ذات مسئولية محدودة<br>سجل تجاري : ١٠١١١٤٥٠٣٥<br>سجل استثماري : ٩٩٣٧٦</div>
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
    st.title(f'📊 شاشة إدخال الدفعات - لشهر ({month_selected})')
    st.write('قم بتعديل مبالغ الدفعات للفروع المحدثة، وسيتحدث السجل ومسير الرواتب والسندات تلقائياً.')
    
    t1, t2, t3 = st.tabs(['📍 مستودع الخرج (47 موظف)', '📍 مستودع الرياض (5 موظفين)', '📍 رواتب متنوعة'])
    branches = [('مستودع الخرج', t1), ('مستودع الرياض', t2), ('رواتب متنوعة', t3)]
    
    for b_name, tab_obj in branches:
        with tab_obj:
            df_b = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name].copy()
            
            edited_b = st.data_editor(
                df_b,
                column_config={
                    "م": st.column_config.NumberColumn("م", disabled=True),
                    "الاسم": st.column_config.TextColumn("اسم الموظف", disabled=True),
                    "الوظيفة": st.column_config.TextColumn("الوظيفة", disabled=True),
                    "الفرع": st.column_config.TextColumn("الفرع", disabled=True),
                    "الراتب الأساسي": st.column_config.NumberColumn("الراتب المستحق", disabled=True, format="%d ر.س"),
                    "الدفعة المدفوعة": st.column_config.NumberColumn("الدفعة المصروفة (ر.س)", min_value=0, format="%d ر.س"),
                    "نوع الإجراء": st.column_config.SelectboxColumn("نوع الإجراء", options=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"]),
                    "الملاحظات": st.column_config.TextColumn("الملاحظات")
                },
                use_container_width=True,
                key=f"editor_{b_name}_{month_selected}"
            )
            
            edited_b['المتبقي'] = edited_b['الراتب الأساسي'] - edited_b['الدفعة المدفوعة']
            st.session_state.payroll_df.update(edited_b)
            
            req = edited_b['الراتب الأساسي'].sum()
            paid = edited_b['الدفعة المدفوعة'].sum()
            rem = edited_b['المتبقي'].sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric(f'مستحق {b_name}', f'{req:,.0f} ر.س')
            c2.metric(f'مصروف {b_name}', f'{paid:,.0f} ر.س')
            c3.metric(f'متبقي {b_name}', f'{rem:,.0f} ر.س')

elif '💼' in menu:
    st.title(f'💼 سجل الموظفين والإجماليات - ({month_selected})')
    s1, s2, s3 = st.tabs(['مستودع الخرج', 'مستودع الرياض', 'رواتب متنوعة'])
    
    for b_name, tab_obj in [('مستودع الخرج', s1), ('مستودع الرياض', s2), ('رواتب متنوعة', s3)]:
        with tab_obj:
            df_b = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name]
            st.dataframe(df_b[['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'الدفعة المدفوعة', 'المتبقي', 'نوع الإجراء', 'الملاحظات']], use_container_width=True)
            
            req = df_b['الراتب الأساسي'].sum()
            paid = df_b['الدفعة المدفوعة'].sum()
            rem = df_b['المتبقي'].sum()
            st.info(f"📊 **إجمالي {b_name}:** المستحق: **{req:,.0f} ر.س** | المصروف: **{paid:,.0f} ر.س** | المتبقي: **{rem:,.0f} ر.س**")

    st.divider()
    st.subheader('🌐 الإجمالي العام للشركة')
    tot_req = st.session_state.payroll_df['الراتب الأساسي'].sum()
    tot_paid = st.session_state.payroll_df['الدفعة المدفوعة'].sum()
    tot_rem = st.session_state.payroll_df['المتبقي'].sum()
    
    g1, g2, g3 = st.columns(3)
    g1.metric('إجمالي رواتب الشركة', f'{tot_req:,.0f} ر.س')
    g2.metric('إجمالي الدفعات المسلمة', f'{tot_paid:,.0f} ر.س')
    g3.metric('إجمالي المتبقي الكلي', f'{tot_rem:,.0f} ر.س')

elif '📑' in menu:
    st.title(f'📑 مسير الرواتب الرسمي للشهر ({month_selected})')
    st.write('كشف مسير الرواتب الموحد لجميع الموظفين بالفروع جاهز للطباعة والتحميل.')
    
    filter_sheet = st.selectbox('اختر الفرع لمسير الرواتب:', ['جميع الفروع', 'مستودع الخرج', 'مستودع الرياض', 'رواتب متنوعة'])
    
    if filter_sheet == 'جميع الفروع':
        df_sheet = st.session_state.payroll_df
    else:
        df_sheet = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == filter_sheet]
        
    st.dataframe(df_sheet[['م', 'الاسم', 'الوظيفة', 'الفرع', 'الراتب الأساسي', 'الدفعة المدفوعة', 'المتبقي', 'نوع الإجراء', 'الملاحظات']], use_container_width=True)
    
    # زر طباعة المسير
    sheet_html = f"""
    <html dir="rtl"><head><meta charset="utf-8"><style>
    body {{ font-family: Arial; padding: 20px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
    th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }}
    th {{ background-color: #1E3A8A; color: white; }}
    .header {{ text-align: center; color: #1E3A8A; }}
    </style></head><body>
    <div class="header">
        <h2>🏢 شركة ميم الخماسية للتصنيع</h2>
        <h3>كشف مسير رواتب شهر ({month_selected}) - {filter_sheet}</h3>
    </div>
    <table>
        <tr><th>م</th><th>اسم الموظف</th><th>الوظيفة</th><th>الفرع</th><th>الراتب المستحق</th><th>الدفعة المصروفة</th><th>المتبقي</th><th>التوقيع / الاستلام</th></tr>
    """
    for idx, r in df_sheet.iterrows():
        sheet_html += f"<tr><td>{r['م']}</td><td>{r['الاسم']}</td><td>{r['الوظيفة']}</td><td>{r['الفرع']}</td><td>{r['الراتب الأساسي']}</td><td>{r['الدفعة المدفوعة']}</td><td>{r['المتبقي']}</td><td></td></tr>"
    sheet_html += f"</table><br><br><b>إجمالي المستحق: {df_sheet['الراتب الأساسي'].sum():,.0f} ر.س | إجمالي المصروف: {df_sheet['الدفعة المدفوعة'].sum():,.0f} ر.س | إجمالي المتبقي: {df_sheet['المتبقي'].sum():,.0f} ر.س</b></body></html>"
    
    st.download_button(
        label=f"🖨️ تنزيل وطباعة مسير رواتب {filter_sheet} (HTML / PDF)",
        data=sheet_html.encode('utf-8'),
        file_name=f"مسير_رواتب_{filter_sheet}_{month_selected}.html",
        mime="text/html"
    )

elif '🖨️' in menu:
    st.title(f'🖨️ طباعة سندات القبض الرسمية - ({month_selected})')
    selected_b = st.selectbox('اختر الفرع للتصدير والطباعة:', ['جميع الفروع', 'مستودع الخرج', 'مستودع الرياض', 'رواتب متنوعة'])
    
    if selected_b == 'جميع الفروع':
        df_print = st.session_state.payroll_df
    else:
        df_print = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == selected_b]
        
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
