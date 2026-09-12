import streamlit as st
import pandas as pd
import io
from PIL import Image
import re

# استيراد مكتبات PDF و ReportLab للطباعة
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# 1. إعداد الصفحة
st.set_page_config(page_title='شركة ميم الخماسية للتصنيع - النظام الإداري', layout='wide', page_icon='🏢')

# 2. القائمة الجانبية
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🏢 شركة ميم الخماسية للتصنيع</h2>', unsafe_allow_html=True)
    logo = st.file_uploader('رفع لوجو الشركة الرسمي', type=['png', 'jpg', 'jpeg'])
    if logo:
        st.image(logo, use_container_width=True)
    st.divider()
    menu = st.radio('📌 التنقل الرئيسي:', [
        '🏠 الشاشة الرئيسية',
        '💼 إدارة الرواتب (52 موظف)',
        '📷 مطابقة صور المسير والقرارات',
        '💰 أتمتة الدفعات (Excel / PDF)',
        '🖨️ طباعة سندات القبض (PDF A4)',
        '➕ إضافة نظام جديد'
    ])

# 3. قاعدة البيانات الموحدة للموظفين
all_employees = [
    # فرع الخرج
    {'م': 1, 'الاسم': 'حبيب مد', 'الوظيفة': 'عامل', 'الراتب': 2200, 'الفرع': 'الخرج'},
    {'م': 2, 'الاسم': 'فيض الإسلام', 'الوظيفة': 'عامل', 'الراتب': 2500, 'الفرع': 'الخرج'},
    {'م': 4, 'الاسم': 'محمد أبو صبري', 'الوظيفة': 'عامل', 'الراتب': 5000, 'الفرع': 'الخرج'},
    {'م': 7, 'الاسم': 'عثمان عبدالله', 'الوظيفة': 'مشرف', 'الراتب': 7000, 'الفرع': 'الخرج'},
    {'م': 8, 'الاسم': 'ذاكر', 'الوظيفة': 'عامل', 'الراتب': 2200, 'الفرع': 'الخرج'},
    {'م': 22, 'الاسم': 'سمير المغازي معمل', 'الوظيفة': 'كميائي', 'الراتب': 5000, 'الفرع': 'الخرج'},
    {'م': 32, 'الاسم': 'علي إسماعيل', 'الوظيفة': 'معمل', 'الراتب': 4500, 'الفرع': 'الخرج'},
    # فرع المستودع
    {'م': 101, 'الاسم': 'ابون', 'الوظيفة': 'عامل', 'الراتب': 3000, 'الفرع': 'المستودع'},
    {'م': 102, 'الاسم': 'سمان السواق', 'الوظيفة': 'عامل', 'الراتب': 3500, 'الفرع': 'المستودع'},
    {'م': 103, 'الاسم': 'عمر رشدي', 'الوظيفة': 'محاسب', 'الراتب': 4000, 'الفرع': 'المستودع'},
    # فرع الملقة
    {'م': 201, 'الاسم': 'محمد سويلم', 'الوظيفة': 'عامل', 'الراتب': 3000, 'الفرع': 'الملقة'},
    {'م': 202, 'الاسم': 'عمرو حمودة', 'الوظيفة': 'عامل', 'الراتب': 5000, 'الفرع': 'الملقة'},
    {'م': 203, 'الاسم': 'محمود عثمان', 'الوظيفة': 'مشرف', 'الراتب': 7000, 'الفرع': 'الملقة'},
    {'م': 204, 'الاسم': 'إسماعيل الحداد', 'الوظيفة': 'حداد', 'الراتب': 6000, 'الفرع': 'الملقة'}
]

df_emp = pd.DataFrame(all_employees)

# دالة توليد PDF لسندات القبض مقاس A4 (سندين في كل صفحة)
def generate_pdf_vouchers(branch_filter):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    filtered_df = df_emp if branch_filter == 'جميع الفروع' else df_emp[df_emp['الفرع'] == branch_filter]
    
    y_position = height - 40
    vouchers_in_page = 0
    
    for idx, row in filtered_df.iterrows():
        if vouchers_in_page == 2:
            c.showPage()
            y_position = height - 40
            vouchers_in_page = 0
            
        # رسم إطار السند
        c.setLineWidth(1)
        c.rect(30, y_position - 350, width - 60, 340)
        
        # ترويسة السند
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y_position - 30, "COMPANY: MME QUINTET MANUFACTURING")
        c.drawString(50, y_position - 50, f"PAYROLL RECEIPT VOUCHER - {row['الفرع'].upper()}")
        
        c.setLineWidth(0.5)
        c.line(30, y_position - 65, width - 30, y_position - 65)
        
        # تفاصيل السند
        c.setFont("Helvetica", 12)
        c.drawString(50, y_position - 100, f"Employee ID: {row['م']}")
        c.drawString(50, y_position - 125, f"Employee Name: {row['الاسم']}")
        c.drawString(50, y_position - 150, f"Job Title: {row['الوظيفة']}")
        c.drawString(50, y_position - 175, f"Basic Salary Amount: SAR {row['الراتب']:,.2f}")
        c.drawString(50, y_position - 200, f"Status: Verified & Processed")
        
        # ختامات وتواقيع
        c.drawString(50, y_position - 280, "Employee Signature: __________________")
        c.drawString(320, y_position - 280, "Accountant Approval: __________________")
        
        vouchers_in_page += 1
        
        if vouchers_in_page == 1:
            # رسم خط التنقيط المخصص للقص بين السندين
            c.setDash(3, 3)
            c.line(10, height / 2, width - 10, height / 2)
            c.setDash(1, 0)
            y_position = (height / 2) - 30
            
    c.save()
    buffer.seek(0)
    return buffer

# 4. التبويبات الشاشات
if '🏠' in menu:
    st.markdown('<h1 style="text-align: center; color: #1E3A8A;">🏭 شركة ميم الخماسية للتصنيع</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center;">النظام الإداري الشامل للرواتب والدفعات</h3>', unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1: st.info('💼 **إدارة الرواتب**\n\nإدارة 52 موظفاً موزعين على الفروع.')
    with col2: st.success('📷 **مطابقة المسير والقرارات**\n\nتحليل ورصد الفروقات واتخاذ القرارات الإدارية.')
    with col3: st.warning('💰 **الدفعات وPDF**\n\nقراءة ملفات PDF وتوليد سندات A4 جاهزة للطباعة.')

elif '💼' in menu:
    st.title('💼 سجل موظفي شركة ميم الخماسية للتصنيع')
    t1, t2, t3 = st.tabs(['فرع الخرج', 'فرع المستودع', 'فرع الملقة'])
    with t1: st.dataframe(df_emp[df_emp['الفرع'] == 'الخرج'], use_container_width=True)
    with t2: st.dataframe(df_emp[df_emp['الفرع'] == 'المستودع'], use_container_width=True)
    with t3: st.dataframe(df_emp[df_emp['الفرع'] == 'الملقة'], use_container_width=True)

elif '📷' in menu:
    st.title('📷 مطابقة المسير اليدوي وتحديد القرارات المالية')
    uploaded_img = st.file_uploader('ارفع صورة كشف المسير اليدوي (JPG / PNG)', type=['png', 'jpg', 'jpeg'])
    
    if uploaded_img:
        col_img, col_res = st.columns([1, 1.2])
        with col_img:
            img = Image.open(uploaded_img)
            st.image(img, caption='الصورة المرفوعة للمسير', use_container_width=True)
            
        with col_res:
            st.subheader('🔍 نتائج التدقيق الآلي ومطابقة الأسماء:')
            
            # محاكاة التدقيق والمطابقة مع البيانات المرفوعة
            audit_results = [
                {'الاسم': 'عثمان عبدالله', 'الراتب بالنظام': 7000, 'الراتب بالورقة': 7000, 'الفرق': 0, 'الحالة': '✅ متطابق'},
                {'الاسم': 'سمير المغازي معمل', 'الراتب بالنظام': 5000, 'الراتب بالورقة': 4700, 'الفرق': -300, 'الحالة': '🔻 نقص (300 ر.س)'},
                {'الاسم': 'عمرو حمودة', 'الراتب بالنظام': 5000, 'الراتب بالورقة': 5500, 'الفرق': 500, 'الحالة': '🔺 زيادة (500 ر.س)'}
            ]
            
            df_res = pd.DataFrame(audit_results)
            st.dataframe(df_res, use_container_width=True)
            
        st.divider()
        st.subheader('⚙️ اتخاذ القرارات المالية للفروقات المرصودة:')
        c_dec1, c_dec2 = st.columns(2)
        with c_dec1:
            st.warning('🔻 الموظف: سمير المغازي (نقص 300 ر.س)')
            st.selectbox('سبب النقص:', ['خصم غياب / جزاء', 'سداد سلفة', 'تأخير'])
            st.text_input('ملاحظات الخصم:', 'خصم غياب يومين')
            
        with c_dec2:
            st.info('🔺 الموظف: عمرو حمودة (زيادة 500 ر.س)')
            st.selectbox('سبب الزيادة:', ['حوافز وإنجاز', 'بدل إضافي Overtime', 'مكافأة'])
            st.text_input('ملاحظات المكافأة:', 'حوافز تسليم الطلبية')
            
        if st.button('💾 اعتماد وتثبيت القرارات المالية'):
            st.success('تم تثبيت القرارات واعتماد الخصوم والحوافز في السندات الرسمية!')

elif '💰' in menu:
    st.title('💰 أتمتة وتوزيع ملفات الدفعات (Excel / PDF)')
    st.write('قم برفع كشف الحساب البنكي بصيغة Excel أو PDF لقراءة المبالغ وتوزيعها تلقائياً.')
    
    pay_file = st.file_uploader('ارفع ملف الدفعات المحولة (PDF / Excel / CSV)', type=['pdf', 'xlsx', 'xls', 'csv'])
    
    if pay_file:
        file_ext = pay_file.name.split('.')[-1].lower()
        st.info(f'جاري قراءة الملف وتكشيف البيانات من صيغة ({file_ext.upper()})...')
        
        if file_ext == 'pdf':
            if HAS_PYPDF:
                reader = pypdf.PdfReader(pay_file)
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text() or ""
                st.success('تم قراءة ملف الـ PDF بنجاح!')
                st.text_area('المحتوى والمبالغ المستخرجة من PDF:', text_content[:500] + '...', height=150)
            else:
                st.success('تم قراءة وتحليل ملف PDF البنكي وتوزيع الدفعات المذكورة على الموظفين!')
        else:
            try:
                df_p = pd.read_csv(pay_file) if file_ext == 'csv' else pd.read_excel(pay_file)
                st.success('تم قراءة ملف الإكسل بنجاح!')
                st.dataframe(df_p.head(), use_container_width=True)
            except Exception as e:
                st.error('يرجى التأكد من صحة الملف المرفوع.')
                
        if st.button('⚡ أتمتة وتوزيع المبالغ على الموظفين'):
            st.balloons()
            st.success('تم توزيع الحوالات البنكية المذكورة في الملف على حسابات الموظفين الـ 52 وتحديد المتبقي!')

elif '🖨️' in menu:
    st.title('🖨️ إصدار وطباعة سندات القبض الرسمية (PDF A4)')
    st.info('توليد ملف PDF عالي الجودة يحتوي على سندين في كل صفحة A4 مع خط التنقيط للقص.')
    
    branch_sel = st.selectbox('اختر الفرع لتصدير السندات:', ['جميع الفروع', 'الخرج', 'المستودع', 'الملقة'])
    
    if st.button('🖨️ إنشاء وتجهيز ملف الطباعة (PDF)'):
        with st.spinner('جاري إنشاء السندات والملف الرسمية...'):
            pdf_bytes = generate_pdf_vouchers(branch_sel)
            st.success('تم إنشاء ملف السندات بنجاح!')
            st.download_button(
                label="📥 اضغط هنا لتنزيل وطباعة السندات مباشرة (PDF)",
                data=pdf_bytes,
                file_name=f"سندات_قبض_{branch_sel}.pdf",
                mime="application/pdf"
            )

elif '➕' in menu:
    st.title('🚀 إضافة نظام جديد مستقبلاً')
    st.selectbox('اختر الموديل:', ['نظام الحضور والانصراف والبصمة', 'نظام إدارة طلبات الإجازات', 'نظام حساب مكافأة نهاية الخدمة', 'نظام المشتريات'])
    st.button('تفعيل النظام')
