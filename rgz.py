import random
from lab1 import *

def read_graph(file_name):
    G = {}
    while True:
        try:
            with open(file_name, 'r') as file:
                n, m = map(int, file.readline().split())
                for i in range(1, n + 1):
                    line = file.readline().strip()
                    parts = line.split(':')
                    if len(parts) == 2:
                        node = int(parts[0])
                        neighbors = [int(neighbor) for neighbor in parts[1].split(',')]
                        G[node] = neighbors
                    else:
                        print("Ошибка в формате файла.")
                        return None
        except FileNotFoundError:
            print("Файл не найден.")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        return G

def get_user_choice():
    while True:
        user_choice = input("\nВыберите вопрос: (1 - Докажите изоморфность, 2 - Покажите гамильтонов цикл) ")
        if user_choice in ["1", "2"]:
            return user_choice
        else:
            print("Пожалуйста, выберите 1 или 2.")

file_name = "graph.txt"
G = read_graph(file_name)

if G is None:
    exit()

graph_data = G
gamilton_cycle = [1, 4, 5, 2, 3, 6]

G = dict()
for node, neighbors in graph_data.items():
    G[node] = neighbors

H = dict()
vertex_mapping = dict()
old_nodes = list(G.keys())
new_nodes = random.sample(old_nodes, len(old_nodes))

for old_node, new_node in zip(old_nodes, new_nodes):
    H[new_node] = list()
    vertex_mapping[old_node] = new_node

for node, neighbors in G.items():
    for neighbor in neighbors:
        H[vertex_mapping[node]].append(vertex_mapping[neighbor])

print("Исходный граф из файла:")
for node, neighbors in G.items():
    print(f"{node}: {', '.join(map(str, neighbors))}")

output_file_name = "isomorphic_graph.txt"
with open(output_file_name, 'w') as output_file:
    for node, neighbors in sorted(H.items()):
        output_file.write(f"{node}:{','.join(map(str, sorted(neighbors)))}\n")

print(f"\nИзоморфный граф был записан в файл: {output_file_name}")


print("\nИзоморфный граф из файла:")
for node, neighbors in sorted(H.items()): 
    print(f"{node}: {', '.join(map(str, sorted(neighbors)))}")

keys = {}

def generate_coprime(p):
    result = random.randint(2, p)

    while gcd(p, result) != 1:
        result = random.randint(2, p)

    return result

def RSA_encode(m) -> list:
    result = list()
    print("\nСгенерированные ключи для RSA-шифрования:")
    P = generate_prime(0, 10 ** 9)
    print("P = ", P)
    Q = generate_prime(0, 10 ** 9)
    print("Q = ", Q)

    N = P * Q
    print("N = ", N)
    Phi = (P - 1) * (Q - 1)
    print("Phi = ", Phi)

    d = generate_coprime(Phi)
    print("d = ", d)

    c = gcd_modified(d, Phi)[1]
    if c < 0:
        c += Phi
    print("c = ", c)

    keys['RSA'] = {'c': c, 'N': N} 
    for part in m:
        e = pow_module(part, d, N)
        result.append(e)
      
    return result

def RSA_decode(e) -> list:
    result = list()
    c = keys["RSA"]["c"]
    N = keys["RSA"]["N"]
    for part in e:
        m1 = pow_module(part, c, N)
        result.append(m1)
    print("m1 = ", m1)
    return result

def read_file(filename: str, ext: str) -> bytearray:
    with open(filename + '.' + ext, 'rb') as origin_file:
        return bytearray(origin_file.read())

filename = 'isomorphic_graph'
filename2 = 'isomorphic_graph2'
ext = 'txt'
m = read_file(filename, ext)
print(m)

RSA_enc = RSA_encode(m)
print(f"\nШифрование содержимого файла {filename} и запись зашифрованных данных в файл {filename2}")
print("\nЗашифрованные данные:")
print(RSA_enc)
with open('isomorphic_graph2.txt', 'wt') as magic_e:
    magic_e.write(str(RSA_enc))

filename3 = 'isomorphic_graph3'
print(f"\nДешифрование данных из файла {filename2} и запись их в файл {filename3}")
RSA_dec = RSA_decode(RSA_enc)
for node, neighbors in sorted(H.items()):
    print(f"{node}: {', '.join(map(str, sorted(neighbors)))}")
print(bytearray(RSA_dec))
with open('isomorphic_graph3.txt', 'wb') as magic_d:
    magic_d.write(bytearray(RSA_dec))

reverse_vertex_mapping = {v: k for k, v in vertex_mapping.items()}
H_reverse = dict()

for node, neighbors in H.items():
    H_reverse[reverse_vertex_mapping[node]] = [reverse_vertex_mapping[n] for n in neighbors]

user_choice = get_user_choice()

if user_choice == "1":
    print("\nРасшифрованный изоморфный граф:")
    with open('isomorphic_graph3.txt', 'r') as decrypted_file:
        decrypted_content = decrypted_file.read()
        print(decrypted_content)

    print("\nИзоморфный граф с обратной перестановкой:")
    for node, neighbors in H_reverse.items():
        print(f"{node}: {', '.join(map(str, neighbors))}")
  
    isomorphic = G == H_reverse

    if isomorphic:
        print("\nГрафы изоморфны.")
    else:
        print("\nГрафы не изоморфны.")
elif user_choice == "2":
    original_hamilton_cycle = [1, 4, 5, 2, 3, 6]
    shuffled_hamilton_cycle = [vertex_mapping[node] for node in original_hamilton_cycle]

    print("\nГамильтонов цикл в изоморфном графе:")
    print(" -> ".join(map(str, shuffled_hamilton_cycle)))
