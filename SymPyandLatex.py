import sympy as sp
from io import BytesIO
import win32clipboard
from PIL import Image

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

x,y = sp.symbols('x,y')
eqn = sp.sin(sp.sqrt(x**2 + 20)) + y/(sp.factorial(x) - 2) + (x**2 * sp.sqrt(y))/3
f = BytesIO()
sp.preview(eqn, viewer='BytesIO', outputbuffer=f)
f.seek(0)
outp = BytesIO()
#img = Image.new("RGB", (200, 200), (255, 0, 0))
img = Image.open(f)
img.convert("RGBA").save(outp, "BMP")
data = outp.getvalue()[14:]
outp.close()
send_to_clipboard(win32clipboard.CF_DIB, data)
#sp.preview(eqn, viewer='file', filename='ooo.png')