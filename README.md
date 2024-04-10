# 拼音注音轉換器（Python實現）

本項目是至今為止網路上最好用的「漢語拼音」──「注音符號」轉換工具之一，由Python實現。

通過Converter.py中的Converter類，任何人可輕鬆實現任意長度的「漢語拼音標準拼式」──「國語注音符號標準注音文」的互相轉換，另外本項目亦可用於解析複雜的拼式或注音文，也可以幫助提取任何文章中的所有漢語拼音或注音符號。

具體使用方法如下：

注意：使用前必須將「音節對照表.csv」和「漢語拼音聲調表.csv」兩個必要輔助檔案放置到與Converter類所在的Python檔案（即此倉庫中的示例──「Converter.py」）相同的目錄下。

初始化Converter類對象：

```{python}
converter=Converter()
```

以下正常的示例均使用例句「穿上綠皮襖流利地唱山歌」──「chuānshànglǜpí'ǎoliúlìdechàngshān'gē」──「ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋ˙ㄉㄜㄔㄤˋㄕㄢㄍㄜ」。

## 標準漢語拼音拼式或注音文的轉換

```{python}
converter.convert_pinyin("chuānshànglǜpí'ǎoliúlìdechàngshān'gē")
converter.convert_zhuyin('ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋ˙ㄉㄜㄔㄤˋㄕㄢㄍㄜ')
```

以上兩行代碼返回值相同，實際應用中只需其中某一行即可。

返回值是一個長度為4的元組（tuple），其內容如下：

```{python}
("chuānshànglǜpí'ǎoliúlìdechàngshān'gē",
'ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋ˙ㄉㄜㄔㄤˋㄕㄢㄍㄜ',
['chuān', 'shàng', 'lǜ', 'pí', 'ǎo', 'liú', 'lì', 'de', 'chàng', 'shān', 'gē'],
['ㄔㄨㄢ', 'ㄕㄤˋ', 'ㄌㄩˋ', 'ㄆㄧˊ', 'ㄠˇ', 'ㄌㄧㄡˊ', 'ㄌㄧˋ', '˙ㄉㄜ', 'ㄔㄤˋ', 'ㄕㄢ', 'ㄍㄜ'])
```

其中第一個元素為標準的漢語拼音拼式（為字符串str，除必要時使用隔音符「'」外其餘均無間隔），第二個元素為標準的國語注音符號注音文（為字符串str，除必要時使用空格外其餘均無間隔），第三個元素為解析出的所有單字的漢語拼音列表（list），第四個元素為解析出的所有單字的注音符號列表（list）。

## 不規範的注音文的轉換

注意到上面傳入的注音文中輕聲調號「˙」位於音節左側（即「˙ㄉㄜ」），但若使用位於音節右側的不規範寫法（即「ㄉㄜ˙」）也不影響其解析，如：

```{python}
converter.convert_zhuyin('ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋㄉㄜ˙ㄔㄤˋㄕㄢㄍㄜ')
```

以上代碼的返回值與之前完全相同。本項目只生成標準的（教科書）注音文寫法，不規範的寫法可使用解析出的結果（即返回的tuple中的第四個元素）自行處理得到。

## 帶分隔符的漢語拼音拼式或注音文的轉換

在傳入的漢語拼音或注音符號之間插入（一個或多個）不屬於其字符集範圍的特殊符號，如空格、豎線（「|」）等，均不影響其解析，如：

```{python}
converter.convert_pinyin("chuān shàng lǜ pí ǎo liú lì de chàng shān gē")
converter.convert_zhuyin('ㄔㄨㄢ ㄕㄤˋ ㄌㄩˋ ㄆㄧˊ ㄠˇ ㄌㄧㄡˊ ㄌㄧˋ ˙ㄉㄜ ㄔㄤˋ ㄕㄢ ㄍㄜ')
converter.convert_pinyin("chuān|shàng|lǜ|pí|ǎo|liú|lì|de|chàng|shān|gē")
converter.convert_zhuyin('ㄔㄨㄢ|ㄕㄤˋ|ㄌㄩˋ|ㄆㄧˊ|ㄠˇ|ㄌㄧㄡˊ|ㄌㄧˋ|˙ㄉㄜ|ㄔㄤˋ|ㄕㄢ|ㄍㄜ')
```

以上每行代碼的返回值均與之前完全相同。

## 替換隔音符（分隔符）為其他字符

標準漢語拼音的隔音符為「'」，但也可將其替換為任意其他字符（如「|」等），如：

```{python}
converter.convert_pinyin("chuānshànglǜpí'ǎoliúlìdechàngshān'gē",pinyin_split='|')
```

以上代碼的返回值為：

```{python}
('chuānshànglǜpí|ǎoliúlìdechàngshān|gē',
'ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋ˙ㄉㄜㄔㄤˋㄕㄢㄍㄜ',
['chuān', 'shàng', 'lǜ', 'pí', 'ǎo', 'liú', 'lì', 'de', 'chàng', 'shān', 'gē'],
['ㄔㄨㄢ', 'ㄕㄤˋ', 'ㄌㄩˋ', 'ㄆㄧˊ', 'ㄠˇ', 'ㄌㄧㄡˊ', 'ㄌㄧˋ', '˙ㄉㄜ', 'ㄔㄤˋ', 'ㄕㄢ', 'ㄍㄜ'])
```

注意到只有第一個元素有變化。

注音符號的默認分隔符為空格，亦可在參數`zhuyin_split`中修改，如「居安思危」──「jū'ānsīwéi」──「ㄐㄩ ㄢㄙ ㄨㄟˊ」：

```{python}
converter.convert_zhuyin('ㄐㄩ ㄢㄙ ㄨㄟˊ')
converter.convert_zhuyin('ㄐㄩ ㄢㄙ ㄨㄟˊ',pinyin_split='|',zhuyin_split='|')
```

以上兩行代碼的返回值分別為：

```{python}
("jū'ānsīwéi", 'ㄐㄩ ㄢㄙ ㄨㄟˊ', ['jū', 'ān', 'sī', 'wéi'], ['ㄐㄩ', 'ㄢ', 'ㄙ', 'ㄨㄟˊ'])
('jū|ānsīwéi', 'ㄐㄩ|ㄢㄙ|ㄨㄟˊ', ['jū', 'ān', 'sī', 'wéi'], ['ㄐㄩ', 'ㄢ', 'ㄙ', 'ㄨㄟˊ'])
```

## 非法拼式或注音文

若傳入的拼式或注音文為非法，函式返回`('', '', [], [])`，如：

```{python}
converter.convert_pinyin('ansel')
converter.convert_zhuyin('ansel')
```

以上兩行代碼返回值均為：

```{python}
('', '', [], [])
```

## 提取文章中所有的拼式或注音

`extract_all_pinyin`和`extract_all_zhuyin`兩個函式可以幫助提取一篇文章中的所有拼式和注音符號，返回類型為列表（list），如：

```{python}
converter.extract_all_pinyin('''《大陸居民臺灣正體字講義》一簡多繁辨析之「裊、嬝、嫋、褭」→「袅」
辨音：「裊、嬝、嫋、褭」音niǎo。
辨意：「裊」是指柔軟美好、搖曳、擺動、繚繞、揮打、揮舞，如「裊裊」（縈迴繚繞的樣子）、「裊裊上升」、「裊裊炊煙」、「青煙裊裊」等。而「嬝」則是指纖細柔美或搖曳（通「裊」），如「嬝娜（niǎonuó）」（姿態柔美的樣子，又稱「嬝嬝娜娜」）、「嬝嬝婷婷」（女子體態輕盈優雅的樣子）、「輕嬝嬝」（纖細婉柔的樣子）等。而「嫋」則是指長弱貌、嬌柔美好、音調悠揚婉轉、搖擺、擺動，如「嫋嫋」（形容輕盈柔弱；形容搖曳不定；音調悠揚不絕；風動的樣子）、「餘音嫋嫋」等。而「褭」則是指以絲帶飾馬、「騕褭（yǎoniǎo）」（古駿馬名，也作「要褭（yāoniǎo）」）、吹拂、柔軟美好（通「裊」、「嫋」），如「娉娉褭褭（pīngpīngniǎoniǎo）」（輕盈柔美的樣子）等。現代語境中區分「裊」、「嬝」、「嫋」和「褭」，只要記住「騕褭」、「娉娉褭褭」必須用「褭」，「餘音嫋嫋」一般用「嫋」，形容女子姿態柔美一般用「嬝」，否則一律用「裊」即可。
偏旁辨析：「裊」、「褭」均可作偏旁，如「嬝」、「㒟」、「㠡」、「䃵」等。''')
```

以上代碼返回值為`['pīngpīngniǎoniǎo', 'niǎonuó', 'yǎoniǎo', 'yāoniǎo', 'niǎo']`。

注意，這兩個函式的返回值中相同的字符串（str）只會出現一次，所有字符串都依照從長到短的順序排列，方便用於搜索替換等後續任務。