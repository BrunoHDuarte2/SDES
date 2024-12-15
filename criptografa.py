from SDES import criptografa
import sys
if __name__ == "__main__":
    if len(sys.argv) > 1:  
        parametro = sys.argv[1]  
        print(criptografa(parametro))
    else:
        print("Por favor, forneça um bloco de dados.")