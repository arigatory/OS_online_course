import bitstring 


memory = {}
logical_addresses = []


with open("dataset_44327_15 (1).txt", "r") as f:
    first_line = f.readline()
    next_line = first_line
    m = int(first_line.split()[0])
    q = int(first_line.split()[1])
    r = int(first_line.split()[2])

    for i in range(m):
        next_line = f.readline()
        memory[int(next_line.split()[0])] = format(int(next_line.split()[1]), "064b")
    
    for i in range(q):
        next_line = f.readline()
        logic_address = format(int(next_line), "064b")
        logical_addresses.append(logic_address)
        
with open('my_output.txt','w') as f:
    for i in range(q):
        logic_address = logical_addresses[i]
         
        pml4 = int(PML4(logic_address),2)
        directory_ptr = int(DirectoryPtr(logic_address),2)
        directory = int(Directory(logic_address),2)
        table = int(Table(logic_address),2)
        offset = int(Offset(logic_address),2)

        pml4e = memory.get(r+8*pml4,format(0, "064b"))
        if P(pml4e) == '0':
            f.write('fault\n')
            continue
        popte = memory.get(PhysicalAddressInt(pml4e)+ 8*directory_ptr,format(0, "064b"))
        if P(popte) == '0':
            f.write('fault\n')
            continue
        pde   = memory.get(PhysicalAddressInt(popte) + 8*directory,format(0, "064b"))
        if P(pde)== '0':
            f.write('fault\n')
            continue
        pte   = memory.get(PhysicalAddressInt(pde) + 8*table,format(0, "064b"))
        if P(pte) == '0':
            f.write('fault\n')
            continue
        f.write(f'{PhysicalAddressInt(pte)+offset}\n')
