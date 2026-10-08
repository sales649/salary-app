with open('streamlit_app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'elif selected_option in' in line or 'elif st.session_state' in line:
        if 'SyntaxError' in line or "'" not in line or "]" not in line or line.count("'") % 2 != 0:
            lines[i] = "    elif selected_option in ['عقود السائقين', 'عقود الموظفين']:\n"

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
