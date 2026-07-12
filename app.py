import streamlit as st
import cadconvert
import os

st.set_page_config(page_title="DWG to DXF", layout="centered")

st.title("DWG ➔ DXF 変換ツール")
st.write("スマホやPCからDWGファイルをアップロードするだけで、即座にDXFへ変換します。")

# ファイルアップローダー
uploaded_file = st.file_uploader("DWGファイルを選択してください", type=["dwg"])

if uploaded_file is not None:
    # 1. アップロードされたDWGファイルを一時保存
    input_dwg = "input_file.dwg"
    output_dxf = "output_file.dxf"
    
    with open(input_dwg, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.info("変換処理を実行中...")
    
    try:
        # 2. cadconvertを使ってDWGからDXFへ変換
        # 外部サービスを一切使わず、サーバー内部で処理します
        cadconvert.convert(input_dwg, output_dxf)
        
        # 3. 変換成功メッセージとダウンロードボタンの表示
        st.success("変換が完了しました！以下のボタンから保存してください。")
        
        with open(output_dxf, "rb") as f:
            st.download_button(
                label="📁 DXFファイルをダウンロード",
                data=f,
                file_name=uploaded_file.name.rsplit('.', 1)[0] + ".dxf",
                mime="application/dxf"
            )
            
    except Exception as e:
        st.error("変換中にエラーが発生しました。ファイルが破損しているか、未対応のバージョンです。")
        st.caption(f"エラー詳細: {str(e)}")
        
    finally:
        # 4. サーバー内のお掃除（不要なファイルを削除）
        if os.path.exists(input_dwg):
            os.remove(input_dwg)
        if os.path.exists(output_dxf):
            os.remove(output_dxf)

