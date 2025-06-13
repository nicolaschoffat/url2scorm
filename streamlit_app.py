import streamlit as st
import zipfile
import io
from datetime import timedelta

# Templates pour le manifest SCORM 1.2 et SCORM 2004
MANIFEST_12 = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.example.scorm" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2
          imscp_rootv1p1p2.xsd">
  <organizations default="ORG">
    <organization identifier="ORG">
      <title>SCORM Module</title>
      <item identifier="ITEM" identifierref="RES">
        <title>SCORM URL Content</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/>
    </resource>
  </resources>
</manifest>
'''

MANIFEST_2004 = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.example.scorm" version="1.0"
          xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_v1p3"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1 imscp_v1p1.xsd">
  <organizations default="ORG">
    <organization identifier="ORG">
      <title>SCORM Module</title>
      <item identifier="ITEM" identifierref="RES">
        <title>SCORM URL Content</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES" type="webcontent" adlcp:scormType="sco" href="index.html">
      <file href="index.html"/>
    </resource>
  </resources>
</manifest>
'''

# HTML + JS avec minuterie
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
  <title>SCORM Content</title>
  <script>
    let scormAPI = null;
    let elapsed = 0;
    const requiredTime = {time};

    function findAPI(win) {
      if (win.API) return win.API;
      if (win.parent && win.parent !== win) return findAPI(win.parent);
      return null;
    }

    function initSCORM() {
      scormAPI = findAPI(window);
      if (scormAPI) scormAPI.LMSInitialize("");
    }

    function checkTime() {
      elapsed++;
      if (elapsed >= requiredTime) {
        if (scormAPI) {
          scormAPI.LMSSetValue("cmi.core.lesson_status", "completed");
          scormAPI.LMSCommit("");
        }
        clearInterval(timer);
      }
    }

    window.onload = function() {
      initSCORM();
      timer = setInterval(checkTime, 1000);
      document.getElementById("target").src = "{url}";
    }
  </script>
</head>
<body>
  <h2>Chargement du contenu...</h2>
  <iframe id="target" width="100%" height="600px"></iframe>
</body>
</html>
'''

# --- Streamlit App ---
st.title("Générateur de paquet SCORM")

url = st.text_input("URL à consulter", "https://example.com")
scorm_version = st.selectbox("Version SCORM", ["SCORM 1.2", "SCORM 2004 3rd edition"])
duration = st.number_input("Durée minimale (en secondes)", min_value=1, value=30)

if st.button("Générer le SCORM"):
    # Créer un zip en mémoire
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        html_content = HTML_TEMPLATE.replace("{url}", url).replace("{time}", str(duration))
        zf.writestr("index.html", html_content)

        if scorm_version == "SCORM 1.2":
            zf.writestr("imsmanifest.xml", MANIFEST_12)
        else:
            zf.writestr("imsmanifest.xml", MANIFEST_2004)

    st.success("Fichier SCORM généré !")
    st.download_button("📥 Télécharger le paquet SCORM", data=buffer.getvalue(), file_name="scorm_package.zip")
