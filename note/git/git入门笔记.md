## Git入门
### Git介绍
虽然git跟svn都是版本管理工具，但是git和svn有个本质上的区别是git是分布式版本管理工具，而svn是集中式版本管理。
我们以前都是使用svn进行代码管理，都知道在svn上看体检记录是需要连上svn服务上获取的会比较慢，同样的道理svn的commit和checkout都是很慢的，而且这些操作都需要连网。但是git就不一样了，git是分布式版本管理，因此我们所有人的本地都会有代码仓库的完整镜像，记录所有的commit和版本记录，查看提交记录，提交和checkout你会发现简直是飞一般的感觉，而且这些操作在我们断网的情况下也可以操作，只有将本地库push到远程库时需要联网。
下面我们来简单介绍下git的各个空间，以及我们写的代码在各个空间是如何流转的。简单来说，git主要分成本地和远程两大空间，而本地空间有分为工作目录，缓存区和HEAD区三部分。文件在各空间流转过程可以详看下图：
![Git常用命令流转图.png](../../image/git/Git常用命令流转图.png)
### Git常用命令
从图中我们可以看到常用的命令主要有如下几条：
 * ```git init```：初始化git仓库
 * ```git add```：将工作目录中修改记录在缓存区中
 * ```git commit```：将缓存区中内容提交到本地HEAD 区中
 * ```git push```：将HEAD区内容推送到远程库中
 * ```git checkout```：将暂存区分支内容checkout出来，并替换工作目录中内容；即切换分支并将分支内容覆盖工作目录。（注意跟svn的checkout区别，这个操作比较危险，会恢复工作目录中的内容）【git checkout – filename 撤销文件修改但为缓存的内容】
 * ```git checkout HEAD```：这个与git checkout类似，不同的是这个命令将HEAD区的内容checkout出来，替换暂存区和工作目录的内容。【HEAD实际是一个指向你正在工作中的本地分支最新提交记录的指针】
 * ```git reset HEAD```：这个与上面的git checkout HEAD 类似，不同在于将HEAD区内容替换暂存区内容，但是不修改工作目录，即撤销上一次git add暂存的内容
 * ```git fetch```：从远程库拉取更新到本地HEAD区，默认会拉取所有分支，可以指定分支。
 * ```git merge```：将指定分支合并到当前分支中。
 * ```git pull```：取回远程分支，并于本地分支合并
 * ```git rm --cache```：直接从暂存区删除记录，但是不修改本地工作目录（即将文件从git跟踪清单中移除，git不在追踪此文件的改变）
 * ```git clone```：从现有git仓库中拉取项目。（通常本地新拉取一个新的项目，和git init一样为初始化本地仓库的命令，不一样的地方在于git init没有远程仓库，git clone已有远程仓库）
 * ```git status```：可以查看当前仓库的状态
 * ```git reset HEAD```：取消已缓存的内容（即如果一个文件已经git add到缓存区里，可以执行git reset HEAD 取消此文件的缓存，等价于没有执行git add操作）
 * ```git mv```：修改文件名，这也是git和svn差异比较大的一点，svn是记录文件的整个修改过程来记录文件的修改，而git是根据文件内容快照来记录文件修改，因此如果我们直接改文件名而不修改文件内容，在git的元数据仓库里体现不出这次修改。等价于如下三条操作
```git
$ mv README.txt README
$ git rm README.txt
$ git add README
```
 * ```git remote –v```：查看当前仓库的远程库列表
通过上面的介绍我们都知道了git是直接记录文件内容快照的，因此若我们合并分支出现了冲突仅需要编辑文件内容合并冲突就可以，编辑完后记得git add和git commit

