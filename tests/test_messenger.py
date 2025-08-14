import pywhatkit as kit


def test_send_whatsapp_msg():
    kit.sendwhatmsg_instantly("+4915782987461", "Test", tab_close=True)


