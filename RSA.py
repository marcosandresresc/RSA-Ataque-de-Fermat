import random
import time

################################ Funciones matemáticas ################################

def exponenciacion_modular(a, b, n):
    """
    Calcula a^b mod n usando exponenciación binaria.

    Idea:
    b se escribe en binario.
    Se usan identidades:
      a^(2k) = (a^k)^2
      a^(2k+1) = a * (a^k)^2
      a*b mod n = ((a mod n)*(b mod n)) mod n

    """
    resultado = 1
    a = a % n

    while b > 0:
        if b & 1:  # si el bit menos significativo es 1
            resultado = (resultado * a) % n
        a = (a * a) % n
        b >>= 1

    return resultado

def descomponer_potencia_dos(n):
    """
    Escribe n - 1 como: n - 1 = d * 2^s
    con d impar.
    """
    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    return s, d

def mcd_extendido(a, b):
    """
    Algoritmo de Euclides extendido.

    Devuelve:
    m = mcd(a, b)
    x, y tales que: m = ax + by
    """
    if a == 0:
        return b, 0, 1

    g, x1, y1 = mcd_extendido(b % a, a)
    return g, y1 - (b // a) * x1, x1

def inverso_modular(a, m):
    """
    Calcula x tal que:
        a*x ≡ 1 (mod m)

    Solo existe si mcd(a, m) = 1
    """
    g, x, _ = mcd_extendido(a, m)
    if g != 1:
        raise Exception("No existe inverso modular")
    return x % m

def raiz_entera(n):
    """
    Calcula ⌊√n⌋ usando el método de Newton con aritmética entera.
    """
    if n < 0:
        raise ValueError("No se puede calcular la raíz de un número negativo.")
    if n == 0:
        return 0
    
    x = 2**(n.bit_length() // 2 + 1)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


################################ Test de Primalidad ################################


def ronda_miller_rabin(n, a):
    """
    Aplica una ronda del test de Miller-Rabin con base 'a'.

    Se basa en propiedades de:
    a^(n-1) ≡ 1 (mod n) si n es primo.
    """
    s, d = descomponer_potencia_dos(n)
    x = exponenciacion_modular(a, d, n)

    if x == 1 or x == n - 1:
        return True

    for _ in range(0, s - 1, 1):
        x = (x * x) % n
        if x == n - 1:
            return True

    return False

def es_primo_probable(n, rondas=40):
    """
    Aplica el test de Miller-Rabin.

    Con 40 rondas el error es < 2⁻⁸⁰ (nivel criptográfico)
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for i in range(0, rondas, 1):
        a = random.randrange(2, n - 1)
        if not ronda_miller_rabin(n, a):
            return False

    return True

def generar_impar_aleatorio(bits):
    """
    Genera un entero impar con exactamente 'bits' bits.

    - Se fuerza el bit más alto para que tenga el tamaño correcto.
    - Se fuerza el bit menos significativo para que sea impar.
    """
    n = random.getrandbits(bits)
    n |= (1 << (bits - 1))
    n |= 1
    return n

def generar_primo(bits):
    """
    Genera un primo probable de 'bits' bits.

    Repite:
    - generar impar aleatorio
    - test Miller-Rabin
    """
    while True:
        n = generar_impar_aleatorio(bits)
        if es_primo_probable(n):
            return n

################################ RSA ################################

def generar_claves_rsa(bits=1024):
    """
    - Elige primos p, q
    - n = p*q
    - φ(n) = (p-1)(q-1)
    - e coprimo con φ(n)
    - d = e⁻¹ mod φ(n)
    """
    p = generar_primo(bits)
    q = generar_primo(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = inverso_modular(e, phi)

    return (n, e), (n, d)

def cifrar_rsa(mensaje, clave_publica):
    n, e = clave_publica
    return exponenciacion_modular(mensaje, e, n)

def descifrar_rsa(cifrado, clave_privada):
    n, d = clave_privada
    return exponenciacion_modular(cifrado, d, n)

################################ Ataque de Fermat ################################

def ataque_de_fermat(n, K=10000000):
    """
    Todo número impar n = p*q puede escribirse como:
        n = x² - y² = (x - y)(x + y)

    donde:
        x = (p + q)/2
        y = (q - p)/2

    Si p y q son primos muy cercanos entre sí, entonces x ≈ √n.

    El ataque consiste en:
    - comenzar con x = ⌈√n⌉
    - incrementar x hasta que x² - n sea un cuadrado perfecto
    - recuperar p = x - y, q = x + y

    Vulnerabilidad:
    Funciona solo si |p - q| es pequeño.

    En RSA seguro:
    p y q se eligen aleatoriamente y están muy separados,
    haciendo este ataque computacionalmente inviable.
    """
    x = raiz_entera(n)
    if x * x < n:
        x += 1

    for _ in range(0,K,1):
        y2 = x*x - n
        y = raiz_entera(y2)
        if y*y == y2:
            return (x - y), (x + y)
        x += 1

    return None

################################ Demo RSA ################################

def texto_a_entero(texto):
    data = texto.encode("utf-8")
    return int.from_bytes(data, "big")

def entero_a_texto(entero):
    data = entero.to_bytes((entero.bit_length() + 7) // 8, "big")
    return data.decode("utf-8")

def demo_rsa():
    print("\n=== DEMO RSA ===")

    publica, privada = generar_claves_rsa(1024)

    mensaje = "Este es un mensaje secreto."
    msj = texto_a_entero(mensaje)
    print("Mensaje original: ", mensaje)

    cifrado = cifrar_rsa(msj, publica)
    print("Mensaje cifrado: ", cifrado)

    descifrado = descifrar_rsa(cifrado, privada)
    msj_descifrado = entero_a_texto(descifrado)
    print("Mensaje descifrado: ", msj_descifrado)

################################ Demo Ataques ################################

def mostrar_mensaje_interceptado(cifrado):
    print("Mensaje interceptado (cifrado):")
    print(cifrado)

def romper_rsa(cifrado, clave_publica, K=10000000):
    n, e = clave_publica

    inicio = time.time()
    factores = ataque_de_fermat(n, K)
    fin = time.time()

    if factores is None:
        return None, (fin - inicio)

    p, q = factores
    phi = (p - 1) * (q - 1)
    d = inverso_modular(e, phi)

    mensaje_int = descifrar_rsa(cifrado, (n, d))
    return mensaje_int, (fin - inicio)

def demo_intercepcion_fallida():
    print("\n=== DEMO INTERCEPCIÓN (ATAQUE FALLIDO) ===")

    publica, _ = generar_claves_rsa(512)

    mensaje = "Este es un mensaje secreto."
    cifrado = cifrar_rsa(texto_a_entero(mensaje), publica)

    mostrar_mensaje_interceptado(cifrado)

    print("Intentando factorizar n...")
    mensaje_roto, tiempo = romper_rsa(cifrado, publica, K=1000000)

    if mensaje_roto is None:
        print("No se pudo factorizar n.")
    else:
        print("Mensaje recuperado:", entero_a_texto(mensaje_roto))

    print(f"Tiempo transcurrido: {tiempo:.2f} segundos")

def demo_intercepcion_exitosa():
    print("\n=== DEMO INTERCEPCIÓN (RSA MAL GENERADO) ===")

    p = generar_primo(1024)
    q = p + 2
    while not es_primo_probable(q):
        q += 2 
    n = p * q
    e = 65537

    mensaje = "Este es un mensaje secreto."
    msj = texto_a_entero(mensaje)

    cifrado = cifrar_rsa(msj, (n, e))
    mostrar_mensaje_interceptado(cifrado)

    mensaje_roto, _ = romper_rsa(cifrado, (n, e))
    print("Mensaje recuperado por el atacante:")
    print(entero_a_texto(mensaje_roto))


demo_rsa()
demo_intercepcion_fallida()
demo_intercepcion_exitosa()