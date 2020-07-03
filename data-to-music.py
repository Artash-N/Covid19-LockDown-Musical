from miditime.miditime import MIDITime
import csv
import matplotlib.pyplot as plt

def listint(x):
    return(int(x[0]))
    
def chunks(l, n):
    nl = []
    """Yield n number of sequential chunks from l."""
    d, r = divmod(len(l), n)
    for i in range(n):
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        nl.append( l[si:si+(d+1 if i < r else d)])
    return nl

def Average(lst):
    return sum(lst) / len(lst)

csvfile = open(r'C:\Users\vikas\Desktop\2020 COVID19 Sensors\beat.csv', newline='')
file = csv.reader(csvfile, delimiter=' ', quotechar='|')

data_raw = list(file)


dust = []
light = []

for row in data_raw:
    l , d = row[0].split(',')
    dust.append(int(d))
    light.append(int(l))

#c = chunks(data, 64)
#
#all_avg = []
#
#for i in c:
#    all_avg.append(Average(i))


midinotes_light = []
midinotes_dust = []
mymidi_light = MIDITime(120, r'C:\Users\vikas\Desktop\2020 COVID19 Sensors\music beat\test-light.mid')
mymidi_dust = MIDITime(120, r'C:\Users\vikas\Desktop\2020 COVID19 Sensors\music beat\test-dust.mid')




a = 0
for i in light:
    i = int(i)
    midinotes_light.append([a,i,63,1])
    a=a+1
    
a = 0
for i in dust:
    i = int(i)
    midinotes_dust.append([a,i,63,1])
    a=a+1
    


mymidi_light.add_track(midinotes_light)
mymidi_dust.add_track(midinotes_dust)
# Output the .mid file
mymidi_light.save_midi()
mymidi_dust.save_midi()