import sys
from . import convert_binary as conv_bin

async def getBinRemainder(n, maxDepth):
    rem = str(int((n*2)-(n*2)%1))
    if not n*2 == 0.0 :
        rem += await getBinRemainder((n*2)%1, maxDepth-1)
    return rem



async def getSign(n):
    
    sign = "1" if n<0 else "0"
    num = n if n>=0 else -n

    return (sign, num)

async def getFloat(sign, integer, fraction, double=False):
    # are we working with 32-bit or 64-bit?
    expLen = 8 if not double else 11
    lenMant = 23 if not double else 52
    

    # calc exponent
    offset, bias = len(integer)-1, 2**(expLen-1)-1
    exp = await conv_bin.conv_Bin(bias+offset if not(integer=="0" and integer=="10" and integer == "1") else bias-offset).rjust(expLen, "0")
    print(bias)

    # calc mantisse & pad 
    mantisse = (integer[1:len(integer)] + fraction).ljust(lenMant,"0")[0:lenMant]

    return (sign, exp, mantisse) 
    
async def run(num:float):
    sign, pos = getSign(num)
    fraction = getBinRemainder(pos%1, 30)
    integer = conv_bin.conv_Bin(int(pos - (pos%1)))
    float32 = getFloat(sign, integer, fraction)
    float64 = getFloat(sign, integer, fraction, double=True)

    result = {
        "float32": float32,
        "float64": float64,
    }
    return result

