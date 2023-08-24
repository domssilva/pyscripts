ip_address:str = '192.168.1.18'
# expected output 192[.]168[.]1[.]18

def defang(address:str):
    result: str = ''
    # iterate over every character in the string
    for ch in address:
        # replace with [.] if its a dot
        if ch == '.':
            result += '[.]'
        # otherwise, keep character as is
        else:
            result += ch
    return result


print(f'Original address = {ip_address}\nDefanged address = {defang(ip_address)}')
