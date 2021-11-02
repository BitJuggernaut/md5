import socket
import time
import threading
import math
import hashlib
import flash


class Craker():
    def __init__(self, ip='10.30.58.40', port=13370):
        self.port = port
        self.ip = ip

        soc = socket.socket()
        soc.connect((ip, port))
        soc.send("Howdy".encode())
        self.ans = soc.recv(1024).decode()
        self.id = int(self.ans)
        soc.close()

        self.port += self.id
        server_soc = socket.socket()
        server_soc.bind(("", self.port))
        server_soc.listen(1)
        self.client_soc, adrr = server_soc.accept()
        print("connected")

        self.ans = self.client_soc.recv(1024).decode().split(",")  # [start,end,md5]
        self.md5 = self.ans[-1]
        self.groups = []  # (start,end)
        self.found = False
        self.finish = False
        self.password = ""

    def compare(self, num_range):#ex: (97,122)
        int_password = num_range[0]
        while int_password <= num_range[1] and not self.found and not self.finish:
            if hashlib.md5(base10ToBase26Letter(int_password).encode('utf-8')).hexdigest() == self.md5:
                self.found = True
                self.finish = True
                self.password = base10ToBase26Letter(int_password)
                int_password+=1


    def did_finish(self):
        for t in self.threads:
            t.join()
        self.finish = True

    def thread(self, num_of_threads):
        self.found = False
        self.finish = False
        self.threads = []
        for i in range(num_of_threads):
            t = threading.Thread(target=self.compare, args=(self.groups[i],))
            self.threads.append(t)
        for t in self.threads:
            t.start()
        threading.Thread(target=self.did_finish).start()
        self.did_someone_find()
        if self.finish:
            if self.found:
                self.find_md5(self.password)
            else:
                self.not_find_md5()
                print("not found")

    def find_md5(self, passowrd):
        self.client_soc.send(f"{self.id},true,{self.md5},{passowrd}".encode())


    def not_find_md5(self):
        self.client_soc.send(f"{self.id},false,{self.md5}".encode())


    def did_someone_find(self):
        relevent = False
        while not relevent:
            ans = self.client_soc.recv(1024).decode().split(",")
            if ans[0] == "finish":
                if ans[1] == self.md5:
                    self.found = True
                    self.finish = True
                    relevent = True

                    flash.main()
                else:
                    relevent = False

            else:
                self.found = True
                self.finish = True
                self.md5 = self.ans[-1]
                self.groups = []  # (start,end)
                relevent = True



    def division_to_groups(self, start, end):
        start_num = base26LetterToBase10(start)
        end_num = base26LetterToBase10(end)

        all_option = end_num-start_num
        num_of_threads = int(math.sqrt(all_option))
        if num_of_threads**2 != all_option:
            num_of_threads += 1

        option_per_thread = all_option//num_of_threads

        for i in range(num_of_threads):
            #print((start_num, start_num+option_per_thread-1))
            self.groups.append((start_num, start_num+option_per_thread-1))
            start_num += option_per_thread
        return num_of_threads


def base10ToBase26Letter(num):


    ''' Converts any positive integer to Base26(letters only) with no 0th 
    case. Useful for applications such as spreadsheet columns to determine which 
    Letterset goes with a positive integer.
    '''
    if num <= 0:
        return ""
    elif num <= 26:
        return chr(96+num)
    else:
        return base10ToBase26Letter(int((num-1)/26))+chr(97+(num-1) % 26)


def base26LetterToBase10(string):


    ''' Converts a string from Base26(letters only) with no 0th case to a positive
    integer. Useful for figuring out column numbers from letters so that they can
    be called from a list.
    '''
    string = string.lower()
    if string == " " or len(string) == 0:
        return 0
    if len(string) == 1:
        return ord(string)-96
    else:
        return base26LetterToBase10(string[1:])+(26**(len(string)-1))*(ord(string[0])-96)


def main():
    '''
    #print(hashlib.md5("########################".encode('utf-8')).hexdigest())
    num_of_threads = 10
    option_per_thread = 20
    start_num = 100
    groups=[]
    for i in range(num_of_threads):
        groups.append((start_num,start_num+option_per_thread-1))
        start_num+=option_per_thread

    print(groups)
    '''
    craker = Craker()
    while True:
        craker.thread(craker.division_to_groups(craker.ans[0], craker.ans[1]))


if __name__ == "__main__":
    main()
