# Oh My Vim

这是我的vim配置文件,大体的功能有C、C++、Java、Python语言的语法高亮、语法检查、代码自动补全等功能，具
体个功能比较多，这里就不一一列举了，详情见Vimrc的注释。  

![intro](https://raw.githubusercontent.com/wiki/DerekChenGit/oh_my_vim/images/oh_my_vim.gif "intro")

## 如何安装

### 1. 安装Vim和Vim基本插件

首先安装好Vim和Vim的基本插件，这些使用apt-get安装即可。  

### 2. Vim配置文件

在终端内输入： 
```bash
git clone https://github.com/DerekChenGit/oh_my_vim
```
```bash
cp oh_my_vim/vimrc ~/.vimrc
```

### 3. 安装Ctags：apt-get install ctags

ctags可以建立源码树的标签索引（标签就是一个标识符被定义的地方，如函数定义），使程序员在编程时能迅速定位函数、变量、宏定义等位置去查看原形。

### 4. 安装Bundle

终端内执行:   
```bash
git clone https://github.com/gmarik/vundle.git~/.vim/bundle/vundle
```
在终端内打开Vim，在命令模式下输入:BundleInstall。这样Vim所需要的插件会自动安装。  

### 5. 编译YouCompleteMe

在终端内执行:  
```bash
cd ~/.vim/bundle/YouCompleteMe
```
```bash
./install --clang-completer 
```
这句话支持C/C++补全使用。  

