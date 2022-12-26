data = open("out.zip", "rb").read()

flag_data = data[0:0x74]
fake_data = data[0x74:0xf8]

fake_header = data[0xf8:0x146]
flag_header = data[0x146:0x194]
eocd_record = data[0x194:]

# Lets just straight up remove fake
new_data = flag_data + fake_data + flag_header + fake_header + eocd_record

f = open("fixed.zip", "wb")
f.write(new_data)