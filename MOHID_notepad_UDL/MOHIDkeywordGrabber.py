import os


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def GetF90Files(main_path):
    walker = list(os.walk(main_path))
    f90_files = []

    for i in walker:
        for f in i[2]:
            if f.endswith('.f90') or f.endswith('.F90'):
                f90_files.append((i[0] + '/' + f).replace('\\','/'))

    return f90_files



def GetKeywords(fortran_files_paths):
    keywords = []
    for fortran_file in fortran_files_paths:
        f1 = open(fortran_file, 'r')
        while True:
            l = f1.readline()
            if l == '':
                break
            if l.strip().startswith('!$'):
                l = l.replace('!$','')
            if l.strip().startswith('!'):
                continue
            if l.lower().find('write(*,*)') != -1 or l.lower().find('write (*,*)') != -1:
                continue
            if l.lower().find('call seterror') != -1:
                continue
            l = ' ' + l
            l = l.replace('=', ' = ')
            l = l.replace(',', ' , ')
            if l.lower().find(' keyword ') != -1 and l.lower().rfind('=') > l.lower().rfind(' keyword'):
                if l.find('!'):
                    keyword = l[0:l.find('!')]
                keyword = keyword.strip('(),& ')
                keyword = keyword.replace(' ','').replace('"','').replace("'",'')
                keyword = keyword.split('=')[-1]
                if l.find('%') != -1:
                    continue
                if l.find('trim(') != -1:
                    continue
                keywords.append(keyword)
            if l.lower().find('call readfilenames') != -1:
                continue
            if l.lower().find('call readfilename') != -1:
                keyword = l.replace('call ReadFileName','').replace('\n','').replace(' ','')
                keyword = keyword.strip('()&')
                keyword = keyword.split(',')[0]
                keyword = keyword.replace('KEYWORD=','').replace('Keyword=','').replace('keyword=','')
                keyword = keyword.strip('"\'')
                keywords.append(keyword)

        f1.close()
    return list(dict.fromkeys(keywords))


def GetBlocks(fortran_files_paths):
    blocks = []
    for fortran_file in fortran_files_paths:
        f1 = open(fortran_file, 'r')
        while True:
            l = f1.readline()
            if l == '':
                break
            if l.strip().startswith('!'):
                continue
            if l.lower().find('write(') != -1:
                continue
            if l.find('<') > -1 and l.find('>') != -1:
                #print(l.replace('\n','').strip())
                l = l[l.find('<')-1:l.rfind('>')+1+1]
                if (l.startswith("'") and l.endswith("'")) or (l.startswith('"') and l.endswith('"')):
                    if l.find(',') != -1:
                        ls = l.replace(' ','').split(',')
                        for l in ls:
                            blocks.append(l.replace('"','').replace("'",''))
                    else:
                        blocks.append(l.replace('"','').replace("'",''))

        f1.close()
    return list(dict.fromkeys(blocks))


def getProperties(fortran_files_paths):
    properties = []
    for fortran_file in fortran_files_paths:
        if fortran_file.lower().endswith('globaldata.f90'):
            f1 = open(fortran_file, 'r')
            while True:
                l = f1.readline()
                if l == '':
                    break
                if l.strip().startswith('!'):
                    continue
                if l.strip().lower().startswith('character(stringlength), private, parameter ::'):
                    if l.find('!'):
                        l = l[:l.find('!')]
                    l = l[l.find('=')+1:]
                    if l.find("'") != -1:
                        l = l[l.find("'")+1:l.rfind("'")]
                    if l.find('"') != -1:
                        l = l[l.find('"')+1:l.rfind('"')]
                    if l.find('/') != -1 or l.find('\\') != -1:
                        continue
                    properties.append(l)


            f1.close()
    return list(dict.fromkeys(properties))


def WriteKeywordsToFile(file_path, keywords, n=1, quotations=False):
    keywords_lists = split(keywords, n)
    file_n = 1
    for keywords_list in keywords_lists:
        with open(file_path.replace('.txt', str(file_n)+'.txt'), 'w') as f:
            for keyword in keywords_list:
                if quotations:
                    keyword = '"' + keyword + '"'
                f.write(keyword + ' ')
        file_n+=1


def main():
    main_path = 'G:/Users/AlexandreCorreia/GitHub/Originals/Mohid/Software/'
    f90_files = GetF90Files(main_path)
    keywords = GetKeywords(f90_files)
    WriteKeywordsToFile('./MOHIDkeywords.txt', keywords, n=4)
    blocks = GetBlocks(f90_files)
    WriteKeywordsToFile('./MOHIDblocks.txt', blocks, n=1)
    properties = getProperties(f90_files)
    WriteKeywordsToFile('./MOHIDproperties.txt', properties, n=1, quotations=True)


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
