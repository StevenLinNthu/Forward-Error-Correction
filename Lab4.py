#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import warnings
warnings.simplefilter("ignore", DeprecationWarning)


# In[2]:


def random_defec(data, times=1):
    randList = random.sample(range(len(data)), times)
    tmp = list(data)
    for pos in randList:
        tmp[pos] = str(1-int(tmp[pos]))
    data = ''.join(tmp)
    return data


# In[3]:


def hamming_encode(ori):
    code = '0000'
    ori = ori[0:4]+code[0]+ori[4:7]+code[1]+ori[7]+code[2:]
    tmp = []
    for i in range(len(ori)):
        if ori[i] == '1':
            tmp.append(12-i)
    #print(tmp)
    for i in tmp:
        code = int(code, 2) ^ int(str(i), 10)   
        code = '{:04b}'.format(code)
    #print(code)    
    enc = ori[0:4]+code[0]+ori[5:8]+code[1]+ori[9]+code[2:]
    return enc


# In[4]:


def hamming_decode(enc):
    code = enc[4]+enc[8]+enc[10:]
    tmp = []
    dec =''
    for i in range(len(enc)):
        if enc[i] == '1' and i not in [4,8,10,11]:
            tmp.append(12-i)
    for i in tmp:
        code = int(code, 2) ^ int(str(i), 10)   
        code = '{:04b}'.format(code)
    #print(code)
    pos = -1
    if code != '0000':
        pos = int(code, 2)
    for i in range(len(enc)):
        if i not in [4,8,10,11]:
            if i != 12 - pos:
                dec += enc[i]
            else:
                dec += str(1 - int(enc[i]))
    return dec


# In[5]:


#hamming code(12,8)
original = np.random.randint(2, size=1024)#'00111001'
a=''
for i in original:
    a += str(i)
original = a
print(original)
encode ,defective ,decode = '', '', ''
for i in range(int(len(original)/8)):
    enc = hamming_encode(original[i*8:i*8+8])
    encode += enc 
defec = random_defec(encode)
for i in range(int(len(encode)/12)):
    dec = hamming_decode(encode[i*12:i*12+12])
    decode += dec
original == decode


# In[6]:


original == decode


# In[7]:


def linear_block_encode(ori):
    m = np.fromstring(ori, dtype='u1') - ord('0')
    G = np.matrix([[1,0,0,0,1,1,1],[0,1,0,0,1,1,0],[0,0,1,0,1,0,1],[0,0,0,1,0,1,1]])
    c = np.matmul(m, G)
    enc=''
    for i in range(7):
        if c.item(i)%2 == 0:
            enc += '0'
        else:
            enc += '1'
    #print(encode)
    return enc


# In[8]:


def linear_block_decode(enc):
    HT = np.matrix([[1,1,1],[1,1,0],[1,0,1],[0,1,1],[1,0,0],[0,1,0],[0,0,1]])
    errorList = ['111','110','101','011','100','010','001','000']
    x = np.fromstring(enc, dtype='u1') - ord('0')
    s = np.matmul(x, HT)
    #print(s)
    pos=''
    for i in range(3):
        if s.item(i)%2 == 0:
            pos += '0'
        else:
            pos += '1'
    pos = errorList.index(pos)
    if pos < 7:
        enc = enc[:pos] + str(1 - int(enc[pos])) + enc[pos+1:]
    dec = enc[:4]
    return dec


# In[9]:


#linear block code(7,4)
original = np.random.randint(2, size=1024)#'00111001'
a=''
for i in original:
    a += str(i)
original = a
print(original)
encode ,defective ,decode = '', '', ''
for i in range(int(len(original)/4)):
    enc = linear_block_encode(original[i*4:i*4+4])
    encode += enc 
defec = random_defec(encode)
for i in range(int(len(encode)/7)):
    dec = linear_block_decode(encode[i*7:i*7+7])
    decode += dec
original == decode


# In[10]:


def cyclic_encode(ori):
    table = ['0000000','0001011','0010110','0011101','0100111','0101100','0110001','0111010',
            '1000101','1001110','1010011','1011000','1100010','1101001','1110100','1111111']
    enc = table[int(ori, 2)]
    return enc


# In[11]:


def cyclic_decode(enc):
    g = [1,0,1,1]
    errorList = ['101','111','110','011','100','010','001','000']
    table = ['0000000','0001011','0010110','0011101','0100111','0101100','0110001','0111010',
            '1000101','1001110','1010011','1011000','1100010','1101001','1110100','1111111']
    encList = [int(x) for x in list(enc)]
    for i in range(4):
        if encList[i] == 1:
            for j in range(4):
                encList[i+j] = max(encList[i+j], g[j]) - min(encList[i+j], g[j])
    #print(encList)
    s = ''.join([str(x) for x in encList[4:]])
    pos = errorList.index(s)
    if pos < 7:
        enc = enc[:pos] + str(1 - int(enc[pos])) + enc[pos+1:]
    dec = '{:04b}'.format(table.index(enc))
    return dec


# In[12]:


#cyclic code(7,4)
original = np.random.randint(2, size=1024)#'00111001'
a=''
for i in original:
    a += str(i)
original = a
print(original)
encode ,defective ,decode = '', '', ''
for i in range(int(len(original)/4)):
    enc = cyclic_encode(original[i*4:i*4+4])
    encode += enc 
defec = random_defec(encode)
for i in range(int(len(encode)/7)):
    dec = cyclic_decode(encode[i*7:i*7+7])
    decode += dec
original == decode


# In[ ]:




