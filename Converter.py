import csv,os
class Converter:
    zhuyin_tones=['','ˊ','ˇ','ˋ','˙']
    def __init__(self)->None:
        self.load_tones()
        self.load_syllables()
        self.load_valid_characters()
    def load_tones(self):
        self.vowels={}
        self.back_vowels={}
        full_path=os.path.realpath(__file__)
        path,_=os.path.split(full_path)
        with open(path+'/漢語拼音聲調表.csv',mode='r',encoding='utf-8') as tones:
            rows=csv.reader(tones)
            for row in rows:
                self.vowels[row[-1]]=[]
                for tone in row:
                    self.vowels[row[-1]].append(tone)
                    self.back_vowels[tone]=row[-1]
    def load_syllables(self):
        self.pinyin_syllables={}
        self.zhuyin_syllables={}
        full_path=os.path.realpath(__file__)
        path,_=os.path.split(full_path)
        with open(path+'/音節對照表.csv',mode='r',encoding='utf-8') as syllables:
            rows=list(csv.reader(syllables))
            for i in range(len(rows)//2):
                for j in range(len(rows[2*i])):
                    self.pinyin_syllables[rows[2*i][j]]=rows[2*i+1][j]
                    self.zhuyin_syllables[rows[2*i+1][j]]=rows[2*i][j]
    def load_valid_characters(self):
        self.pinyin_characters=set(self.back_vowels.keys())
        self.zhuyin_characters=set(self.zhuyin_tones)
        for syllable in self.pinyin_syllables:
            for character in syllable:
                self.pinyin_characters.add(character)
        for syllable in self.zhuyin_syllables:
            for character in syllable:
                self.zhuyin_characters.add(character)
    def extract_all_pinyin(self,article:str)->list:
        particles=set()
        i=0
        while i<len(article):
            if article[i] in self.pinyin_characters:
                index=i
                while index<len(article) and article[index] in self.pinyin_characters or "'"==article[i] or ' '==article[i]:
                    index+=1
                particle=article[i:index].strip()
                while ''!=particle and "'"==particle[-1]:
                    particle=particle[:-1]
                    particle=particle.strip()
                if ''!=particle:
                    particles.add(particle)
                i=index
            i+=1
        return list(reversed(sorted(list(particles),key=len)))
    def extract_all_zhuyin(self,article:str)->list:
        particles=set()
        i=0
        while i<len(article):
            if article[i] in self.zhuyin_characters:
                index=i
                while index<len(article) and article[index] in self.zhuyin_characters or ' '==article[i]:
                    index+=1
                particle=article[i:index].strip()
                if ''!=particle:
                    particles.add(particle)
                i=index
            i+=1
        return list(reversed(sorted(list(particles),key=len)))
    def normalize_pinyin(self,pinyin:str)->str:
        temp=''
        for i in range(len(pinyin)):
            if pinyin[i] not in self.pinyin_characters:
                temp+=' '
            else:
                temp+=pinyin[i]
        pinyin=temp
        pinyin=' '.join(pinyin.split())
        pure=''
        for letter in pinyin:
            if letter not in self.back_vowels:
                pure+=letter
            else:
                pure+=self.back_vowels[letter]
        return pure.split(),''.join(pinyin.split())
    def normalize_zhuyin(self,zhuyin:str)->str:
        temp=''
        for i in range(len(zhuyin)):
            if zhuyin[i] not in self.zhuyin_characters:
                temp+=' '
            else:
                temp+=zhuyin[i]
        zhuyin=temp
        zhuyin=' '.join(zhuyin.split())
        pure=''
        for letter in zhuyin:
            if letter not in self.zhuyin_tones:
                pure+=letter
            else:
                pure+=' '
        return pure.split(),''.join(zhuyin.split())
    def pinyin_split_search(self,current:str):
        bingo=False
        for i in range(len(current),0,-1):
            if current[:i] in self.pinyin_syllables:
                self.current_state.append(current[:i])
                if i!=len(current):
                    bingo=bingo or self.pinyin_split_search(current[i:])
                else:
                    self.results=self.current_state
                    bingo=True
                self.current_state=self.current_state[:-1]
            if bingo:
                break
        return bingo
    def zhuyin_split_search(self,current:str):
        bingo=False
        for i in range(len(current),0,-1):
            if current[:i] in self.zhuyin_syllables:
                self.current_state.append(current[:i])
                if i!=len(current):
                    bingo=bingo or self.zhuyin_split_search(current[i:])
                else:
                    self.results=self.current_state
                    bingo=True
                self.current_state=self.current_state[:-1]
            if bingo:
                break
        return bingo
    def pinyin_list_to_string(self,pinyin_list:list,pinyin_split:str="'")->str:
        if 0==len(pinyin_list):
            return ''
        pinyin=pinyin_list[0]
        for i in range(1,len(pinyin_list)):
            if ''!=pinyin_list[i-1] and ''!=pinyin_list[i]:
                comb=pinyin_list[i-1]+pinyin_list[i]
                temp=''
                for j in range(len(comb)):
                    if comb[j] in self.back_vowels:
                        temp+=self.back_vowels[comb[j]]
                    else:
                        temp+=comb[j]
                comb=temp
                need_split=comb in self.pinyin_syllables
                if not need_split and 1<len(comb):
                    for j in range(1,len(comb)):
                        if j!=len(pinyin_list[i-1]) and comb[:j] in self.pinyin_syllables and comb[j:] in self.pinyin_syllables:
                            need_split=True
                            break
                if need_split:
                    pinyin+=pinyin_split
            pinyin+=pinyin_list[i]
        return pinyin
    def zhuyin_list_to_string(self,zhuyin_list:list,zhuyin_split:str=' ')->str:
        if 0==len(zhuyin_list):
            return ''
        zhuyin=zhuyin_list[0]
        for i in range(1,len(zhuyin_list)):
            if ''!=zhuyin_list[i-1] and ''!=zhuyin_list[i] and zhuyin_list[i][0] not in self.zhuyin_tones and zhuyin_list[i-1][-1] not in self.zhuyin_tones:
                previous_zhuyin=zhuyin_list[i-1]
                comb=zhuyin_list[i-1]+zhuyin_list[i]
                for tone in self.zhuyin_tones:
                    comb=comb.replace(tone,'')
                    previous_zhuyin=previous_zhuyin.replace(tone,'')
                need_split=comb in self.zhuyin_syllables
                if not need_split and 1<len(comb):
                    for j in range(1,len(comb)):
                        if j!=len(previous_zhuyin) and comb[:j] in self.zhuyin_syllables and comb[j:] in self.zhuyin_syllables:
                            need_split=True
                            break
                if need_split:
                    zhuyin+=zhuyin_split
            zhuyin+=zhuyin_list[i]
        return zhuyin
    def add_tone_to_pinyin_syllable(self,pinyin:str,tone:int):
        vowel_indices=[]
        for i in range(len(pinyin)):
            if pinyin[i] in self.vowels:
                vowel_indices.append(i)
        toned_pinyin=''
        added=False
        skipped=False
        for i in range(len(pinyin)):
            if not added and not skipped and 1<len(vowel_indices) and pinyin[i] in ('i','u','ü'):
                toned_pinyin+=pinyin[i]
                skipped=True
            elif not added and pinyin[i] in self.vowels:
                toned_pinyin+=self.vowels[pinyin[i]][tone]
                added=True
            else:
                toned_pinyin+=pinyin[i]
        return toned_pinyin
    def add_tone_to_zhuyin_syllable(self,zhuyin:str,tone:int):
        if 4==tone:
            return self.zhuyin_tones[tone]+zhuyin
        else:
            return zhuyin+self.zhuyin_tones[tone]
    def convert_pinyin(self,pinyin:str,pinyin_split="'",zhuyin_split:str=' ')->tuple:
        pure,pinyin=self.normalize_pinyin(pinyin)
        syllables=[]
        for paragraph in pure:
            self.results=None
            self.current_state=[]
            self.pinyin_split_search(paragraph)
            syllables.append(self.results)
        pinyin_list=[]
        zhuyin_list=[]
        for i in range(len(syllables)):
            if None!=syllables[i]:
                for pure_syllable in syllables[i]:
                    pinyin_syllable=pinyin[:len(pure_syllable)]
                    tone=4
                    for character in pinyin_syllable:
                        if character in self.back_vowels:
                            new_tone=self.vowels[self.back_vowels[character]].index(character)
                            if new_tone<tone:
                                tone=new_tone
                    pinyin_list.append(self.add_tone_to_pinyin_syllable(pure_syllable,tone))
                    zhuyin_list.append(self.add_tone_to_zhuyin_syllable(self.pinyin_syllables[pure_syllable],tone))
                    pinyin=pinyin[len(pure_syllable):]
        return self.pinyin_list_to_string(pinyin_list,pinyin_split),self.zhuyin_list_to_string(zhuyin_list,zhuyin_split),pinyin_list,zhuyin_list
    def convert_zhuyin(self,zhuyin:str,pinyin_split="'",zhuyin_split:str=' ',irregular=False)->tuple:
        pure,zhuyin=self.normalize_zhuyin(zhuyin)
        syllables=[]
        for paragraph in pure:
            self.results=None
            self.current_state=[]
            self.zhuyin_split_search(paragraph)
            syllables.append(self.results)
        pinyin_list=[]
        zhuyin_list=[]
        for i in range(len(syllables)):
            if None!=syllables[i]:
                for pure_syllable in syllables[i]:
                    left_index=zhuyin.index(pure_syllable)
                    right_index=left_index+len(pure_syllable)-1
                    tone=0
                    if irregular:
                        if right_index+1<len(zhuyin) and zhuyin[right_index+1] in self.zhuyin_tones:
                            tone=self.zhuyin_tones.index(zhuyin[right_index+1])
                    else:
                        if left_index>0 and zhuyin[left_index-1]==self.zhuyin_tones[4]:
                            tone=4
                        elif right_index+1<len(zhuyin) and zhuyin[right_index+1] in self.zhuyin_tones[:4]:
                            tone=self.zhuyin_tones.index(zhuyin[right_index+1])
                    pinyin_list.append(self.add_tone_to_pinyin_syllable(self.zhuyin_syllables[pure_syllable],tone))
                    zhuyin_list.append(self.add_tone_to_zhuyin_syllable(pure_syllable,tone))
                    zhuyin=zhuyin[right_index+1:]
        return self.pinyin_list_to_string(pinyin_list,pinyin_split),self.zhuyin_list_to_string(zhuyin_list,zhuyin_split),pinyin_list,zhuyin_list
def main():
    converter=Converter()
    print(converter.convert_pinyin("chuānshànglǜpí'ǎoliúlìdechàngshān'gē"))
    print(converter.convert_zhuyin('ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋ˙ㄉㄜㄔㄤˋㄕㄢㄍㄜ'))
    print(converter.convert_zhuyin('ㄔㄨㄢㄕㄤˋㄌㄩˋㄆㄧˊㄠˇㄌㄧㄡˊㄌㄧˋㄉㄜ˙ㄔㄤˋㄕㄢㄍㄜ',irregular=True))
    print(converter.convert_zhuyin('ㄨㄛˇㄉㄜ˙ㄕ'))
    print(converter.convert_zhuyin('ㄨㄛˇㄉㄜ˙ㄕ',irregular=True))
    print(converter.convert_pinyin("chuān shàng lǜ pí ǎo liú lì de chàng shān gē"))
    print(converter.convert_zhuyin('ㄔㄨㄢ ㄕㄤˋ ㄌㄩˋ ㄆㄧˊ ㄠˇ ㄌㄧㄡˊ ㄌㄧˋ ˙ㄉㄜ ㄔㄤˋ ㄕㄢ ㄍㄜ'))
    print(converter.convert_pinyin("chuān|shàng|lǜ|pí|ǎo|liú|lì|de|chàng|shān|gē"))
    print(converter.convert_zhuyin('ㄔㄨㄢ|ㄕㄤˋ|ㄌㄩˋ|ㄆㄧˊ|ㄠˇ|ㄌㄧㄡˊ|ㄌㄧˋ|˙ㄉㄜ|ㄔㄤˋ|ㄕㄢ|ㄍㄜ'))
    print(converter.convert_pinyin("chuānshànglǜpí'ǎoliúlìdechàngshān'gē",pinyin_split='|'))
    print(converter.convert_zhuyin('ㄐㄩ ㄢㄙ ㄨㄟˊ'))
    print(converter.convert_zhuyin('ㄐㄩ ㄢㄙ ㄨㄟˊ',pinyin_split='|',zhuyin_split='|'))
    print(converter.convert_pinyin('ansel'))
    print(converter.convert_zhuyin('ㄢㄙㄜㄌ'))
    print(converter.extract_all_pinyin('''《大陸居民臺灣正體字講義》一簡多繁辨析之「裊、嬝、嫋、褭」→「袅」
辨音：「裊、嬝、嫋、褭」音niǎo。
辨意：「裊」是指柔軟美好、搖曳、擺動、繚繞、揮打、揮舞，如「裊裊」（縈迴繚繞的樣子）、「裊裊上升」、「裊裊炊煙」、「青煙裊裊」等。而「嬝」則是指纖細柔美或搖曳（通「裊」），如「嬝娜（niǎonuó）」（姿態柔美的樣子，又稱「嬝嬝娜娜」）、「嬝嬝婷婷」（女子體態輕盈優雅的樣子）、「輕嬝嬝」（纖細婉柔的樣子）等。而「嫋」則是指長弱貌、嬌柔美好、音調悠揚婉轉、搖擺、擺動，如「嫋嫋」（形容輕盈柔弱；形容搖曳不定；音調悠揚不絕；風動的樣子）、「餘音嫋嫋」等。而「褭」則是指以絲帶飾馬、「騕褭（yǎoniǎo）」（古駿馬名，也作「要褭（yāoniǎo）」）、吹拂、柔軟美好（通「裊」、「嫋」），如「娉娉褭褭（pīngpīngniǎoniǎo）」（輕盈柔美的樣子）等。現代語境中區分「裊」、「嬝」、「嫋」和「褭」，只要記住「騕褭」、「娉娉褭褭」必須用「褭」，「餘音嫋嫋」一般用「嫋」，形容女子姿態柔美一般用「嬝」，否則一律用「裊」即可。
偏旁辨析：「裊」、「褭」均可作偏旁，如「嬝」、「㒟」、「㠡」、「䃵」等。'''))
if '__main__'==__name__:
    main()