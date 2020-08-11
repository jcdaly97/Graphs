def alphabetize(arr):
    temp = arr
    temp.sort()
    for word in temp:
        print(word)

x = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
alphabetize(x)