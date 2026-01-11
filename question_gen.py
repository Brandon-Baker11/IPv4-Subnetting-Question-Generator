# pylint: disable = line-too-long
# pylint: disable = missing-function-docstring
# pylint: disable = invalid-name
""" Program that will be used to practice subnetting"""
import random


def new_host_address():
    """Funtion generates a random host IP address"""
    num_roll = random.randint(1, 3)

    if num_roll == 1:
        host_address = [10]
        for _ in range(3):
            host_address.append(random.randint(0, 255))
    elif num_roll == 2:
        host_address = [172]
        host_address.append(random.randint(16, 31))
        for _ in range(2):
            host_address.append(random.randint(0, 255))
    elif num_roll == 3:
        host_address = [192, 168]
        for _ in range(2):
            host_address.append(random.randint(0, 255))

    return host_address


def get_variable_subnet_mask(ip, masks):

    if ip[0] == 10:
        add_zeroes = 2
        init_subnet = [255]
        for _ in range(3):
            octet = random.choice(masks)
            if octet != 255:
                init_subnet.append(octet)
                break
            init_subnet.append(octet)
            add_zeroes -= 1

        if add_zeroes > 0:
            for _ in range(add_zeroes):
                init_subnet.append(0)

    elif ip[0] == 172:
        add_zeroes = 1
        init_subnet = [255, 255]
        for _ in range(2):
            octet = random.choice(masks)
            if octet != 255:
                init_subnet.append(octet)
                break
            init_subnet.append(octet)
            add_zeroes -= 1

        if add_zeroes > 0:
            init_subnet.append(0)

    elif ip[0] == 192:
        init_subnet = [255, 255, 255]
        octet = random.choice(masks)
        if octet == 255:
            while octet == 255:
                octet = random.choice(masks)
        init_subnet.append(octet)

    return init_subnet


def get_cidr_block(subnet_mask, masks):
    cidr_notation = ""

    if subnet_mask[1] != 255:
        cidr_blocks_a = ["/9", "/10", "/11", "/12", "/13", "/14", "/15", "16"]
        variable_mask = subnet_mask[1]
        cidr_block_index = masks.index(variable_mask)
        cidr_notation = cidr_blocks_a[cidr_block_index]
    elif subnet_mask[2] != 255:
        cidr_blocks_b = ["/17", "/18", "/19",
                         "/20", "/21", "/22", "/23", "/24"]
        variable_mask = subnet_mask[2]
        cidr_block_index = masks.index(variable_mask)
        cidr_notation = cidr_blocks_b[cidr_block_index]
    elif subnet_mask[3] != 255:
        cidr_blocks_c = ["/25", "/26", "/27",
                         "/28", "/29", "/30", "/31", "/32"]
        variable_mask = subnet_mask[3]
        cidr_block_index = masks.index(variable_mask)
        cidr_notation = cidr_blocks_c[cidr_block_index]

    return cidr_notation


def get_interesting_octet(subnet_mask):
    for octet in subnet_mask:
        if octet != 255:
            int_octet_index = subnet_mask.index(octet)
            break

    return int_octet_index


def get_address_block(subnet_mask):
    for octet in subnet_mask:
        if octet != 255:
            int_octet = octet
            break
    block = 256 - int_octet

    return block


def get_network_address(subnet_mask, ip, address_size, int_octet):

    net_address = []
    index = 0

    for octet in subnet_mask:
        if octet == 255:
            net_address.append(ip[index])
            index += 1

    boundary_start = 0
    boundary_end = address_size - 1

    if ip[int_octet] > boundary_start and ip[int_octet] > boundary_end:
        while ip[int_octet] > boundary_start and ip[int_octet] > boundary_end:
            boundary_start += address_size
            boundary_end += address_size
        net_address.append(boundary_start)

    if len(net_address) < 4:
        while len(net_address) < 4:
            net_address.append(0)

    return net_address


def get_broadcast_address(subnet_mask, ip, address_size, int_octet):
    bcast_address = []
    index = 0
    for octet in subnet_mask:
        if octet == 255:
            bcast_address.append(ip[index])
            index += 1

    boundary_start = 0
    boundary_end = address_size - 1

    if ip[int_octet] > boundary_start and ip[int_octet] > boundary_end:
        while ip[int_octet] > boundary_start and ip[int_octet] > boundary_end:
            boundary_start += address_size
            boundary_end += address_size
        bcast_address.append(boundary_end)

    if len(bcast_address) < 4:
        while len(bcast_address) < 4:
            bcast_address.append(255)

    return bcast_address


def get_first_host(net_address):
    first_host = []
    index = 0

    for _ in net_address:
        first_host.append(net_address[index])
        index += 1
    first_host[3] = first_host[3] + 1

    return first_host


def get_last_host(bcast_address):
    last_host = []
    index = 0

    for _ in bcast_address:
        last_host.append(bcast_address[index])
        index += 1
    last_host[3] = last_host[3] - 1

    return last_host


def get_placement():
    num_roll = random.randint(1, 6)
    place = ""

    if num_roll == 1:
        place = "first"
    elif num_roll == 2:
        place = "second"
    elif num_roll == 3:
        place = "third"
    elif num_roll == 4:
        place = "fourth"
    elif num_roll == 5:
        place = "fifth"
    elif num_roll == 6:
        place = "sixth"

    return place


def get_number_of_subnets(ip, subnet_mask, masks):
    borrowed_bits = 0
    possible_subnets = 0

    if ip[0] == 10:
        for _ in subnet_mask[1:]:
            if _ == 255:
                borrowed_bits += 8
            else:
                borrowed_bits += masks.index(_)
                break
        possible_subnets = 2 ** (borrowed_bits + 1)

    elif ip[0] == 172:
        for _ in subnet_mask[2:]:
            if _ == 255:
                borrowed_bits += 8
            else:
                borrowed_bits += masks.index(_)
                break
        possible_subnets = 2 ** (borrowed_bits + 1)

    else:
        borrowed_bits += masks.index(subnet_mask[3])
        possible_subnets = 2 ** (borrowed_bits + 1)

    return possible_subnets


def get_number_of_hosts(ip, subnet_mask, masks):
    host_bits = 0
    possible_hosts = 0
    mask_octet = 0

    if ip[0] == 10:
        for _ in subnet_mask[::-1]:
            if _ == 0:
                host_bits += 8
            else:
                mask_octet = masks.index(_) + 1
                host_bits += 8 - mask_octet
                break
        possible_hosts = (2 ** host_bits) - 2

    elif ip[0] == 172:
        if subnet_mask[3] == 0:
            host_bits += 8
            mask_octet = masks.index(subnet_mask[2]) + 1
            host_bits += 8 - mask_octet
            possible_hosts = (2 ** host_bits) - 2
        else:
            mask_octet = masks.index(subnet_mask[3]) + 1
            host_bits += 8 - mask_octet
            possible_hosts = (2 ** host_bits) - 2

    else:
        mask_octet = masks.index(subnet_mask[3]) + 1
        host_bits += 8 - mask_octet
        possible_hosts = (2 ** host_bits) - 2

    return possible_hosts


def display_banner():
    display = print(r""" 
    
               _____                                                      
              / ___/__  ______  ___  _____                                
              \__ \/ / / / __ \/ _ \/ ___/                                
             ___/ / /_/ / /_/ /  __/ /                                    
            /____/\__,_/ .___/\___/_/                                     
         _____       _/_/             __  __               __             
        / ___/__  __/ /_  ____  ___  / /_/ /____  _____    \ \            
        \__ \/ / / / __ \/ __ \/ _ \/ __/ __/ _ \/ ___/     \ \           
       ___/ / /_/ / /_/ / / / /  __/ /_/ /_/  __/ /         / /           
      /____/\__,_/_.___/_/ /_/\___/\__/\__/\___/_/         /_/_____       
                                                            /_____/       
     """)
    return display


def start_super_subnetter():

    return


def menus():

    return


def generate_question(ip, cidr, subnet_mask, net_address, place):
    num_roll = random.randint(1, 28)
    subnetting_question = ""

    if num_roll == 1:
        subnetting_question = f"What valid host range is the IP address {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} a part of?"
    elif num_roll == 2:
        subnetting_question = f"What valid host range is the IP address {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} a part of?"
    elif num_roll == 3:
        subnetting_question = f"Which subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belong to?"
    elif num_roll == 4:
        subnetting_question = f"Which subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belong to?"
    elif num_roll == 5:
        subnetting_question = f"What subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belong to?"
    elif num_roll == 6:
        subnetting_question = f"What subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belong to?"
    elif num_roll == 7:
        subnetting_question = f"Your server needs to be assigned the last usable host address on the {place} subnet of network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}. What address would you assign to the server?"
    elif num_roll == 8:
        subnetting_question = f"Your server needs to be assigned the last usable host address on the {place} subnet of network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What address would you assign to the server?"
    elif num_roll == 9:
        subnetting_question = f"What is the first valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
    elif num_roll == 10:
        subnetting_question = f"What is the first valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belongs to?"
    elif num_roll == 11:
        subnetting_question = f"What is the broadcast address of the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} is a part of?"
    elif num_roll == 12:
        subnetting_question = f"What is the broadcast address of the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} is a part of?"
    elif num_roll == 13:
        subnetting_question = f"What is the last valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belongs to?"
    elif num_roll == 14:
        subnetting_question = f"What is the last valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
    elif num_roll == 15:
        subnetting_question = f"What is the broadcast address of network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}?"
    elif num_roll == 16:
        subnetting_question = f"What is the broadcast address of network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 17:
        subnetting_question = f"You need to assign a server the last valid host address on the subnet {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}. What IP address would you assign?"
    elif num_roll == 18:
        subnetting_question = f"You need to assign a server the last valid host address on the subnet {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What IP address would you assign?"
    elif num_roll == 19:
        subnetting_question = f"How many subnets and hosts per subnet can you get from the network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}?"
    elif num_roll == 20:
        subnetting_question = f"How many subnets and hosts per subnet can you get from the network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 21:
        subnetting_question = f"What is the last valid host on subnet {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}?"
    elif num_roll == 22:
        subnetting_question = f"What is the last valid host on subnet {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 23:
        subnetting_question = f"You have the following subnetted network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}. You need to assign your router the first usable host address on the {place}. subnet. What address would you use?"
    elif num_roll == 24:
        subnetting_question = f"You have the following subnetted network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. You need to assign your router the first usable host address on the {place}. subnet. What address would you use?"
    elif num_roll == 25:
        subnetting_question = f"How many subnets are available with the network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}"
    elif num_roll == 26:
        subnetting_question = f"How many subnets are available with the network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 27:
        subnetting_question = f"How many hosts are available with the network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]}{cidr}?"
    elif num_roll == 28:
        subnetting_question = f"How many hosts are available with the network {net_address[0]}.{net_address[1]}.{net_address[2]}.{net_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    return subnetting_question


possible_variable_masks = [128, 192, 224, 240, 248, 252, 254, 255]
ip_address = new_host_address()
variable_length_subnet_mask = get_variable_subnet_mask(
    ip_address, possible_variable_masks)
cidr_block = get_cidr_block(
    variable_length_subnet_mask, possible_variable_masks)
address_block = get_address_block(variable_length_subnet_mask)
interesting_octet = get_interesting_octet(variable_length_subnet_mask)
network_address = get_network_address(
    variable_length_subnet_mask, ip_address, address_block, interesting_octet)
broadcast_address = get_broadcast_address(
    variable_length_subnet_mask, ip_address, address_block, interesting_octet)
first_valid_host = get_first_host(network_address)
last_valid_host = get_last_host(broadcast_address)
placement = get_placement()
num_of_subnets = get_number_of_subnets(
    ip_address, variable_length_subnet_mask, possible_variable_masks)
num_of_hosts = get_number_of_hosts(
    ip_address, variable_length_subnet_mask, possible_variable_masks)
question = generate_question(
    ip_address, cidr_block, variable_length_subnet_mask, network_address, placement)
banner = display_banner()

# ***BE SURE TO DEFINE THE LISTS THAT ARE USED MULTIPLE TIMES ONCE AND PROVIDE THEM AS AN ARGUMENT FOR EACH FUNCTION***

# print(ip_address, cidr_block, subnet_mask, network_address)
# print(f"IP Address: {ip_address}")
# print(f"CIDR Block: {cidr_block}")
# print(f"Subnet Mask: {subnet_mask}")
# print(f"Network Address: {network_address}")
# print(f"Broadcast Address: {broadcast_address}")
# print(f"Interesting Octet: {interesting_octet}")
# print(f"Address Block: {address_block}")
# print(f"First Host: {first_valid_host}")
# print(f"Last Host: {last_valid_host}")
# print(f"Placement {placement}")
print(question)
print(f"Number of subnets: {num_of_subnets}")
print(f"Number of hosts: {num_of_hosts}")
print(banner)


# Questions that only require a host IP and subnet or CIDR block

# "What valid host range is the IP address [ip address/CIDR] a part of?",
# "What is the first valid host address on the subnet that host [ip address subnet mask] belongs to?",
# "Which subnet does host [hostip/cidr] belong to? (random host)",
# "What is the broadcast address of the subnet that host [ipaddress/cidr] is a part of?",
# "What subnet does host [hostip/cidr] belong to?",
# "What is the last valid host address on the subnet that host [hostip/cidr] belongs to?"

# "Your server needs to be assigned the last usable host address on the 5th subnet of network [subnetip/CIDR]. What address would you assign to the server?",
# "**You need to divide the [subnetadd] into [x amount] of subnets with [x amount] of hosts per subnet. What subnet mask should you use?",
# "What is the broadcast address of network [subnetadd/cidr]?",
# "You need to subnet the [subnetadd] network into [x amount] of different subnets. What subnet mask would you use?",
# "You need to assign a server the last valid host address on the subnet [subnetadd/cidr]. What IP address would you assign?",
# "How many subnets and hosts per subnet can you get from the network [subnetadd/cidr]?",
# "What is the last valid host on subnet [subnetadd/cidr]?",
# "You have been given the [subnetadd] network. You need to design a subnet mask that will give you [x amount] of subnets and up to [x amount] of hosts. What subnet mask should you use?",
# "You have the following subnetted network [subnetadd/cidr]. You need to assign your router the first usable host address on the third/fourth/fifth/etc. subnet. What address would you use?",
# "How many subnets are available with the network [subnet/ip]?"
# "Network [network_add] needs to be divided into [x amount] subnets, while keeping as many usable hosts in each subnet as possible. What mask should be used"
