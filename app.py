import streamlit as st
import aspose.cad as cad
import os

st.title("DWG ➔ DXF 変換ツール")
st.write("DWGファイルをアップロードすると、DXFに変換してダウンロードできます。")

uploaded_file = st.file_uploader("DWGファイルを選択", type=["dwg"])

if uploaded_file is not None:
    with open("temp.dwg", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.info("変換中...")
    
    # 変換処理
    image = cad.Image.load("temp.dwg")
    options = cad.imageoptions.DxfOptions()
    image.save("temp.dxf", options)
    
    with open("temp.dxf", "rb") as f:
        st.download_button(
            label="DXFファイルをダウンロード",
            data=f,
            file_name=uploaded_file.name.replace(".dwg", ".dxf"),
            mime="application/dxf"
        )
    st.success("変換が完了しました！")
