# pylint: disable = line-too-long
# pylint: disable = missing-function-docstring
# pylint: disable = invalid-name
# pylint: disable = trailing-whitespace
# pylint: disable = missing-module-docstring
import random


def new_host_address():

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


def get_subnet_id(subnet_mask, ip, address_size, int_octet):

    _id = []
    index = 0

    for octet in subnet_mask:
        if octet == 255:
            _id.append(ip[index])
            index += 1

    boundary_start = 0
    boundary_end = address_size - 1

    while ip[int_octet] > boundary_start and ip[int_octet] > boundary_end:
        boundary_start += address_size
        boundary_end += address_size

    _id.append(boundary_start)

    while len(_id) < 4:
        _id.append(0)

    return _id


def get_parent_network_id(subnet_mask, ip):
    parent_id = []
    index = 0

    for octet in subnet_mask:
        if octet == 255:
            parent_id.append(ip[index])
            index += 1

    while len(parent_id) < 4:
        parent_id.append(0)

    return parent_id


def get_broadcast_address(subnet_mask, address_size, net_address):

    bcast_address = []
    index = 0

    for octet in subnet_mask:
        if octet == 255:
            bcast_address.append(net_address[index])
            index += 1
        elif octet != 255 and octet > 0:
            bcast_address.append(net_address[index])

    bcast_address[index] += address_size - 1

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


def get_placement(subnet_mask):

    place = ""
    end_range = 0

    for octet in subnet_mask:
        if octet == 128:
            end_range = 2
            break
        elif octet == 192:
            end_range = 4
            break
        else:
            end_range = 8
            break

    num_roll = random.randint(1, 6)

    if end_range == 2:
        if num_roll == 1:
            place = "first"
        else:
            place = "second"

    if end_range == 4:
        if num_roll == 1:
            place = "first"
        elif num_roll == 2:
            place = "second"
        elif num_roll == 3:
            place = "third"
        else:
            place = "fourth"

    if end_range == 8:
        if num_roll == 5:
            place = "fifth"
        elif num_roll == 6:
            place = "sixth"
        elif num_roll == 7:
            place = "seventh"
        else:
            place = "eighth"

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
    display = r""" 
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
     """
    return display


def start_super_subnetter():

    return


def menus():

    return


def generate_qna(ip, cidr, subnet_mask, subnet_id, bcast_address, place, first_host, last_host, host_amount, subnet_amount, parent_id):
    aaa = [5, 6, 21, 22]
    # num_roll = random.randint(1, 26)
    num_roll = random.choice(aaa)
    question = ""
    answer = ""

    if num_roll == 1:
        question = f"What valid host range is the IP address {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} a part of?"
        answer = f"{first_host[0]}.{first_host[1]}.{first_host[2]}.{first_host[3]} - {last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 2:
        question = f"What valid host range is the IP address {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} a part of?"
        answer = f"{first_host[0]}.{first_host[1]}.{first_host[2]}.{first_host[3]} - {last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 3:
        question = f"Which subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belong to?"
        answer = f"{subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}"
    elif num_roll == 4:
        question = f"Which subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belong to?"
        answer = f"{subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}"
    elif num_roll == 5:
        question = f"Your server needs to be assigned the last usable host address on the {place} subnet of network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]}{cidr}. What address would you assign to the server?"
        answer = f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"
    elif num_roll == 6:
        question = f"Your server needs to be assigned the last usable host address on the {place} subnet of network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What address would you assign to the server?"
        answer = f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"
    elif num_roll == 7:
        question = f"What is the first valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
        answer = f"{first_host[0]}.{first_host[1]}.{first_host[2]}.{first_host[3]}"
    elif num_roll == 8:
        question = f"What is the first valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belongs to?"
        answer = f"{first_host[0]}.{first_host[1]}.{first_host[2]}.{first_host[3]}"
    elif num_roll == 9:
        question = f"What is the broadcast address of the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} is a part of?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 10:
        question = f"What is the broadcast address of the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} is a part of?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 11:
        question = f"What is the last valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belongs to?"
        answer = f"{last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 12:
        question = f"What is the last valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
        answer = f"{last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 13:
        question = f"What is the broadcast address of network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 14:
        question = f"What is the broadcast address of network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 15:
        question = f"You need to assign a server the last valid host address on the subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}. What IP address would you assign?"
        answer = f"{last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 16:
        question = f"You need to assign a server the last valid host address on the subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What IP address would you assign?"
        answer = f"{last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 17:
        question = f"How many subnets and hosts per subnet can you get from the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{host_amount} hosts and {subnet_amount} subnets"
    elif num_roll == 18:
        question = f"How many subnets and hosts per subnet can you get from the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{host_amount} hosts and {subnet_amount} subnets"
    elif num_roll == 19:
        question = f"What is the last valid host on subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 20:
        question = f"What is the last valid host on subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{last_host[0]}.{last_host[1]}.{last_host[2]}.{last_host[3]}"
    elif num_roll == 21:
        question = f"You have the following subnetted network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]}{cidr}. You need to assign your router the first usable host address on the {place} subnet. What address would you use?"
        answer = f"{first_host[0]}.{first_host[1]}.{first_host[2]}.{first_host[3]}"
    elif num_roll == 22:
        question = f"You have the following subnetted network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. You need to assign your router the first usable host address on the {place} subnet. What address would you use?"
        answer = f"{first_host[0]}.{first_host[1]}.{first_host[2]}.{first_host[3]}"
    elif num_roll == 23:
        question = f"How many subnets are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}"
        answer = f"{subnet_amount} subnets"
    elif num_roll == 24:
        question = f"How many subnets are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{subnet_amount} subnets"
    elif num_roll == 25:
        question = f"How many hosts are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{host_amount} hosts"
    elif num_roll == 26:
        question = f"How many hosts are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{host_amount} hosts"
    return {"question": question, "answer": answer}


possible_variable_masks = [128, 192, 224, 240, 248, 252, 254, 255]
ip_address = new_host_address()
variable_length_subnet_mask = get_variable_subnet_mask(
    ip_address, possible_variable_masks)
cidr_block = get_cidr_block(
    variable_length_subnet_mask, possible_variable_masks)
address_block = get_address_block(variable_length_subnet_mask)
interesting_octet = get_interesting_octet(variable_length_subnet_mask)
subnetted_network_id = get_subnet_id(
    variable_length_subnet_mask, ip_address, address_block, interesting_octet)
broadcast_address = get_broadcast_address(
    variable_length_subnet_mask, address_block, subnetted_network_id)
parent_network_id = get_parent_network_id(
    variable_length_subnet_mask, ip_address)
first_valid_host = get_first_host(subnetted_network_id)
last_valid_host = get_last_host(broadcast_address)
placement = get_placement(variable_length_subnet_mask)
num_of_subnets = get_number_of_subnets(
    ip_address, variable_length_subnet_mask, possible_variable_masks)
num_of_hosts = get_number_of_hosts(
    ip_address, variable_length_subnet_mask, possible_variable_masks)
q_n_a = generate_qna(
    ip_address, cidr_block, variable_length_subnet_mask, subnetted_network_id, broadcast_address, placement, first_valid_host, last_valid_host, num_of_hosts, num_of_subnets, parent_network_id)
banner = display_banner()

# THE QUESTIONS THAT ARE BEING TESTED NEED TO HAVE THEIR OWN FUNCTION THAT WILL FIND THE FIRST/LAST ADDRESS OF THE SPECIFIED (1ST, 2ND, 3RD, ETC.) SUBNET
# MAY NEED TO INCLUDE THE BOUNDARY SETTER FROM THE OG NETWORK ID FUNCTION AND USE LENGTH TO MOVE THE WINDOW n TIMES AS NEEDED

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
print(q_n_a.get("question"))
print(q_n_a.get("answer"))
# print(f"Number of subnets: {num_of_subnets}")
# print(f"Number of hosts: {num_of_hosts}")
# print(banner)
# print(parent_network_id)


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
