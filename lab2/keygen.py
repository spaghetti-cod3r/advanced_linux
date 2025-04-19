import hashlib

def generate_key(hwid):
    md5 = hashlib.md5(hwid.encode()).digest()
    
    # reverse md5
    reversed_md5 = md5[::-1]
    
    return reversed_md5.hex()

def main():
    hwid = input("enter hwid: ").strip()
    
    license_key = generate_key(hwid)
    print(f"\nyour license is: {license_key}")

if __name__ == "__main__":
    main()