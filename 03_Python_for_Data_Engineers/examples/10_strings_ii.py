# Module 03, 10 · Strings-II: Problem Solving with Strings
# Every runnable example from the topic, in order.
# Run:  python 10_strings_ii.py

print(ord("A"), ord("Z"), ord("a"), ord("z"), ord("0"))
print(chr(65), chr(97), chr(48))

print(ord("a") - ord("A"))          # distance between lower and upper case
print(chr(ord("A") + 2))            # two letters after A
print(ord("d") - ord("a"))          # position of d in the alphabet (a = 0)

text = "Data Engineering at XYZ Company"

vowels = 0
consonants = 0
for ch in text.lower():
    if ch.isalpha():
        if ch in "aeiou":
            vowels += 1
        else:
            consonants += 1

print("Vowels:", vowels, " Consonants:", consonants)

text = "banana split"

freq = {}
for ch in text:
    if ch != " ":
        freq[ch] = freq.get(ch, 0) + 1

for ch, n in sorted(freq.items()):
    print(ch, n)

sample = "Order#4521 for Meera, Pune!"

letters = digits = spaces = others = 0
for ch in sample:
    if ch.isalpha():
        letters += 1
    elif ch.isdigit():
        digits += 1
    elif ch.isspace():
        spaces += 1
    else:
        others += 1

print(f"letters={letters} digits={digits} spaces={spaces} others={others}")

def is_palindrome(text):
    cleaned = ""
    for ch in text:
        if ch.isalnum():
            cleaned += ch.lower()
    return cleaned == cleaned[::-1]

for phrase in ["Madam", "A man, a plan, a canal: Panama", "Data Engineer", "12321"]:
    print(f"{phrase!r:<35} {is_palindrome(phrase)}")

sentence = "load clean validate publish"

words = sentence.split()
print(" ".join(reversed(words)))                  # reverse the word order
print(" ".join(w[::-1] for w in words))           # reverse each word

def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())

print(is_anagram("Listen", "Silent"))
print(is_anagram("Order", "Rodeo"))
print(is_anagram("Data", "Dart"))

def caesar(text, shift):
    result = []
    for ch in text:
        if ch.isupper():
            position = ord(ch) - ord("A")
            result.append(chr((position + shift) % 26 + ord("A")))
        elif ch.islower():
            position = ord(ch) - ord("a")
            result.append(chr((position + shift) % 26 + ord("a")))
        else:
            result.append(ch)              # digits, spaces, punctuation stay unchanged
    return "".join(result)

secret = caesar("Order XYZ-1042 ships to Pune", 3)
print(secret)
print(caesar(secret, -3))                  # shifting back decodes it

def clean_id(raw):
    kept = [ch for ch in raw if ch.isalnum()]
    return "".join(kept).upper()

for raw in [" ab-1042 ", "AB 1042", "ab_1042!", "ab1042"]:
    print(f"{raw!r:<14} -> {clean_id(raw)}")

def clean_phone(raw):
    digits = ""
    for ch in raw:
        if ch.isdigit():
            digits += ch
    return digits

print(clean_phone("+91 (98765) 43210"))
print(clean_phone("98765-43210"))

def validate_email(raw):
    email = raw.strip().lower()
    if email.count("@") != 1:
        return None, "needs exactly one @"
    local, domain = email.split("@")
    if not local:
        return None, "nothing before @"
    if "." not in domain:
        return None, "domain has no dot"
    if domain.startswith(".") or domain.endswith("."):
        return None, "domain starts or ends with a dot"
    if " " in email:
        return None, "contains a space"
    return email, "ok"

for raw in ["  Meera.Iyer@XYZ.com ", "rahul@@xyz.com", "@xyz.com", "anika@xyz", "ok user@xyz.com"]:
    cleaned, reason = validate_email(raw)
    print(f"{raw!r:<26} {cleaned!s:<20} {reason}")

def mask_card(number):
    digits = "".join(ch for ch in number if ch.isdigit())
    return "*" * (len(digits) - 4) + digits[-4:]

print(mask_card("4111 1111 1111 1234"))

raw_rows = [
    "  ab-1042 , Meera Iyer , MEERA.IYER@XYZ.COM ",
    "cd 2210,rahul sharma,rahul@@xyz.com",
    "EF_3301 ,  anika  gupta , anika.gupta@xyz.com",
]

clean, rejected = [], []
for row in raw_rows:
    cid, name, email = [part.strip() for part in row.split(",")]
    cid = "".join(ch for ch in cid if ch.isalnum()).upper()
    name = " ".join(name.split()).title()
    valid_email, reason = validate_email(email)
    if valid_email:
        clean.append((cid, name, valid_email))
    else:
        rejected.append((cid, name, reason))

print("clean:")
for r in clean:
    print("  ", r)
print("rejected:")
for r in rejected:
    print("  ", r)
