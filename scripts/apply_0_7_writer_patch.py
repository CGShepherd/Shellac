from pathlib import Path

writer = Path("generator/writers/kicad9.py")
text = writer.read_text(encoding="utf-8")
needle = '"Connector_Generic:Conn_01x03": 3,'
addition = '"Connector_Generic:Conn_01x05": 5,'

if addition in text:
    print("Writer already supports Conn_01x05.")
elif needle in text:
    text = text.replace(needle, needle + "\n    " + addition)
    writer.write_text(text, encoding="utf-8")
    print("Added Conn_01x05 support.")
else:
    raise SystemExit("Could not locate Conn_01x03 PIN_COUNTS entry.")
