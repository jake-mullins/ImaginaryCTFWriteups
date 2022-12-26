# Directions
Using xxd, we can get the byte representation of the compressed file.

```
┌──(jake㉿Horus)-[~/ImaginaryCTFWriteups/Directions-12-20-2022]
└─$ xxd out.zip
00000000: 504b 0304 1400 0200 0800 e21a 9455 fa75  PK...........U.u
00000010: 48b9 3200 0000 3800 0000 0800 1c00 666c  H.2...8.......fl
00000020: 6167 2e74 7874 5554 0900 0318 9ba1 634e  ag.txtUT......cN
00000030: 9ba1 6375 780b 0001 04e8 0300 0004 e803  ..cux...........
00000040: 0000 cb4a 2e49 ab2e 4a4d 894f cb49 4c2f  ...J.I..JM.O.IL/
00000050: 8e4f cc03 b212 b353 a1dc b4fc a25c a058  .O.....S.....\.X
00000060: 7c6a 6169 6659 624e 6a5e 726a 7c72 4e62  |jaifYbNj^rj|rNb
00000070: 7171 2d00 504b 0304 1400 0200 0800 251b  qq-.PK........%.
00000080: 9455 e353 f2ae 4200 0000 4f00 0000 0800  .U.S..B...O.....
00000090: 1c00 6661 6b65 2e74 7874 5554 0900 0395  ..fake.txtUT....
000000a0: 9ba1 6395 9ba1 6375 780b 0001 04e8 0300  ..c...cux.......
000000b0: 0004 e803 0000 05c1 410e 8020 0c04 c0e7  ........A.. ....
000000c0: f8ac 0de2 024d b035 74a3 07e3 df9d b1aa  .....M.5t.......
000000d0: f66a 58c2 c923 a1c0 4e14 78b8 96dd 5626  .jX..#..N.x...V&
000000e0: 26bd 6ba0 cdd2 110b 9c49 98f0 846f 42a7  &.k......I...oB.
000000f0: 50e3 bc16 3379 7c3f 504b 0102 1e03 1400  P...3y|?PK......
00000100: 0200 0800 e21a 9455 fa75 48b9 3200 0000  .......U.uH.2...
00000110: 3800 0000 0800 1800 0000 0000 0100 0000  8...............
00000120: ff81 0000 0000 6661 6b65 2e74 7874 5554  ......fake.txtUT
00000130: 0500 0318 9ba1 6375 780b 0001 04e8 0300  ......cux.......
00000140: 0004 e803 0000 504b 0102 1e03 1400 0200  ......PK........
00000150: 0800 251b 9455 e353 f2ae 4200 0000 4f00  ..%..U.S..B...O.
00000160: 0000 0800 1800 0000 0000 0100 0000 ff81  ................
00000170: 0000 0000 666c 6167 2e74 7874 5554 0500  ....flag.txtUT..
00000180: 0395 9ba1 6375 780b 0001 04e8 0300 0004  ....cux.........
00000190: e803 0000 504b 0506 0000 0000 0200 0200  ....PK..........
000001a0: 9c00 0000 f800 0000 0000                 ..........
```

Consulting <a>https://en.wikipedia.org/wiki/ZIP_(file_format)</a>, we find out that a zip files are represented with the following format ![zip format](https://upload.wikimedia.org/wikipedia/commons/6/63/ZIP-64_Internal_Layout.svg).

Notice that the order in the Central Directory reflects the order of the compressed files. The central directory portion of the file goes from 0xf8 to the end of the file. After I went through a long process of individually going through the bytes and comparing them, mostly as practice, I noticed that the order of the files in the **body** is:

    1. ```flag.txt```
    2. ```fake.txt```

whereas the order of the headers in the **central directory** is 

    1. ```fake.txt```
    2. ```flag.txt```

The first solution was to completely remove the references to ```fake.txt``` in both the body and the central directory, using the following script:

```
data = open("out.zip", "rb").read()

flag_data = data[0:0x74]
fake_data = data[0x74:0xf8]

fake_header = data[0xf8:0x146]
flag_header = data[0x146:0x194]
eocd_record = data[0x194:]

# Lets just straight up remove fake
new_data = flag_data + flag_header + eocd_record

f = open("fixed.zip", "wb")
f.write(new_data)
```

Eahc one of these sections starts with 0x504b (```PK```).

But this didn't work for an unknown error. Likely a sizing issue, but instead of tracking that down, I noticed that the header entry for ```flag.txt``` says that the relative offset of ```flag.txt``` at 0x00. As such, there should be no issue with simply flipping around the central directory entry for ```flag.txt```. We can accomplish this by changing the 3rd to last line:
```
new_data = flag_data + fake_data + flag_header + fake_header + eocd_record
```

This reveals a false flag. The entries for both ```flag.txt``` and ```fake.txt``` list their respective offsets within the file body as 0x00. If we manually changing the value at 0x170 to 0x74, the address of the compressed ```fake.txt``` file, we can see that it decompresses successfully into the real flag.