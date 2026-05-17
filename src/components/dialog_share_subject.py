import io
import urllib.parse
import urllib.request

import streamlit as st


def _make_qr_png(data: str) -> bytes:
    try:
        import qrcode

        buf = io.BytesIO()
        qrcode.make(data).save(buf, format="PNG")
        return buf.getvalue()
    except ModuleNotFoundError:
        pass

    try:
        import segno

        buf = io.BytesIO()
        segno.make(data).save(buf, kind="png", scale=10, border=1)
        return buf.getvalue()
    except ModuleNotFoundError:
        pass

    url = (
        "https://api.qrserver.com/v1/create-qr-code/?"
        f"size=300x300&format=png&data={urllib.parse.quote(data)}"
    )
    with urllib.request.urlopen(url, timeout=15) as response:
        return response.read()


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    join_url = (
        f"https://snapclass-mithragoud123.streamlit.app/?join-code={subject_code}"
    )

    st.header("Scan to Join")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info("Copy this link to share on Whatsapp or Email")

    with col2:
        st.markdown("### Scan to Join")
        st.image(_make_qr_png(join_url), caption="QR code for class joining")
