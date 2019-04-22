import sys
import os
import shutil
import xlwt

res = ([],[],[],[])  # same, file1_have, file2_have, diff

def set_only_have(path,k):
    for f in os.listdir(os.path.join('file%d'%k,path)):
        print('onle %s file have:'%['first','second'][k-1],os.path.join(path,f))
        if os.path.isdir(os.path.join('file%d'%k,path,f)):
            
            res[k].append(os.path.join(path,f))
            set_only_have(os.path.join(path,f),k)
        else:
            res[k].append(os.path.join(path,f))


def search(path):
    next_path = set()
    file1_dir_res = os.listdir(os.path.join('file1',path))
    file2_dir_res = os.listdir(os.path.join('file2',path))
    if path =='':
        print('comparing','"."')
    else:
        print('comparing:','"'+path+'"')
    current_path_same = True
    for f1 in file1_dir_res:
        if os.path.isdir(os.path.join('file1',path,f1)):
            if f1 not in file2_dir_res:
                set_only_have(os.path.join(path,f1),1)
                res[1].append(os.path.join(path,f1))
                current_path_same=False
                continue
            next_path.add(os.path.join(path,f1))
            continue
        if f1 in file2_dir_res:
            res[0].append(path+f1)
        else:
            current_path_same=False
            res[1].append(os.path.join(path,f1))
    for f2 in file2_dir_res:
        if os.path.isdir(os.path.join('file2',path,f2)):
            if f2 not in file1_dir_res:
                res[2].append(os.path.join(path,f2))
                set_only_have(os.path.join(path,f2),2)
                current_path_same=False
                continue
            next_path.add(os.path.join(path,f2))
            continue
        if f2 not in file1_dir_res:
            current_path_same=False
            res[2].append(os.path.join(path,f2))
    for next_p in next_path:
        if not search(next_p):
            res[3].append(next_p)
            current_path_same=False
    return current_path_same
    

def write_to_excel(file_path = 'res.xls'):
    file_path = os.path.join('..',file_path)
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True)
    row0 = ["文件1","文件2","状态"]
    row_count = 0
    for i in range(len(row0)):
        sheet1.write(0,i,row0[i])
    i = 0
    for j in range(len(res[i])):
        sheet1.write(row_count+1,i,os.path.abspath(os.path.join('file1',res[i][j])))
        sheet1.write(row_count+1,i+1,os.path.abspath(os.path.join('file2',res[i][j])))
        sheet1.write(row_count+1,i+2,'SAME')
        row_count+=1

    i=3
    for j in range(len(res[i])):
        sheet1.write(row_count+1,0,os.path.abspath(os.path.join('file1',res[i][j])))
        sheet1.write(row_count+1,1,os.path.abspath(os.path.join('file2',res[i][j])))
        sheet1.write(row_count+1,2,'DIFF')
        row_count+=1

    for i in [1,2]:
        for j in range(len(res[i])):
            sheet1.write(row_count+1,i-1,os.path.abspath(os.path.join('file%d'%i,res[i][j])))
            sheet1.write(row_count+1,2,'ISOLATED')
            row_count+=1
    f.save(file_path)


def compare(files_path):
    # prepare
    if os.path.exists('./temp'):
        shutil.rmtree('./temp')
    os.mkdir('./temp')
    os.mkdir('./temp/file1')
    os.mkdir('./temp/file2')
    # extract
    for k,file_path in enumerate(files_path):
        print('# using 7z extract:',file_path)
        print('"c:\\Program Files\\7-zip\\7z.exe"'+' x '+'"'+file_path+'"'+' -o temp\\file'+str(k+1))
        state = os.system(r'"c:\Program Files\7-zip\7z.exe" x %s -otemp\file%d' % (file_path,k+1))
    
    print('\n##############################################\n')
    print('Done: extract files to temp directory')

    # compare
    print('Start: comparing')
    os.chdir('./temp')
    search('')
if __name__ == "__main__":
    if len(sys.argv)<3:
        print('\t Usage: python3 compare.py file1_path file2_path [path_to_save_excel]')
    else:
        files_path = sys.argv[1:3]
        compare(files_path)
        if len(sys.argv) == 4:
            write_to_excel(sys.argv[3])
        else:
            write_to_excel()
