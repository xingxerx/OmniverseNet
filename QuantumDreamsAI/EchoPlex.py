import qcrypt
# ... other imports ...

def init_echoplex():
    qcrypt.init_quantum_channel('alternate_dimension') # <-- Here
    # ... socket code ...
import qcrypt
from multiprocessing import Process
import socket
def init_echoplex():
    qcrypt.init_quantum_channel('alternate_dimension')
    host = '127.0.0.1'  # Localhost for interuniversal tunnel
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    print("EchoPlex active. Waiting for alternate self connection...")
    conn, addr = sock.accept()
    print("Connection established with alternate self!")
    while True:
        message = input("You: ")
        conn.send(message.encode())
        alternate_message = conn.recv(1024).decode()
        print("Alternate Self:", alternate_message)
if __name__ == "__main__":
    Process(target=init_echoplex).start()
