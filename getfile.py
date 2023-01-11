import os

FOLDER_TYPE = 0
FILE_TYPE = 1
CHAR_BLANK = '     '
CHAR_LAST = '└─'
CHAR_START = '├─'
CHAR_MIDDLE = '│  '

class Node:    
    def __init__(self, name, layer, type=FILE_TYPE, index=0) -> None:
        self.__type = type
        self.__prefix = ''
        self.name = name
        #树的深度
        self.layer = layer
        self.index = index
        #树的后代个数
        self.weight = 0
        self.isLastFlag = False

    def isDir(self) -> bool:
        if (self.__type == FOLDER_TYPE):
            return True
        else:
            return False

    def isFile(self) -> bool:
        if (self.__type == FILE_TYPE):
            return True
        else:
            return False

    def addWeight(self, weight):
        self.weight += weight

    def addPrefix(self, prefix):
        self.__prefix += prefix

    def printNode(self):
        lis = [self.name, self.layer, self.index, self.weight, self.isLastFlag]
        print(lis)

    def setLastFlag(self):
        self.isLastFlag = True

    def printTree(self):
        return self.__prefix+self.name




def scanFile(path, layer=1, nodeIndex=1):
    """递归扫描文件和文件夹

    Args:
        path (string): 扫描文件路径
        layer (int, optional): 递归层数. Defaults to 1.
        nodeIndex (int, optional): 深度优先遍历多叉树序号. Defaults to 1.

    Returns:
        _type_: [fileDic, folderLists, nodeIndex]
                fileDic: 文件字典,文件路径为key,文件名为值
                folderLists: 文件夹列表
    """    
    #init
    tmpFileLists = []
    tmpFolderLists = []
    fileDic = {}
    folderLists = []
    resFileDic = []
    resFolderList = []

    #零号节点，包含所有遍历得到的文件夹
    if (nodeIndex == 1):
        zeroItem = Node('.', 0, FOLDER_TYPE)
        zeroItem.setLastFlag()
        folderLists.append(zeroItem)

    try:
        fileLists = os.listdir(path)
    except Exception as e:
        print("Ukown filepath {}, please enter right filepath", path)
    pass

    #print(fileLists)

    #separate file and folder
    for id in range(len(fileLists)):
        if (os.path.isdir(os.path.join(path, fileLists[id]))):
            tmpFolderLists.append(Node(fileLists[id], layer, type=FOLDER_TYPE))
        else:
            tmpFileLists.append(Node(fileLists[id], layer, type=FILE_TYPE))
    fileLists = tmpFileLists
    fileDic[path] = fileLists

    #recursion handle folderList
    #update weight and nodeindex
    for index in range(len(tmpFolderLists)):
        item = tmpFolderLists[index]
        if (index == len(tmpFolderLists) - 1):
            item.setLastFlag()
        item.index = nodeIndex
        nodeIndex += 1
        nextPath = os.path.join(path, item.name)
        resFileDic, resFolderList, nodeIndex = scanFile(nextPath, layer=layer+1, nodeIndex=nodeIndex)

        item.addWeight(len(resFolderList))
        
        #update data
        fileDic.update(resFileDic)
        folderLists.append(item)
        folderLists = folderLists + resFolderList

    if (layer == 1):
        folderLists[0].addWeight(len(folderLists)-1)

    return [fileDic, folderLists, nodeIndex]
    


def printTree(nodeList, index):
    """描绘文件夹树

    Args:
        nodeList (list): 文件夹列表
        index (int): 节点序号
    """    
    while(True):
        if (index >= len(nodeList) or nodeList[index].weight == 0):
            break
        
        item = nodeList[index]
        isLastFlag = False
        
        #循环每棵树的子节点
        for sonIndex in range(item.weight):
            curIndex = sonIndex + item.index + 1
            #根据是否是父节点的儿子来判断添加什么前缀字符串
            if (nodeList[curIndex].layer == item.layer + 1):
                if (nodeList[curIndex].isLastFlag):
                    nodeList[curIndex].addPrefix(CHAR_LAST)
                    isLastFlag = True
                else:
                    nodeList[curIndex].addPrefix(CHAR_START)
            else:
                if (isLastFlag):
                    nodeList[curIndex].addPrefix(CHAR_BLANK) 
                else:
                    nodeList[curIndex].addPrefix(CHAR_MIDDLE)
        
        #只递归父节点的儿子节点
        for sonIndex in range(item.weight):
            curIndex = sonIndex + item.index + 1
            if (nodeList[curIndex].layer == item.layer + 1):
                printTree(nodeList, curIndex)
        
        if (isLastFlag):
            break
        index = index + nodeList[index].weight + 1
        

def getfile(filePath, resPath='', encoding='utf-8', extendName=True, isRecursion=True, isFindFile=True):
    """_summary_

    Args:
        filePath (str): 想遍历的文件路径
        resPath (str): 输出的文件路径,默认输出在同路径下的result.txt
        encoding (str, optional): 编码格式. Defaults to 'utf-8'.
        extendName (bool, optional): 是否需要后缀名. Defaults to True.
        isRecursion (bool, optional): 是否递归扫描路径下所有文件. Defaults to True.
        isFindFile (bool, optional): 是否输出所有文件结果 Defaults to True.
    """    
    tmpFileLists = []
    tmpFolderLists = []
    fileDic = {}
    folderLists = []

    try:
        fileLists = os.listdir(filePath)
    except Exception as e:
        print("Error for filePath, please enter right filepath")

    if (isRecursion):
        fileDic, folderLists, deleIndex = scanFile(filePath)
        pass
    else:
        #separate file and folder
        for id in range(len(fileLists)):
            if (os.path.isdir(os.path.join(filePath, fileLists[id]))):
                tmpFolderLists.append(Node(fileLists[id], layer=1, type=FOLDER_TYPE))
            else:
                tmpFileLists.append(Node(fileLists[id], layer=1, type=FILE_TYPE))
        fileDic[filePath] = tmpFileLists
        folderLists = tmpFolderLists

    if (isFindFile):
        printTree(folderLists, 0)
        pass
    else:
        fileDic.clear()
        pass

    resPath = os.path.join(filePath, 'result.txt')
    with open(resPath, 'w', encoding=encoding) as resFile:
        for item in folderLists:
            resFile.write(item.printTree() + '\n')

        resFile.write('\n==========================\n\n')

        for key in fileDic:
            resFile.write(key+ ':\n')
            for item in fileDic[key]:
                resFile.write('      ' + item.name+ '\n')



getfile('C:\\learn')


