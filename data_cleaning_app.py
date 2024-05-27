import streamlit as st
import pandas as pd

def clean_data(data):
    # 将相关列转换为数值类型
    data['Uds. fabricadas'] = pd.to_numeric(data['Uds. fabricadas'].replace(',', '.', regex=True), errors='coerce')
    data['Run Time'] = pd.to_numeric(data['Run Time'].replace(',', '.', regex=True), errors='coerce')
    data['Tpo STD'] = pd.to_numeric(data['Tpo STD'].replace(',', '.', regex=True), errors='coerce')
    data['Desv vs STD'] = pd.to_numeric(data['Desv vs STD'].str.replace('%', '').replace(',', '.', regex=True), errors='coerce')

    # 计算原始数据集中"Uds. fabricadas"和"Run Time"的总和
    total_uds_fabricadas = data['Uds. fabricadas'].sum()
    total_run_time = data['Run Time'].sum()
    total_rows = len(data)

    # 删除"Desv vs STD"中有无效值的行
    data_cleaned = data.dropna(subset=['Desv vs STD'])

    # 删除"Uds. fabricadas"、"Run Time"、"Tpo STD"小于1的行
    data_cleaned = data_cleaned[(data_cleaned['Uds. fabricadas'] >= 1) &
                                (data_cleaned['Run Time'] >= 1) &
                                (data_cleaned['Tpo STD'] >= 1)]

    # 删除所有列中包含无效值的行
    data_cleaned = data_cleaned.dropna()

    # 计算清理后数据集中"Uds. fabricadas"和"Run Time"的总和
    cleaned_uds_fabricadas = data_cleaned['Uds. fabricadas'].sum()
    cleaned_run_time = data_cleaned['Run Time'].sum()

    # 计算删除的行数和比例
    deleted_rows = total_rows - len(data_cleaned)
    deleted_rows_ratio = deleted_rows / total_rows

    # 计算删除的行对应的数值总和与整个数据集的比例
    uds_fabricadas_deleted_ratio = (total_uds_fabricadas - cleaned_uds_fabricadas) / total_uds_fabricadas
    run_time_deleted_ratio = (total_run_time - cleaned_run_time) / total_run_time

    # 在"Desv vs STD"列中的数值后添加百分比符号
    data_cleaned['Desv vs STD'] = data_cleaned['Desv vs STD'].astype(str) + '%'

    # 返回清理后的数据和删除的比例信息
    return data_cleaned, deleted_rows_ratio, uds_fabricadas_deleted_ratio, run_time_deleted_ratio

def main():
    st.title('数据清理应用程序')
    st.write("上传你的CSV文件以清理数据")

    # 上传CSV文件
    uploaded_file = st.file_uploader("上传CSV文件", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, sep=',', skiprows=1)
        
        # 清理数据
        cleaned_data, deleted_rows_ratio, uds_fabricadas_deleted_ratio, run_time_deleted_ratio = clean_data(data)
        
        # 显示删除比例
        st.write(f"删除的行比例: {deleted_rows_ratio:.2%}")
        st.write(f"删除的'Uds. fabricadas'比例: {uds_fabricadas_deleted_ratio:.2%}")
        st.write(f"删除的'Run Time'比例: {run_time_deleted_ratio:.2%}")
        
        # 显示清理后的数据
        st.write("清理后的数据:")
        st.write(cleaned_data.head())
        
        # 下载清理后的数据
        cleaned_data_csv = cleaned_data.to_csv(index=False, sep=';', decimal=',')
        st.download_button(label="下载清理后的数据", data=cleaned_data_csv, file_name='cleaned_data.csv', mime='text/csv')

if __name__ == "__main__":
    main()
