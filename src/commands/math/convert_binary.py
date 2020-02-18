import sys

async def conv_Bin(n:int, pad:bool):
    def convert(n:int):
        res = ""

        if(n//2 != 0):
            res += str(n%2) + convert(n//2)
        else:
            res += str(n%2)
        return res

    result = convert(n)[::-1]

    if pad:
        pad = (len(result)//8 + 1)*8 if len(result)%8 != 0 else (len(result)//8 + 1)
        
        binary = result.rjust(pad, "0")
        res = ""
        for i in range(len(binary)//8):
            res += f' {binary[ i*8 : (i+1)*8 ]}'
        
        return res[1:len(res)]
    else:
        return result
    

async def conv_Dec(n:str):
    num = n
    res = 0
    for index, num in enumerate(num[::-1]):
        res += int(num) * (2**int(index))
    return res