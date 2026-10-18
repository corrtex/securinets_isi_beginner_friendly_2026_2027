import random, string
junk = [''.join(random.choices(string.ascii_letters, k=20)) for _ in range(5000)]
junk.insert(2500, "Securinets{th3r3_1s_n0_5uch_th1ngs_4s_psych1cs}")
open("redjohn.png", "ab").write(("\n".join(junk)).encode())
