import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, Notify
from mtranslate import translate

def _clipboard_changed(clipboard, event):
    text = clipboard.wait_for_text()
    if not isinstance(text, str):
        return
    
    translated = translate(text, 'vi', 'en')
    Notify.Notification.new(text + ': ' + translated).show()

print('Instant Translator')
print('Put any text into the clipboard for auto translating to Vietnamese')
print('(Select text then press Ctrl+C)')
Notify.init("Instant Translator")
clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
clip.connect("owner-change", _clipboard_changed)

Gtk.main()
