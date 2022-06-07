# gitFlow

## git Flow 几个分支意义

### master

主要用于对外发布稳定的新版本，该分支时常保持着软件可以正常运行的状态，由于要维护这一状态，所以不允许开发者直接对 master 分支的代码进行修改和提交，其他分支的开发工作进展到可以发布的程度后，将会与 master 分支进行合并，并且这一合并只在发版时进行，发布时将会附加版本编号的 Git 标签。

### dev

用来存放我们最新开发的代码，这个分支是我们开发过程中代码中心分支，这个分支也不允许开发者直接进行修改和提交。程序员要以 develop 分支为起点新建 feature 分支，在 feature 分支中进行新功能的开发或者代码的修正，也就是说 develop 分支维系着开发过程中的最新代码，以便程序员创建 feature 分支进行自己的工作。

### feature

功能分支，当你需要开发一个新的功能的时候，可以新建一个 feature-xxx 的分支，在里边开发新功能，这也是我们日常工作的大本营，开发完成后，将之并入 develop 分支中

### release

发版的时候拉的分支，当我们所有的功能做完之后，准备要将代码合并到 master 的时候，从 develop 上拉一个 release-xxx 分支出来，这个分支一般处理发版前的一些提交以及客户体验之后小 BUG 的修复（BUG 修复后也可以将之合并进 develop），不要在这个里边去开发功能，在预发布结束后，将该分支合并进 develop 以及 master，然后删除 release

### hotfixes

用来修复 BUG 的，当我们的项目上线后，发现有 BUG 需要修复，那么就从 Master 上拉一个名为 fixbug-xxx 的分支，然后进行 BUG 修复，修复完成后，再将代码合并到 Master 和 Develop 两个分支中，然后删除 hotfix 分支


## Gitflow分支命名规范

分支	| 作用
:---: | :---:
master	| 迭代历史稳定生产分支
dev	| 集成最新开发特性的活跃分支
f_xxx  | feature 功能特性开发分支
b_xxx	| bug修复分支
r_xxx	| release 版本发包分支

## 企业级大型项目git工作流流程

1. 默认有master/dev分支

2. 本地切换到远程dev分支，远端头分离(head detached)即远端到本机的映射、只可读
    
       git checkout origin/dev  

3. 基于切换到远程的dev，创建本地dev分支

       git checkout -b dev

4. 本地dev与远端dev进行关联

       git branch --set-upstream-to=origin/dev  

5. 基于dev开发登录功能，创建f_login分支

       git checkout -b f_login  

6. 当login功能开发完成，即可申请合并到dev(通常dev仅管理者有操作权限)，即创建merge request给管理者

7. dev管理者同意申请，f_login将合并到dev，并删除远程f_login分支

8. 同时本地可以删除f_login分支、缓存的远程f_login

       git branch -d f_login
       git branch -dr origin/f_login

9. 然后本地切换回dev分支，git pull更新后(必须！)，继续进行其他功能的开发

10. 当需求的所有功能开发完成，可基于dev分支创建release分支，处理发版前的一些提交以及客户体验之后小BUG的修复
11. release版本没有问题，同样merge request申请合并到master
12. master上线中发现BUG，那么就基于Master创建一个hotfixes分支进行修复，修复完成后，将代码合并到Master和Develop两个分支并删除hotfix分支

## git冲突解决

冲突描述：基于远程dev分支，有两个f_order、f_comment功能分支，现f_comment合并到dev出现冲突

* 解决方式一
  * 获取远程最新dev代码

        git fetch origin dev       // fetch只拉取代码而不合并
  * 对比代码，将本地f_comment分支代码，与拉取到的origin/dev进行对比，查看冲突之处，当然借助pycharm，直接右击冲突文件，选择git -> compare with branch，可视化显示冲突

        git diff origin/dev        
  * 修改冲突地方后提交并推送代码
  * 发起合并请求
  
* 解决方式二
  * 拉取远程dev并合并到当前f_comment，借助pycharm执行会提示冲突，解决后合并即可

        git pull origin dev
  * 查看冲突的代码

        git status
  * 找到冲突的文件，修改冲突后提交并推送代码
  * 发起合并请求














