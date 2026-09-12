import streamlit as st
import pandas as pd
import io

# 1. إعداد الصفحة
st.set_page_config(page_title='شركة ميم الخماسية للتصنيع - إدارة الرواتب والدفعات', layout='wide', page_icon='🏢')

# 2. القائمة الجانبية
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🏢 شركة ميم الخماسية للتصنيع</h2>', unsafe_allow_html=True)
    logo = st.file_uploader('رفع لوجو الشركة الرسمي', type=['png', 'jpg', 'jpeg'])
    if logo:
        st.image(logo, use_container_width=True)
    st.divider()
    menu = st.radio('📌 التنقل الرئيسي:', [
        '📊 شاشة إدخال الدفعات (حسب الفرع)',
        '💼 سجل الموظفين والإجماليات',
        '🖨️ طباعة سندات القبض (PDF A4)',
        '➕ إضافة نظام جديد'
    ])
    st.divider()
    month_selected = st.selectbox('📅 اختر الشهر للأرشيف:', ['أغسطس 2026', 'يوليو 2026', 'يونيو 2026'])

# 3. قاعدة البيانات الأساسية لـ 52 موظفاً
initial_data = [
    # فرع الخرج (35 موظف)
    {'م': 1, 'الاسم': 'مد ماجد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'الخرج'},
    {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الخرج'},
    {'م': 3, 'الاسم': 'أيوب', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 4, 'الاسم': 'ذاكر حسين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 5, 'الاسم': 'رفيق الإسلام', 'الوظيفة': 'عامل', 'الراتب الأساسي': 1600, 'الفرع': 'الخرج'},
    {'م': 6, 'الاسم': 'رحيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الخرج'},
    {'م': 7, 'الاسم': 'محي الدين', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الخرج'},
    {'م': 8, 'الاسم': 'محمد ريان', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'الخرج'},
    {'م': 9, 'الاسم': 'مدلايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'الخرج'},
    {'م': 10, 'الاسم': 'عالم روبيل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500, 'الفرع': 'الخرج'},
    {'م': 11, 'الاسم': 'شوقي كامل', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'الخرج'},
    {'م': 12, 'الاسم': 'عمرو فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'الخرج'},
    {'م': 13, 'الاسم': 'محمد فوزي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'الخرج'},
    {'م': 14, 'الاسم': 'إبراهيم السيد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الخرج'},
    {'م': 15, 'الاسم': 'مصطفي عماد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الخرج'},
    {'م': 16, 'الاسم': 'محمد شريف دتة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 17, 'الاسم': 'محمد رضا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الخرج'},
    {'م': 18, 'الاسم': 'أبو نوح', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'الخرج'},
    {'م': 19, 'الاسم': 'أبو صبري', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'الخرج'},
    {'م': 20, 'الاسم': 'سليمان محي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'الخرج'},
    {'م': 21, 'الاسم': 'حمزة داهما', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 22, 'الاسم': 'ريحاني', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 23, 'الاسم': 'دلال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 24, 'الاسم': 'فاربيس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 25, 'الاسم': 'قدوس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 26, 'الاسم': 'مد أبو بكر الصديق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 27, 'الاسم': 'أنيس الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 28, 'الاسم': 'حبيب مد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 29, 'الاسم': 'مطيع الرحمن', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 30, 'الاسم': 'حبيب آل ملايس', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2000, 'الفرع': 'الخرج'},
    {'م': 31, 'الاسم': 'بطشا', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2200, 'الفرع': 'الخرج'},
    {'م': 32, 'الاسم': 'السيد محمود', 'الوظيفة': 'عامل', 'الراتب الأساسي': 500, 'الفرع': 'الخرج'},
    {'م': 33, 'الاسم': 'علي إسماعيل', 'الوظيفة': 'معمل', 'الراتب الأساسي': 4500, 'الفرع': 'الخرج'},
    {'م': 34, 'الاسم': 'محمد حمدان عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 4500, 'الفرع': 'الخرج'},
    {'م': 35, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'الخرج'},

    # فرع المستودع (5 موظفين)
    {'م': 36, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'المستودع'},
    {'م': 37, 'الاسم': 'محمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 0, 'الفرع': 'المستودع'},
    {'م': 38, 'الاسم': 'سمان السواق', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500, 'الفرع': 'المستودع'},
    {'م': 39, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب الأساسي': 4000, 'الفرع': 'المستودع'},
    {'م': 40, 'الاسم': 'إبراهيم جمال', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'المستودع'},

    # فرع الملقة (12 موظف)
    {'م': 41, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3000, 'الفرع': 'الملقة'},
    {'م': 42, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'الملقة'},
    {'م': 43, 'الاسم': 'محمود عثمان', 'الوظيفة': 'مشرف', 'الراتب الأساسي': 7000, 'الفرع': 'الملقة'},
    {'م': 44, 'الاسم': 'شمشاد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 4000, 'الفرع': 'الملقة'},
    {'م': 45, 'الاسم': 'زنجير', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'الملقة'},
    {'م': 46, 'الاسم': 'بابلو', 'الوظيفة': 'عامل', 'الراتب الأساسي': 5000, 'الفرع': 'الملقة'},
    {'م': 47, 'الاسم': 'إسماعيل الحداد', 'الوظيفة': 'حداد', 'الراتب الأساسي': 6000, 'الفرع': 'الملقة'},
    {'م': 48, 'الاسم': 'نعيم', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الملقة'},
    {'م': 49, 'الاسم': 'مرسي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الملقة'},
    {'م': 50, 'الاسم': 'محمد علي كاشف', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الملقة'},
    {'م': 51, 'الاسم': 'احمد علي', 'الوظيفة': 'عامل', 'الراتب الأساسي': 3500, 'الفرع': 'الملقة'},
    {'م': 52, 'الاسم': 'عبد الرحمن محمد', 'الوظيفة': 'عامل', 'الراتب الأساسي': 2500, 'الفرع': 'الملقة'}
]

if 'payroll_df' not in st.session_state:
    df_init = pd.DataFrame(initial_data)
    df_init['الدفعة المدفوعة'] = df_init['الراتب الأساسي']
    df_init['المتبقي'] = 0.0
    df_init['نوع الإجراء'] = 'صرف كامل'
    df_init['الملاحظات'] = ''
    st.session_state.payroll_df = df_init

# دالة توليد صفحة A4 الأنيقة بحجم دقيق وسندين بكل صفحة مع خط التنقيط والهيدر المعتمد
def generate_pretty_html_pdf(df_subset, branch_name):
    output = io.BytesIO()
    
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
    <meta charset="utf-8">
    <title>سندات قبض الرواتب - شركة ميم الخماسية للتصنيع</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffffff;
            color: #111;
            margin: 0;
            padding: 0;
        }}
        .page {{
            height: 270mm;
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .voucher-box {{
            border: 2px solid #1E3A8A;
            border-radius: 8px;
            padding: 12px 18px;
            background: #fff;
            height: 125mm;
            box-sizing: border-box;
            position: relative;
        }}
        .header-logo-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #1E3A8A;
            padding-bottom: 6px;
            margin-bottom: 10px;
        }}
        .header-en {{
            text-align: left;
            font-size: 11px;
            color: #1E3A8A;
            font-weight: bold;
            width: 38%;
        }}
        .header-logo {{
            text-align: center;
            width: 24%;
        }}
        .header-logo span {{
            font-size: 42px;
            font-weight: 900;
            color: #DC2626;
            letter-spacing: -2px;
            font-family: Arial, sans-serif;
        }}
        .header-ar {{
            text-align: right;
            font-size: 12px;
            color: #1E3A8A;
            font-weight: bold;
            width: 38%;
        }}
        .voucher-title {{
            text-align: center;
            font-size: 15px;
            font-weight: bold;
            color: #1E3A8A;
            margin: 4px 0 8px 0;
            background: #f1f5f9;
            padding: 4px;
            border-radius: 4px;
        }}
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 6px;
        }}
        .info-table td {{
            padding: 6px 10px;
            font-size: 13px;
            border: 1px solid #e0e0e0;
        }}
        .info-table th {{
            background-color: #f8fafc;
            color: #1E3A8A;
            padding: 6px 10px;
            font-size: 13px;
            border: 1px solid #cbd5e1;
            text-align: right;
        }}
        .signatures {{
            margin-top: 18px;
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            font-size: 13px;
            padding: 0 15px;
        }}
        .cut-line {{
            border-top: 2px dashed #94a3b8;
            text-align: center;
            margin: 6mm 0;
            position: relative;
        }}
        .cut-line span {{
            background: #fff;
            padding: 0 10px;
            position: relative;
            top: -12px;
            color: #64748b;
            font-size: 11px;
        }}
        @media print {{
            .no-print {{ display: none; }}
        }}
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
        
        # السند الأول
        v1 = rows[i]
        html += f"""
        <div class="voucher-box">
            <div class="header-logo-container">
                <div class="header-en">
                    Five-M Company For Industry<br>
                    A limited liability company<br>
                    C. R. : 1011145035<br>
                    Investment R. : 99376
                </div>
                <div class="header-logo">
                    <span>5M</span>
                </div>
                <div class="header-ar">
                    شركة ميم الخماسية للتصنيع<br>
                    شركة ذات مسئولية محدودة<br>
                    سجل تجاري : ١٠١١١٤٥٠٣٥<br>
                    سجل استثماري : ٩٩٣٧٦
                </div>
            </div>
            
            <div class="voucher-title">
                سند تسليم راتب / دفعة - {branch_name} ({month_selected}) | رقم السند: #{v1['م']:03d}
            </div>
            
            <table class="info-table">
                <tr>
                    <th>اسم الموظف</th>
                    <td><strong>{v1['الاسم']}</strong></td>
                    <th>الوظيفة / الفرع</th>
                    <td>{v1['الوظيفة']} ({v1['الفرع']})</td>
                </tr>
                <tr>
                    <th>الراتب الأساسي المستحق</th>
                    <td>{v1['الراتب الأساسي']:,.0f} ر.س</td>
                    <th>الدفعة المصروفة فعلياً</th>
                    <td style="color: #047857; font-weight: bold;">{v1['الدفعة المدفوعة']:,.0f} ر.س</td>
                </tr>
                <tr>
                    <th>المتبقي بالرصيد</th>
                    <td style="color: #b91c1c; font-weight: bold;">{v1['المتبقي']:,.0f} ر.س</td>
                    <th>نوع الإجراء المعتمد</th>
                    <td>{v1['نوع الإجراء']}</td>
                </tr>
                <tr>
                    <th>الملاحظات والبيانات</th>
                    <td colspan="3">{v1['الملاحظات'] if v1['الملاحظات'] else 'تم اعتماده وصرفه حسَب مسير الرواتب المعتمد.'}</td>
                </tr>
            </table>
            
            <div class="signatures">
                <div>توقيع واستلام الموظف: __________________</div>
                <div>اعتماد المحاسب / الإدارة: __________________</div>
            </div>
        </div>
        """
        
        # السند الثاني بالصفحة
        if i + 1 < len(rows):
            v2 = rows[i + 1]
            html += """
            <div class="cut-line">
                <span>✂️ خط القص المخصص بين السندين ✂️</span>
            </div>
            """
            html += f"""
            <div class="voucher-box">
                <div class="header-logo-container">
                    <div class="header-en">
                        Five-M Company For Industry<br>
                        A limited liability company<br>
                        C. R. : 1011145035<br>
                        Investment R. : 99376
                    </div>
                    <div class="header-logo">
                        <span>5M</span>
                    </div>
                    <div class="header-ar">
                        شركة ميم الخماسية للتصنيع<br>
                        شركة ذات مسئولية محدودة<br>
                        سجل تجاري : ١٠١١١٤٥٠٣٥<br>
                        سجل استثماري : ٩٩٣٧٦
                    </div>
                </div>
                
                <div class="voucher-title">
                    سند تسليم راتب / دفعة - {branch_name} ({month_selected}) | رقم السند: #{v2['م']:03d}
                </div>
                
                <table class="info-table">
                    <tr>
                        <th>اسم الموظف</th>
                        <td><strong>{v2['الاسم']}</strong></td>
                        <th>الوظيفة / الفرع</th>
                        <td>{v2['الوظيفة']} ({v2['الفرع']})</td>
                    </tr>
                    <tr>
                        <th>الراتب الأساسي المستحق</th>
                        <td>{v2['الراتب الأساسي']:,.0f} ر.س</td>
                        <th>الدفعة المصروفة فعلياً</th>
                        <td style="color: #047857; font-weight: bold;">{v2['الدفعة المدفوعة']:,.0f} ر.س</td>
                    </tr>
                    <tr>
                        <th>المتبقي بالرصيد</th>
                        <td style="color: #b91c1c; font-weight: bold;">{v2['المتبقي']:,.0f} ر.س</td>
                        <th>نوع الإجراء المعتمد</th>
                        <td>{v2['نوع الإجراء']}</td>
                    </tr>
                    <tr>
                        <th>الملاحظات والبيانات</th>
                        <td colspan="3">{v2['الملاحظات'] if v2['الملاحظات'] else 'تم اعتماده وصرفه حسَب مسير الرواتب المعتمد.'}</td>
                    </tr>
                </table>
                
                <div class="signatures">
                    <div>توقيع واستلام الموظف: __________________</div>
                    <div>اعتماد المحاسب / الإدارة: __________________</div>
                </div>
            </div>
            """
            
        html += '</div>'
        
    html += "</body></html>"
    output.write(html.encode('utf-8'))
    output.seek(0)
    return output

# 4. الشاشات
if '📊' in menu:
    st.title('📊 شاشة إدخال وتعديل الدفعات (حسب الفرع)')
    st.write('قم بتسجيل الدفعات والملاحظات لكل فرع، وستتحدث الحسابات وسندات القبض تلقائياً.')
    
    t1, t2, t3 = st.tabs(['📍 فرع الخرج (35 موظف)', '📍 فرع المستودع (5 موظفين)', '📍 فرع الملقة (12 موظف)'])
    branches = [('الخرج', t1), ('المستودع', t2), ('الملقة', t3)]
    
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
                    "نوع الإجراء": st.column_config.SelectboxColumn(
                        "نوع الإجراء",
                        options=["صرف كامل", "خصم غياب", "جزاء إداري", "حوافز وأداء", "سداد سلفة", "لم يُصرف"]
                    ),
                    "الملاحظات": st.column_config.TextColumn("الملاحظات")
                },
                use_container_width=True,
                key=f"editor_{b_name}"
            )
            
            edited_b['المتبقي'] = edited_b['الراتب الأساسي'] - edited_b['الدفعة المدفوعة']
            st.session_state.payroll_df.update(edited_b)
            
            req = edited_b['الراتب الأساسي'].sum()
            paid = edited_b['الدفعة المدفوعة'].sum()
            rem = edited_b['المتبقي'].sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric(f'مستحق فرع {b_name}', f'{req:,.0f} ر.س')
            c2.metric(f'مصروف فرع {b_name}', f'{paid:,.0f} ر.س')
            c3.metric(f'متبقي فرع {b_name}', f'{rem:,.0f} ر.س')

elif '💼' in menu:
    st.title('💼 سجل الموظفين والإجماليات المالية الحالية')
    s1, s2, s3 = st.tabs(['سجل فرع الخرج', 'سجل فرع المستودع', 'سجل فرع الملقة'])
    
    for b_name, tab_obj in [('الخرج', s1), ('المستودع', s2), ('الملقة', s3)]:
        with tab_obj:
            df_b = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == b_name]
            st.dataframe(df_b[['م', 'الاسم', 'الوظيفة', 'الراتب الأساسي', 'الدفعة المدفوعة', 'المتبقي', 'نوع الإجراء', 'الملاحظات']], use_container_width=True)
            
            req = df_b['الراتب الأساسي'].sum()
            paid = df_b['الدفعة المدفوعة'].sum()
            rem = df_b['المتبقي'].sum()
            
            st.info(f"📊 **إجمالي فرع {b_name}:** المستحق: **{req:,.0f} ر.س** | المصروف: **{paid:,.0f} ر.س** | المتبقي: **{rem:,.0f} ر.س**")

    st.divider()
    st.subheader('🌐 الإجمالي العام للشركة (52 موظف)')
    tot_req = st.session_state.payroll_df['الراتب الأساسي'].sum()
    tot_paid = st.session_state.payroll_df['الدفعة المدفوعة'].sum()
    tot_rem = st.session_state.payroll_df['المتبقي'].sum()
    
    g1, g2, g3 = st.columns(3)
    g1.metric('إجمالي رواتب الشركة', f'{tot_req:,.0f} ر.س')
    g2.metric('إجمالي الدفعات المسلمة', f'{tot_paid:,.0f} ر.س')
    g3.metric('إجمالي المتبقي الكلي', f'{tot_rem:,.0f} ر.س')

elif '🖨️' in menu:
    st.title('🖨️ طباعة سندات القبض الرسمية (A4)')
    st.write('قم باختيار الفرع واستعراض السندات المنظمة مع الهيدر الرسمي للشركة.')
    
    selected_b = st.selectbox('اختر الفرع للتصدير والطباعة:', ['جميع الفروع (52 موظف)', 'الخرج', 'المستودع', 'الملقة'])
    
    if selected_b == 'جميع الفروع (52 موظف)':
        df_print = st.session_state.payroll_df
    else:
        df_print = st.session_state.payroll_df[st.session_state.payroll_df['الفرع'] == selected_b]
        
    pdf_bytes = generate_pretty_html_pdf(df_print, selected_b)
    
    st.download_button(
        label=f"📄 فتح واستعراض سندات قبض {selected_b} بالهيدر الرسمي 🖨️",
        data=pdf_bytes,
        file_name=f"سندات_قبض_{selected_b}.html",
        mime="text/html"
    )

elif '➕' in menu:
    st.title('🚀 إضافة نظام جديد مستقبلاً')
    st.selectbox('اختر الموديل:', ['نظام الحضور والانصراف والبصمة', 'نظام إدارة طلبات الإجازات', 'نظام حساب مكافأة نهاية الخدمة'])
    st.button('تفعيل النظام')
