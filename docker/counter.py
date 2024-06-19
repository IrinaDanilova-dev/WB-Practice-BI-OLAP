import time


def main(qty):
    pfile_name = './counter-data/data.txt'
    file = open(pfile_name, "w")

    for i in range(qty):
        print(i)
        file.write(f"iter {i} ")
        time.sleep(1)
    file.close()
        
main(15)
        
