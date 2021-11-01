import socket,time,threading,math,hashlib
class Craker():
	def __init__(self,ip='10.30.58.40',port=13370):
		self.port = port
		self.ip = ip
		
		soc = socket.socket()
		soc.connect(ip,port)
		soc.send("howdy".encode())
		self.ans = soc.recv(1024).decode()
		self.id=int(self.ans)
		soc.close()

		self.port += self.id
		server_soc = socket.socket()
		server_soc.bind(self.ip,self.port)
		server_soc.lisen(1)
		self.client_soc,adrr = server_soc.accept()

		self.ans = self.client_soc.recv(1024).decode().split(",")
		self.md5 = self.ans[-1]
		self.groups=[]#(start,end)
		self.found = False
		self.thread(self.division_to_groups(self.ans[0],self.ans[1]))
		

	def compare(self,num_range):
		string = num_range[0]

		start_num=base26LetterToBase10(string)
		end_num=base26LetterToBase10(num_range[-1])

		while start_num <= end_num and not found:
			if hashlib.md5(string.encode('utf-8')).hexdigest() == self.md5:
				self.found = True
				self.find_md5(string)

			string = base10ToBase26Letter(base26LetterToBase10(string)+1)
			
		

	def thread(self,num_of_threads):
		threads = []
		for i in range(num_of_threads):
			t = threading.Thread(target=compare,arg=(self.groups[i],))
			threads.append(t)
		for t in threads:
			t.start()
		for t in threads:
			t.join()

		if not self.found:
			not_find_md5()

	def division_to_groups(start,end):
		start_num=base26LetterToBase10(start)
		end_num=base26LetterToBase10(end)

		all_option=end_num-start_num
		num_of_threads=int(math.sqrt(all_option))
		if num_of_threads**2!=all_option:
			num_of_threads+=1

		option_per_thread=all_option//num_of_threads
		
		for i in range(num_of_threads):
			self.groups.append((start_num,start_num+option_per_thread-1))
			start_num+=option_per_thread

		return num_of_threads
	
	def find_md5(self,passowrd):
		self.client_soc.send(f"{self.id},true,{self.md5},{passowrd}".encode())

	def not_find_md5(self):
		self.client_soc.send(f"{self.id},false,{self.md5}".encode())

	def did_someone_find(self):
		ans=self.client_soc.recv(1024).decode().split(",")
		if ans[0]=="finish":
			if ans[1] == self.md5:
				self.found=True
		else:
			pass


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
        return base10ToBase26Letter(int((num-1)/26))+chr(97+(num-1)%26)

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
	#print(hashlib.md5("########################".encode('utf-8')).hexdigest())
	num_of_threads = 10
	option_per_thread = 20
	start_num = 100
	groups=[]
	for i in range(num_of_threads):
		groups.append((start_num,start_num+option_per_thread-1))
		start_num+=option_per_thread

	print(groups)
if __name__ == "__main__":
	main()