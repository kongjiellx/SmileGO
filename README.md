# SmileGO
use keras<br>
first vesion only use cnn to build a policy network<br>
will add MTCS and RL<br>
=======
自己写着玩的围棋ai。<br>
目前暂时仅仅采用cnn构建策略网络。后期准备逐步加入蒙特卡洛和强化学习方法。<br>
使用keras编写模型，仅仅是简单的三层cnn加上BN。<br>
使用一万盘棋的棋谱，大概200w步。测试正确率30%多一点点的样子。<br>
目前估计棋力大概略比18k高一丝丝<br>
……尴尬<br>
=======
2017.4.24
keras2.0和1.0版本同一模型跑出的结果会有所差别。模型训练采用的是keras1.0.6版本。
修复此bug后棋力略有提升，初步估计有14k以上。但是死活还是比较差。
