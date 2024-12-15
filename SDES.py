# OBS: Os shifs circulares poderiam ser utilizados os implementados pelo numpy, aqui foi adotado a implementação bruta e feita na mão.
def P10(key: str):
    """
        Pega a Chave inputada e permuta de forma que a key denotada por (k1, k2, k3, ..., k10) é transformada em (k3, k5, k2, k7, k4, k10, k1, k9, k8, k6)
    """
    return key[2] + key[4] + key[1] + key[6] + key[3] + key[9] + key[0] + key[8] + key[7] + key[5]
def LS1(stringP10):
    """
        Shift a esquerda nas duas metades do resultado de P10, SHIFT CIRCULAR ou seja o bit em [0] vai para o bit em [n], sendo n o tamanho máximo da substring
    """
    left =  stringP10[0:5]
    right = stringP10[5:]
    strLeft1bitShift = left[1] + left[2] + left[3] + left[4] + left[0]
    strRight1bitShift = right[1] + right[2] + right[3] + right[4] + right[0] 
    strLeft2bitShift =  strLeft1bitShift[2] + strLeft1bitShift[3] + strLeft1bitShift[4] + strLeft1bitShift[0] + strLeft1bitShift[1]
    strRight2bitShift = strRight1bitShift[2] + strRight1bitShift[3] + strRight1bitShift[4] + strRight1bitShift[0] + strRight1bitShift[1]
    return (strLeft1bitShift + strRight1bitShift, strLeft2bitShift+strRight2bitShift)
def P8(key):
    """
        Assim como P10, faz uma permutação do resultado,
        nesse caso é mapeada da seguinte forma:
        (k1, k2, k3, ..., k10) -> (k6, k3, k7, k4, k8, k5, k10, k9)
    """
    return key[5] + key[2] + key[6] + key[3] + key[7] + key[4] + key[9] + key[8] 

def genKey(key):
    umShift, doisShift = LS1(P10(key))
    k1 = P8(umShift)
    k2 = P8(doisShift)
    return k1, k2

def ip(plaintext):
    """
    Permutação inicial definida como:
    (k1, k2, k3, ..., k8) -> (k2, k6, k3, k1, k4, k8, k5, k7)
    """
    return plaintext[1] + plaintext[5] + plaintext[2] + plaintext[0] + plaintext[3] + plaintext[7] + plaintext[4] + plaintext[6] 
def ipInversa(plaintext):
    """
    Permutação final definida como:
    (k1, k2, k3, ..., k8) -> (k4, k1, k3, k5, k7, k2, k8, k6)
    """
    return plaintext[3] + plaintext[0] + plaintext[2] + plaintext[4] + plaintext[6] + plaintext[1] + plaintext[7] + plaintext[5] 
def fk(L, R, key):
    """
        fK(L, R) = (L XOR F(R, SK), R)
        O que isso significa?
    """
    k1, k2, k3, k4 = F(R, key)
    return str(int(L[0])^int(k1)) + str(int(L[1])^int(k2)) + str(int(L[2])^int(k3)) + str(int(L[3])^int(k4)) + R
def F(quatroBits, key):
    """
    Descrito como uma Operação de Expansão/Permutação
    No qual é descrita da seguinte forma:
    (n1, n2, n3, n4) -> (n4, n1, n2, n3, n2, n3, n4, n1)
    e depois combinado com a K1 =  (k11, k12, k13, k14, k15, k16, k17, k18)
    da forma: (n4 XOR k11, n1 XOR k12, n2 XOR k13, n3 XOR k14, n2 XOR k15, n3 XOR k16, n4 XOR k17, n1 XOR k18)
    Os primeiros 4 bits vão para SBox S0 e produz 2 bits de saída da mesma forma o lado direito
    Após isso se aplica P4.
    """
    
    exp = str(int(quatroBits[3])^int(key[0])) + str(int(quatroBits[0])^int(key[1])) + str(int(quatroBits[1])^int(key[2])) + str(int(quatroBits[2])^int(key[3])) + str(int(quatroBits[1])^int(key[4])) + str(int(quatroBits[2])^int(key[5])) + str(int(quatroBits[3])^int(key[6])) + str(int(quatroBits[0])^int(key[7]))
    return P4(SBox0(exp[0], exp[1], exp[2], exp[3]), SBox1(exp[4], exp[5], exp[6], exp[7]))
    
def SBox0(bit1, bit2, bit3, bit4):
    """
    Bit1 e bit4 especificam a linha
    Bit2 e bit3 especificam a coluna 
        [ 1 0 3 2 ]
        [ 3 2 1 0 ]
        [ 0 2 1 3 ] 
        [ 3 1 3 2 ]
    """
    M = [[ 1, 0, 3, 2 ],
        [ 3, 2, 1, 0 ],
        [ 0, 2, 1, 3 ],
        [ 3, 1, 3, 2 ]]
    res = str(bin(M[int(bit1+bit4, 2)][int(bit2+bit3, 2)]))[2:]

    if len(res) != 2:
        res = f'0{res}'
    return res

def SBox1(bit1, bit2, bit3, bit4):
    """
    Bit1 e bit4 especificam a linha
    Bit2 e bit3 especificam a coluna 
        [ 0 1 2 3 ]
        [ 2 0 1 3 ]
        [ 3 0 1 0 ] 
        [ 2 1 0 3 ]
    """
    M = [[ 0, 1, 2, 3 ],
        [ 2, 0, 1, 3 ],
        [ 3, 0, 1, 0 ], 
        [ 2, 1, 0, 3 ]]
    
    res = str(bin(M[int(bit1+bit4,2)][int(bit2+bit3,2)]))[2:]
    if len(res) < 2:
        res = f'0{res}'
    return res
def P4 (S0, S1):
    """
    Pega os resultados de SBOX 0 e 1 e retorna 
    SBOX 0 = (1, 2), SBOX 0 = (3, 4) -> (2, 4, 3, 1)
    Seu resultado é a F.
    """
    return S0[1], S1[1], S1[0], S0[0] 

def criptografa(plaintext):
    k1, k2 = genKey("1010000010")
    ipText = ip(plaintext)
    string8bits = fk(ipText[:4], ipText[4:], k1)
    ipText = string8bits[4:] + string8bits[:4]
    resultadoInvetido = fk(ipText[:4], ipText[4:], k2)
    return ipInversa(resultadoInvetido)


def descriptografa(plaintext):
    k1, k2 = genKey("1010000010")
    ipText = ip(plaintext)
    string8bits = fk(ipText[:4], ipText[4:], k2)
    ipText = string8bits[4:] + string8bits[:4]
    resultadoInvetido = fk(ipText[:4], ipText[4:], k1)
    return ipInversa(resultadoInvetido)

