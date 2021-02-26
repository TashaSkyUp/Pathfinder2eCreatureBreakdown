# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!dir

invalid=['A-C\n', '11\n',
         'Introduction\n',
         'A-C\n', 'D\n',
         'E-G\n', 'H-K\n',
         'L-N\n', 'O-R\n',
         'S-T\n', 'U-Z\n',
         'Appendix\n',
         'Bestiary\n']
template = [[-2,'CREATURE'],
            [1,['TINY','SMALL','MEDIUM','LARGE','HUGE','GARGANTUAN']],
            [2,['TINY','SMALL','MEDIUM','LARGE','HUGE','GARGANTUAN']],            
            [0,'Perception','numeric'],
            [0,'Languages'],
            [0,'Skills'],
            [0,'Str'],
            [0,'Slow'],
            [0,'AC'],
            [0,'HP'],
            [0,'Speed'],
            ['any','[one-action]'],
            ['any','[two-actions]'],
            ['any','[three-actions]'],            
            ['any','[free-action]'],
            ['any','[reaction]'],            
            ]
def load_lines(file = 'monstersbook1' ):
    stream = open('./'+file,encoding=None,errors='replace',)
    a=stream.read()
    a=a.replace("\nCha ", ' Cha ')
    a=a.replace("\nWis ", ' Wis ')
    a=a.replace("Wis\n", 'Wis ')
    a=a.splitlines()
    lines=[]
    line=''    
    for i in range(27804):
        #if stream.
        #print(i)
        try:
            oldline=line
            #line =stream.readline()
            line=a[i]
            #line = stream.read()
        except:
            pass
            #line ='ERROR # previous line: '+str(i)+' '+oldline
            #print(line)

        if  line == '342\n':
            print('found 342: ',i,line)
            break            
        elif len(line)>0:
            lines.append(line)
            #print(i,line)
    return lines;
        
    
def sentance_continues(line):
    if ',\n' in line:        
        return True
    if "and\n" in line[-5:]:
        return True
    return False

def is_complete(line):
    if line.count('(')- line.count(')')==0:
        return 'maybe'
    else:
        return 'false'

def dont_use():
    outlines=[]

    oldline='old'
    newline='new'
    out=''
    for i in range(len(lines)):
        oldline = newline
        newline = lines[i]

        out = out + newline.replace("\n",' ')

        if sentance_continues(newline) or is_complete(out)=='false':
            pass
        else:
            outlines.append(out)
            out=''

    #print(outlines[1:100])
    lines = outlines
            

def fit_line_to_template(line):
    #for all templates
    to_return =-1
    line = line.replace(';',' ')
    line = line.replace(',',' ')
    
    for sub_temp_num, sub_template in enumerate(template):
        key_idx= sub_template[0]
        key = sub_template[1]
        words = line.split(' ')
        lenwords  =len(words)
        if lenwords  == 1:
            words = line
        #print(words,lenwords,key_idx)
        
        if key_idx =='any':
            found = line
            if key in line:
                return sub_temp_num

        #if there are enough words in the line to support the key index            
        elif len(words)>abs(key_idx):          
            
            found = words[key_idx]                                    

            if found == key:
                to_return = sub_temp_num
                #print('found',line)
            
            if (type(key)==list ) and (found in key):
                to_return = sub_temp_num
                #print('found',line)
                
            if to_return !=-1:
                if len(sub_template)==3:
                    if sub_template[2]=='numeric':                    
                        try:                        
                                float(words[key_idx+1])
                                #print('numeric: to return=',to_return)
                        except:
                                to_return=-1

            if to_return !=-1:
                return to_return
        
    return  -1
   
                
def get_creature_blocks(file='monstersbook1'):
    lines=load_lines(file)
    current_creature=-1
    creature_name=''
    creatures_blocks={}
    for line in lines:
        line = line.replace('Ã—','x')
        line = line.replace('â€™','\'')
        line = line.replace('â€“','-')
        if 'CREATURE' in line.split(' '):
            template_position=1
            current_creature+=1
            creature_name = ' '.join(line.split(' ')[:-2])
            #print("loaded.."+creature_name)
            creatures_blocks[creature_name] = {"name":line.strip()}
        elif line in invalid:
            pass
        elif len(creature_name)>0:
            position = fit_line_to_template(line)
            if position >=0:
                if str(position) in creatures_blocks[creature_name]:
                    pass
                    #print("error position already take @",creature_name,str(position))
                    #print("existing ; ",creatures_blocks[creature_name][str(position)])
                    #print("just read; ",line.strip())
                else:
                    creatures_blocks[creature_name][str(position)]=line.strip()
            else:
                pass
    #print (len(creatures_blocks))
    #for creature in creatures_blocks.keys():
    #    print("-")
    #    for line in creatures_blocks[creature]:
    #        print (line)
    #    #print('\n')
    print(len(creatures_blocks)," creatures loaded!")
    return creatures_blocks
