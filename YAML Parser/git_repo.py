from git import Repo, exc
import os
import shutil
import re
import yaml,time



# merging documents from yaml file with multiple documents 
# updated versions may use python multi variable search or rabin karp algo
# note to self: check google first for the queries that you have :)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
def document_merge(yaml_path, item):
    
    with open(os.path.join(yaml_path, item),'r',  encoding="utf8") as firstfile, open(os.path.join(yaml_path, 'search.yml'),'w',  encoding="utf8") as secondfile:
      
        for line in firstfile:
             secondfile.write(line.replace("---",""))

# simple query main function
def simple_query(yaml_path):
    start = time.time()
    flag = 0
    print("Enter key to search: ")
    key = input()
    output = []
                 
    for r, d, f in os.walk(yaml_path):
        for item in f:
            fi = open(os.path.join(yaml_path, item), "r", encoding="utf8")
            for line in fi:
                if key in line:
                    flag = 1
                    output.append("(*)"+line+" in "+item)
                    break

    if flag == 1:
        for line in output:
            print(line) 
    else:
        print("No Key Found")
    end = time.time()
    # print(f"Runtime for simple query: {end-start}")


# nested search main function
def nested_query(yaml_path):
    start = time.time()
    flag = 0
    print("Enter key to search: (key should be in dictionary like format)")
    k = input()
        
    ou = []

    for r, d, f in os.walk(yaml_path):
        i = 0
        for item in f:
            ser = "search.yml"
            document_merge(yaml_path, item)
                
            yaml_file = os.path.join(yaml_path, ser)

            with open(yaml_file, 'r', encoding="utf8") as stream:
                try:
                    x  = yaml.load(stream,Loader=yaml.BaseLoader)
                    st = str(x)
                    ot = search(k, str(x), 101, item)
                    if ot is not None:
                        ou.extend(ot)
                except:
                    print("Error occured while loading the file "+item)

                # ddiff = DeepDiff(doc, a, ignore_order=True)


                            
        if len(ou) == 0:
            print("Key Not Found")
        else:
            for line in ou:
                print(line)
    end = time.time()
    # print(f"Runtime for nested query: {end-start}")


# rabin karp algorithm for nested query
def search(pattern, text, q, item):
    d = 256
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1
    i = 0
    j = 0
    op = []

    if m <= n:
        for i in range(m-1):
            h = (h*d) % q

        # Calculate hash value for pattern and text
        for i in range(m):
            p = (d*p + ord(pattern[i])) % q
            t = (d*t + ord(text[i])) % q

        # Find the match
        for i in range(n-m+1):
            if p == t:
                for j in range(m):
                    if text[i+j] != pattern[j]:
                        break

                j += 1
                if j == m:
                    # print("Pattern is found at position: " + str(i+1)+"  in "+item)
                    op.append("(*) Pattern is found at position: " + str(i+1)+"  in "+item)

            if i < n-m:
                t = (d*(t-ord(text[i])*h) + ord(text[i+m])) % q

                if t < 0:
                    t = t+q
        return op    

#function that initiates searching functions
def git(git_url):
    

    parent_dir =  os.getcwd()

    parent_dir = os.path.join(parent_dir, "Clone_Folder")

    if os.path.isdir(parent_dir) == False:
        os.mkdir(parent_dir)

    directory = git_url.replace("https://github.com/", "")
    directory = directory.replace("/", "")

    yaml_dir = directory+"yaml"
    path = os.path.join(parent_dir, directory)

    if os.path.isdir(path)==False:
        os.mkdir(path)

    yaml_path = os.path.join(parent_dir, yaml_dir)

    if os.path.isdir(yaml_path)==False:
        os.mkdir(yaml_path)
        try:
            Repo.clone_from(git_url, path)
        except:
            print("Given url may not correspond to a repository")

        files_in_dir = []

        for r, d, f in os.walk(path):
            for item in f:
                if '.yaml' in item:
                    files_in_dir.append(os.path.join(r, item))
                if '.yml' in item:
                    files_in_dir.append(os.path.join(r, item))
                

        for item in files_in_dir:
            print("File in dir:", item)
            shutil.copy(item, yaml_path)
        

        shutil.rmtree(path, ignore_errors=True)    

        print("(***) For nested key search enter 1 \n(***) For simple key search enter 2")
        option = int(input())
        
        if option == 1:
            nested_query(yaml_path)
        elif option == 2:
            simple_query(yaml_path)
              
    else:
        print("(***) For nested key search enter 1 \n(***) For simple key search enter 2")
        option = int(input())
        
        
        if option == 1:
            nested_query(yaml_path)
        elif option == 2:
            simple_query(yaml_path)
            
#starting point
if __name__ == "__main__":
    check = True
    git_url = ""
    while check:
        if git_url == "":
            print("Enter Github URL: ")
            git_url = input()
        else:
            print("Do you want to continue searching "+git_url+"? 1(yes)/0(no)")
            ch = int(input())
            if ch == 0:
                print("Enter Github URL: ")
                git_url = input()
            else:
                print("Continuing with previous search")

        git(git_url)

        print("Do you want to continue? Yes/No")
        ch = input()
        if ch[0] == "Y" or ch[0]=="y":
            check = True
        else:
            check = False


