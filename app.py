import streamlit as st
import ezdxf
import os

st.title("DWG ➔ DXF 変換ツール")
st.write("DWGファイルをアップロードすると、DXFに変換してダウンロードできます。")

uploaded_file = st.file_uploader("DWGファイルを選択", type=["dwg", "dxf"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    st.info("変換処理中...")
    
    try:
        # ezdxfでファイルを読み込む
        # ※ezdxfはDWGを直接保存するのではなく、内部でDXF構造を再構築します
        doc = ezdxf.readb(file_bytes) if uploaded_file.name.lower().endswith('.dwg') else ezdxf.read_string(file_bytes.decode('utf-8', errors='ignore'))
        
        # 一時的なDXFファイルとして保存
        output_filename = "converted.dxf"
        doc.saveas(output_filename)
        
        with open(output_filename, "rb") as f:
            st.download_button(
                label="DXFファイルをダウンロード",
                data=f,
                file_name=uploaded_file.name.rsplit('.', 1)[0] + ".dxf",
                mime="application/dxf"
            )
        st.success("変換が完了しました！")
        
        # 終わったらゴミ掃除
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
    except Exception as e:
        st.error(f"エラーが発生しました。ファイル形式が対応していない可能性があります。")
        st.caption(f"エラー詳細: {str(e)}")

