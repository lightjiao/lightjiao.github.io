---
title: "在WSL中使用git svn"
date: 2020-08-14T21:44:53+08:00
draft: false
tags:
 - Git
---

### 什么是git svn？

官方说明地址： https://git-scm.com/docs/git-svn

git svn是git的一个命令，通过这个命令，可以将远程的svn仓库clone到本地成一个git仓库，并且这个命令可以将git的commit提交到svn，以及从svn同步内容到git。

简而言之git svn就是用`git`的形式管理一个`svn`仓库。

而且通过git svn clone到本地的git仓库和其他git仓库没有区别：

- 可以设置remote git repo
- 可以非常轻易的新建、删除、rebase、merge 一个branch
- 可以有本地的 stage、commit 以及stash



### 使用git svn的原因

我目前就职于一家游戏公司，svn简单易上手同时又足够强大，而游戏开发似乎对分支、版本的要求很弱，故svn非常适合团队使用。完美达到简单够用并且做达到版本管理的目的。

我是一名程序，写代码的时候希望能够有本地的commit和stage、stash等特性，而这些特性svn都没有。有过一次手滑提交了写了一半的代码后，觉得有必要在本地搞个git。查询了一番，发现有git svn能够用git的形式管理svn，很满足我的需求。



### 如何在WSL中安装git svn

- > WSL即[Windows Subsystem for Linux](https://docs.microsoft.com/zh-cn/windows/wsl/about)，是一个能在windows上跑linux命令的东西，我几乎就是用他来跑git命令，很方便顺手

- 不要使用homebrew（homebrew的git-svn折磨人总是缺少module安装不成功），用apt安装最新版本git、subversion、git-svn即可正常使用。

 -  添加apt代理
    ```
    # 创建文件
    sudo touch /etc/apt/apt.conf.d/proxy.conf
    ```
    将下面的内容写到文件中（代理地址需要用自己的代理）
    ```
    Acquire::http::Proxy "http://user:password@proxy.server:port/";
    Acquire::https::Proxy "http://user:password@proxy.server:port/";
    ```
    
  - ```
    # 安装gcc
    sudo apt update
    sudo apt install build-essential
    sudo apt-get install manpages-dev
    ```
    
  - ```
    # 安装最新版git 和 git-svn
    sudo apt-add-repository ppa:git-core/ppa
    sudo apt-get update
    sudo apt-get install git
    sudo apt-get install git-core
    sudo apt-get install subversion
    sudo apt-get install git-svn
    ```
    
  - `git svn clone` 的时候出现了一个wsl的文件权限问题，参考 https://askubuntu.com/questions/911804/ubuntu-for-windows-10-all-files-are-own-by-root-and-i-cannot-change-it 
  
  - `git svn clone`时候需要输入linux用户密码、svn用户、svn密码，然后静待clone完成即可
  
  - 一些必要的设置：
  
    > `git config core.filemode false` -- 避免WSL与windows的文件模式冲突
    >
    > `git config --global core.editor vim` 将默认编辑器设置为vim



### 使用git svn

使用 `git svn clone`之后的仓库本身是一个git仓库，本地的操作的部分和普通的git完全一样。下面是如何于svn交互：

- 从svn repo中同步最新的代码

  ```
  git svn rebase
  ```

- 将本地的代码推送到远程svn repo

  ```
  git svn dcommit
  ```



### 关于`git svn rebase`的说明

这个命令其实和git自身的`git rebase`命令逻辑上是一样的，只不过`git svn rebase`多了一层与svn仓库的交互。

`git rebase`是一个不那么常见的git命令，我也是机缘巧合下，参加了以前一位同事开的git讲座才了解到有这个命令。理解了这个命令后才算对git了有了比较熟悉的理解。

`git rebase` 和 进一步的 `git rebase -i` 是非常好用的两个命令，强烈推荐单独了解一下。限于篇幅，这里暂时引用一些其他说明文档吧：

- git官方对于git rebase的说明： https://git-scm.com/docs/git-rebase
- 知乎上关于`rebase`与`merge`的说明，我觉得这篇讲得很简介到位： https://www.zhihu.com/question/36509119 



### 使用git svn的缺陷

- ⚠最大的缺陷其实是 `git svn rebase`这个命令是基于`git rebase`的，这个命令本身就有些不那么好理解，再加上当遇到冲突需要处理的时候，rebase + conflict 足够让不熟悉 `git rebase -i`（中文译名：交互式变基）的人一壶喝好几天，学习难度直线上升。
- svn中是不记录提交用户的email的，所以每当提交到svn仓库后，git中设置的用户邮箱会丢失。（本来想用这个来刷github contribute，但失败了2333），看到这篇文章的你，如果有这个小问题的解决方法，欢迎评论或者邮件我。



### 结语

我在实际工作中使用git svn一个多星期了，感受是git svn 命令十分的成熟，目前没有遇到git于svn仓库的冲突问题。有普通的文件conflict也是正常的文件冲突，修改一下后继续rebase即可。

理论上可以设置一个git server，让程序团队全部用git，使得程序团队只与这个git server交互。并且git 有更成熟的工作流。

- 首先程序团队遵守git flow原则，即不在master分支提交，每次提交都是以分支的形式。push到远程的branch经过code review 再合并到master分支。
- git server repo支持设置钩子，在每次的push、pull、fetch、merge请求时，都先在master分支执行一次`git svn rebase`同步svn的提交.
- 每次merge后主动执行`git svn dcommit`向svn同步提交数据

使用git后可以有的工作流：

- git支持本地的钩子，每次 commit 自动格式化提交部分的代码，保证团队代码风格统一。
- git服务端可以使用[gitlab](http://gitlab.com/)（有免费版）。git强大的分支能力 + gitlab，可以大大提高code review的效率。

这样应该是可以无痛的让程序团队使用git的。之所以说是理论上，是因为我所在的公司目前只提供svn，似乎没有专门的IT support团队来负责提供公司的git服务，我也懒得折腾这些，所以没有实践过。目前本地的git svn能满足我的需求就好。

<br>

---

参考来源：

- https://tonybai.com/2019/06/25/using-git-with-svn-repo/



