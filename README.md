# 基于协同的推荐算法

这是一个基础版本，仅使用相似性实现推荐算法。

## 运行环境

- Python 3
	+ numpy
	+ mongodb
- nodejs
	+ vue
	
```
cd web_front_end
npm install

# 运行后端服务
cd web_api
python ./api.py

# 运行web界面
cd web_front_end
npm run dev

浏览器打开  http://localhost:8080
```

## TODO LIST

- SVD 矩阵分解
- 优化评分系统
- 建立用户画像