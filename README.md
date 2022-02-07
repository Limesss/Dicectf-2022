# Dicectf-2022

问题出现在这里的free ，也就是当最后一个玩家离开这个棋格的时候会free掉这个棋格的postion_name_ptr, 但是问题就在没有好好经过处理，导致棋在离开后又通过chutes-and-ladders 跳回来的话，就会导致UAF。
![image](https://user-images.githubusercontent.com/55912947/152720453-27a8c29b-75cb-4b8e-a466-af29ce1679b3.png)
![image](https://user-images.githubusercontent.com/55912947/152720351-e08cde47-3f0c-47df-b56d-34ce9417d2f3.png)
