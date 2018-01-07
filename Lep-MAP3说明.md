## Lep-MAP3 遗传图谱构建软件    

### 更新时间  

2017/12/11 

### 软件适用群体    

[Lep-MAP3网站](https://sourceforge.net/projects/lep-map3/)并没有提到支持哪些群体，应该是常见的作图群体都适用；  

月季项目使用F1群体构建图谱  

### 一些可能会用到的脚本

路径：/p299/user/og03/chenquan1609/Resequencing/script/LepMAP

```shell
AverageDist.py
DealFinalResult.py
FilterDot.py
GeneticMapVCFfilter_F1.py
GroupMarker.py
gen_lmplotcheck_sh.py
marker_num_in_LG.py
OrderMarker.pl
postfile.py
rm_head_marker.py
SeparateChrom.pl
vcfFromStacks.awk
```

### 前期数据准备    

1. 对各个样品按群体的策略进行变异检测  

2. 对SNP做初步过滤处理，可以使用VCFTools完成，包括：QUAL、MQ、DP、非二等位位点、MAF

   注意：在这里可以先不考虑缺失，因为后续步骤会对部分样品做缺失处理，届时再一并过滤；  

   关于MAF：MAF似乎可以放在后面再过滤，但其实在进行偏分离检验时肯定会滤掉MAF不合格的位点，甚至都不用专门过滤；因此可以放在这一步达到初步过滤的目的

3. 对SNP做严格处理，包括：

   a. 将深度过低的样品设为缺失(DP < 5)  

   b. 将子代与亲本基因型不符的样品设为缺失(如亲本为0/1和0/0，子代不可能出现1/1)  

   c. 过滤亲本不含重组信息的位点(亲本基因型缺失的；亲本纯合且相等的)  

   d. 过滤整体缺失> 0.25 的位点  

   f. 过滤子代基因型不符合分离比的位点(segregation distortion)，使用卡方检验，p值一般设为0.001  

      这一步应该是过滤位点最多的  

   ```shell
   python GeneticMapVCFfilter.py

   usage: GeneticMapVCFfilter.py [-h] -v VCF -f PATERNAL -m MATERNAL [-d MIN_DP]
                                 [-r MISSING_RATE] [-p P_THRESHOLD]

   Filter vcf for GeneticMap

   optional arguments:
     -h, --help       show this help message and exit
     -v VCF           input vcf file
     -f PATERNAL      paternal ID
     -m MATERNAL      maternal ID
     -d MIN_DP        permitted minimum DP [5]
     -r MISSING_RATE  max-missing rate [0.25]
     -p P_THRESHOLD   pvalue threshold [0.001]
   ```

注意：如果是使用stacks做的变异检测，对于vcf文件需要做一步处理！  

`awk -f vcfFromStacks.awk geneticmap.vcf > geneticmap.format.vcf  `

### 软件使用    

路径：`/p299/user/og03/chenquan1609/Bin/LepMap3/`  

软件包括多个模块，主要使用ParentCall2 --> Filtering2 --> SeparateChromosomes2 --> JoinSingles2All --> OrderMarker2  [网站说明](https://sourceforge.net/p/lep-map3/wiki/Modules/)

* ParentCall2  

  输入：1. posteriors文件的头文件(格式如下)  2. VCF文件(实际上软件会从VCF文件中读取posteriors的信息，一般的项目中SNP的信息都是以VCF文件保存，所以这里只讲这种方式)

| CHR  | POS  |   Family    |   Family    |   Family    |     ...     |
| :--: | :--: | :---------: | :---------: | :---------: | :---------: |
| CHR  | POS  | Paternal ID | Maternal ID |  offs1 ID   |  offs2 ID   |
| CHR  | POS  |      0      |      0      | Paternal ID | Paternal ID |
| CHR  | POS  |      0      |      0      | Maternal ID | Maternal ID |
| CHR  | POS  |      1      |      2      |      0      |      0      |
| CHR  | POS  |      0      |      0      |      0      |      0      |

​      posteriors文件包括6行，每行的前两列都是一样的，下面的说明中将自动忽略这两列。  

​      第一行是family name；  

​      第二行依次为各个样品的ID，和VCF文件中的ID保持一致；具体的顺序有没有要求未做测试；  

​      第三、四行前面为0，后为Paternal ID和Maternal ID  

​      第五行为性别信息：1表示male，2表示female，0表示unknown；位置关系和第二行对应；  

​      第六行为表型信息，一般就都填0  

​     使用postfile.py生成post.txt(头文件)  

```shell
python postfile.py 

    Usage: postfile.py <vcf> <paternal ID> <maternal ID>

```



   `java -cp bin/ ParentCall2 data=post.txt vcfFile=final.snp.vcf > data.call 2> parentcall.log`

* Filtering2  

  实际就是对marker进行过滤，由于之前已经完成过滤，所以这一步可以省略。另外测试发现该步骤似乎达不到过滤的效果  

* SeparateChromosomes2  

  作图的关键步骤，按LOD值将marker划分到不同的连锁群。需要设置多个lodLimit值，达到理想的分群  

  ```shell
  java -cp bin/ SeparateChromosomes2 \ 
  data=data.call \
  lodLimit=35 \
  lod3Mode=3 \ 
  sizeLimit=40 > map.txt 2> map.log

  #lod3Mode参数: 
  # Controls how LOD scores are computed between double informative markers [1]
  #  1: haplotypes match (4 alleles, max LOD = log(4^n)
  #  2: homozygotes match (3 alleles, max LOD = log(3^n))
  #  3: homozygotes or heterozygotes match (2 alleles, max LOD = log(2^n))
  ```
  使用SeparateChrom.pl，nohup运行，自动投递任务；筛选最优LOD值  

  ```shell
  perl SeparateChrom.pl

    Usage: SeparateChrom.pl <data.call> <lod1> <lod2> <sizelimit>
  ```

  使用marker_num_in_LG.py查看分群结果，其中LG0表示的是未上图的marker  

  ```shell
  python marker_num_in_LG.py
    
    Usage: marker_num_in_LG.py <map.txt>
  ```

  也可使用GroupMarker.py，可以看到分群结果，同时会生成文件记录每个LG的marker

  ```shell
  python GroupMarker.py

    Usage: GroupMarker.py <map.txt> <data.call>
  ```

* JoinSingles2All  

  The JoinSingles2All module assigns singular markers to existing LGs by computing LOD scores between each single marker and markers from the existing LGs. It needs a map file as input parameter and then it outputs a new map file with possible more markers assigned to LGs. 可以再次计算LOD值，尝试将未上图的marker补充到LG中，可多次迭代至不能再上图。  

  ```shell
  java -cp bin/ JoinSingles2All \
  map=map.txt \
  data=data.call \
  lodLimit=35 \
  iterate=5 >map.iterated.txt
  ```

* OrderMarker2  

  对个连锁群的marker进行排序。每次运行结果不尽相同，可迭代多次，选择likelihood最大(非绝对值)的结果作为最终结果  

  ```shell
  java -cp bin/ OrderMarker2 \
  data=data.call \
  map=map.iterated.txt \
  chromosome=1 \
  sexAveraged=1 \
  useKosambi=1 > order.txt 2> order.log
  ```

  | marker_num | male_position | female_position |
  | :--------: | :-----------: | :-------------: |
  |    776     |     0.00      |      0.00       |
  |    508     |     0.13      |      0.13       |

  最终结果主要关注第二行和前3列：  

  第二行：LG = 1 likelihood = -55585.5126    表示1号连锁群，likelihood应该是取绝对值最大的结果？

  第一列：marker的标号，对应data.call中的相应marker，如776表示data.call文件中的第766个marker；  

  第二、三列：marker分别在父本图谱和母本图谱中的位置，如果设置了sexAveraged=1参数，得到的是  

  sex-average的图谱，male_position和female_position相同  

  使用OrderMarker.pl，nohup运行，自动投递任务

  ```shell
  perl OrderMarker.pl  

    Usage: OrderMarker.py <datafile> <mapfile> <number of LG> <iterate times>
  ```

  ​

* LMPlot 及图谱纠错

  使用Lep-Map3自带的LMPlot模块，对图谱作连线图进行评价，剔除异常marker后得到最终结果并作heatmap。

  ```shell
  # 使用gen_lmplotcheck_sh.py生成脚本，依次投递。
  python gen_lmplotcheck_sh.py
  	Usage: gen_lmplotcheck_sh.py <orderfile.lst>
  # 最终得到.dot文件，在作图之前可先用FilterDot.py进行一个初步检查，
  # 去掉那些连接错误的结果
  # 再对预筛选后的.dot结果作图；由于未能成功安装相应的linux软件，所以只能在windows下进行作图
  # 依据作图结果去掉可能错误的marker
  ```

  ```shell
  # 可使用rm_head_marker.py去掉错误的marker，该脚本只能去除开头连续的marker
  python rm_head_marker.py
  	Usage: rm_head_marker.py <orderfile> <rm former marker num>
  ```

* 提取最终结果


  ```shell
  python DealFinalResult.py

    Usage: DealFinalResult.py <OrderFile.lst> <data.call>
  ```

  对结果做统计

  ```shell
  python AverageDist.py
  	Usage: AverageDist.py <LG.map.lst>
  ```

  ​

  ​



