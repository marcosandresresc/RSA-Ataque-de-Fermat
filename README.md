Implementación de cero del cifrado RSA desde sus bases matemáticas en Python, incluyendo una demostración práctica de la vulnerabilidad ante el Ataque de Factorización de Fermat.

El propósito de este proyecto es demostrar la mecánica interna de los sistemas de clave pública y la importancia crítica de la aleatoriedad en la generación de primos. El código evita el uso de librerías criptográficas de alto nivel para exponer la lógica de la aritmética modular y los tests de primalidad.

**Características Principales**

- Generación de Claves: Implementación completa del ciclo de vida de RSA (generación de primos, cálculo de $\phi(n)$, e inverso modular).
- Aritmética Modular Eficiente: Uso de exponenciación binaria modular para cifrado y descifrado rápido.
- Test de Primalidad de Miller-Rabin: Un algoritmo probabilístico robusto para garantizar la generación de primos de gran tamaño con un margen de error insignificante ($< 2^{-80}$).
- Ataque de Fermat: Implementación de un ataque de factorización para demostrar cómo el uso de primos cercanos (p y q) compromete totalmente la seguridad de la clave privada.

**Detalles Técnicos**

El proyecto incluye las siguientes implementaciones desde cero:
- Algoritmo de Euclides Extendido: Para hallar el inverso modular necesario en la clave privada.
- Exponenciación Binaria: Optimización de la operación $a^b \pmod n$ para manejar números de miles de bits.
- Conversión de Datos: Manejo de codificación UTF-8 para transformar cadenas de texto en enteros procesables matemáticamente.
- Método de Newton: Raíz cuadrada entera para el análisis de factorización.

**Análisis de Vulnerabilidades**

El script incluye dos escenarios de demostración:
- RSA Seguro (1024/2048 bits): Muestra cómo una separación aleatoria y suficiente entre $p$ y $q$ hace que la factorización sea computacionalmente inviable.
- RSA Inseguro (Ataque de Fermat): Demuestra que si la diferencia $|p - q|$ es pequeña, un atacante puede recuperar la clave privada en fracciones de segundo, sin importar la longitud de la clave.


***Especificaciones de Seguridad***

Este software ha sido desarrollado como una prueba de concepto en implementación de algoritmos criptográficos y teoría de números.
Aunque la lógica matemática es precisa y funcional para cifrar y descifrar mensajes, esta implementación no está destinada a entornos de producción por los siguientes criterios de seguridad industrial:
- Ausencia de Padding: Se implementa "Textbook RSA", el cual carece de esquemas como OAEP (Optimal Asymmetric Encryption Padding). En un entorno real, el padding es indispensable para evitar ataques de maleabilidad y garantizar la seguridad semántica.
- Generación de Entropía: El sistema utiliza el generador de números aleatorios estándar de Python para la selección de primos. Para aplicaciones críticas, se requeriría un generador de números aleatorios criptográficamente seguro (CSPRNG) conforme a normativas de seguridad.
- Resistencia a Canales Laterales: Esta implementación prioriza la claridad algorítmica y no incluye mitigaciones contra timing attacks que analicen los tiempos de ejecución de la exponenciación modular.
