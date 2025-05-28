def to_binary_from_dec(num :int ,bits : int) -> str:
    return format(num, f'0{bits}b')


def mashlim_le_shtaim(bin_str:str) -> int:
    num_bits = len(bin_str)
    n = int(bin_str, 2)  
    flipped = ~n & ((1 << num_bits) - 1) #זה בעצם הגודל המקסימלי של ביטים (255 במקרה זה ) והפעולה עושה נוט למספר 42 ועושה אנד ל 255 
    result = flipped + 1
    return format(result, f'0{num_bits}b')

    
print(mashlim_le_shtaim(to_binary_from_dec(42,8)))