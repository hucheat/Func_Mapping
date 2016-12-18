# Func_Mapping
異想天開的PHP基礎函數關係圖生成

編程水平太渣、、

## 想法

靜態分析源碼文本，得到自定義函數的一些信息

- 函數名 fn - str
- 函數所在行 fl - int
- 函數所在文件 fp - str
- 函數參數 fa - list
- 函數內部調用函數 ff - list
- 函數返回參數 fr - str

函數信息以json存儲

讀取函數信息，生成關係調用圖

## 實現

- 遍歷所有源碼文件
- 分析函數
    - 獲取函數名
    - 獲取函數參數
    - 獲取行號

## 未實現

- 匹配花括號獲取函數體
    - 獲取函數內部調用函數
- 生成圖

## 目前

匹配大括號。。(邏輯混亂了，憂傷)

## 判斷函數內部函數

    //自定義函數
    for n in self.data.keys():
        if n in funcBody:
            ff.append(n)
    //內部函數
    for n in phpFuncs:
        if n in funcBody:
            ff.append(n)
