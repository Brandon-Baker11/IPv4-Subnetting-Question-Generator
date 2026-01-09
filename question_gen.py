# pylint: disable = line-too-long
# pylint: disable = missing-function-docstring
# pylint: disable = invalid-name
""" Program that will be used to practice subnetting"""
import random


def new_host_address():
    """Funtion generates a random host IP address"""
    num_roll = random.randint(1, 3)

    if num_roll == 1:
        ip_octets = [10]
        for _ in range(3):
            ip_octets.append(random.randint(0, 255))
    elif num_roll == 2:
        ip_octets = [172]
        ip_octets.append(random.randint(16, 31))
        for _ in range(2):
            ip_octets.append(random.randint(0, 255))
    elif num_roll == 3:
        ip_octets = [192, 168]
        for _ in range(2):
            ip_octets.append(random.randint(0, 255))

    # ip_address = f"{ip_octets[0]}.{ip_octets[1]}.{ip_octets[2]}.{ip_octets[3]}"
    host_address = ip_octets

    return host_address


def get_variable_subnet():
    masks = [128, 192, 224, 240, 248, 252, 254, 255]

    if ip_address[0] == 10:
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

    elif ip_address[0] == 172:
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

    elif ip_address[0] == 192:
        init_subnet = [255, 255, 255]
        octet = random.choice(masks)
        if octet == 255:
            while octet == 255:
                octet = random.choice(masks)
        init_subnet.append(octet)

    return init_subnet


def get_cidr_block():
    masks = [128, 192, 224, 240, 248, 252, 254, 255]

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


def get_interesting_octet():
    for octet in subnet_mask:
        if octet != 255:
            int_octet_index = subnet_mask.index(octet)
            break

    return int_octet_index


def get_address_block():
    for octet in subnet_mask:
        if octet != 255:
            int_octet = octet
            break
    block = 256 - int_octet

    return block


def get_network_add():

    net_address = []
    index = 0

    for octet in subnet_mask:
        if octet == 255:
            net_address.append(ip_address[index])
            index += 1

    boundary_start = 0
    boundary_end = address_block - 1

    if ip_address[interesting_octet] > boundary_start and ip_address[interesting_octet] > boundary_end:
        while ip_address[interesting_octet] > boundary_start and ip_address[interesting_octet] > boundary_end:
            boundary_start += address_block
            boundary_end += address_block
        net_address.append(boundary_start)

    if len(net_address) < 4:
        while len(net_address) < 4:
            net_address.append(0)

    return net_address


def get_broadcast_address():
    bcast_address = []
    index = 0
    for octet in subnet_mask:
        if octet == 255:
            bcast_address.append(ip_address[index])
            index += 1

    boundary_start = 0
    boundary_end = address_block - 1

    if ip_address[interesting_octet] > boundary_start and ip_address[interesting_octet] > boundary_end:
        while ip_address[interesting_octet] > boundary_start and ip_address[interesting_octet] > boundary_end:
            boundary_start += address_block
            boundary_end += address_block
        bcast_address.append(boundary_end)

    if len(bcast_address) < 4:
        while len(bcast_address) < 4:
            bcast_address.append(255)

    return bcast_address


def get_first_host():
    first_host = []
    index = 0

    for _ in network_address:
        first_host.append(network_address[index])
        index += 1
    first_host[3] = first_host[3] + 1

    return first_host


def get_last_host():
    last_host = []
    index = 0

    for _ in broadcast_address:
        last_host.append(broadcast_address[index])
        index += 1
    last_host[3] = last_host[3] - 1

    return last_host


def get_placement():
    num_roll = random.randint(1, 6)

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


def num_of_subnets():
    # may be possible to use the cidr block lists with conditionals and match them with the correct amount of subnets/hosts for that segment
    return


def num_of_hosts():

    return


def generate_question():

    num_roll = random.randint(1, 24)

    if num_roll == 1:
        subnetting_question = f"What valid host range is the IP address {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]}{cidr_block} a part of?"
    elif num_roll == 2:
        subnetting_question = f"What valid host range is the IP address {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} a part of?"
    elif num_roll == 3:
        subnetting_question = f"Which subnet does host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]}{cidr_block} belong to?"
    elif num_roll == 4:
        subnetting_question = f"Which subnet does host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belong to?"
    elif num_roll == 5:
        subnetting_question = f"What subnet does host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]}{cidr_block} belong to?"
    elif num_roll == 6:
        subnetting_question = f"What subnet does host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belong to?"
    elif num_roll == 7:
        subnetting_question = f"Your server needs to be assigned the last usable host address on the {placement} subnet of network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}. What address would you assign to the server?"
    elif num_roll == 8:
        subnetting_question = f"Your server needs to be assigned the last usable host address on the {placement} subnet of network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What address would you assign to the server?"
    elif num_roll == 9:
        subnetting_question = f"What is the first valid host address on the subnet that host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
    elif num_roll == 10:
        subnetting_question = f"What is the first valid host address on the subnet that host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {cidr_block} belongs to?"
    elif num_roll == 11:
        subnetting_question = f"What is the broadcast address of the subnet that host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]}{cidr_block} is a part of?"
    elif num_roll == 12:
        subnetting_question = f"What is the broadcast address of the subnet that host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} is a part of?"
    elif num_roll == 13:
        subnetting_question = f"What is the last valid host address on the subnet that host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]}{cidr_block} belongs to?"
    elif num_roll == 14:
        subnetting_question = f"What is the last valid host address on the subnet that host {ip_address[0]}.{ip_address[1]}.{ip_address[2]}.{ip_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
    elif num_roll == 15:
        subnetting_question = f"What is the broadcast address of network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}?"
    elif num_roll == 16:
        subnetting_question = f"What is the broadcast address of network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 17:
        subnetting_question = f"You need to assign a server the last valid host address on the subnet {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}. What IP address would you assign?"
    elif num_roll == 18:
        subnetting_question = f"You need to assign a server the last valid host address on the subnet {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What IP address would you assign?"
    elif num_roll == 19:
        subnetting_question = f"How many subnets and hosts per subnet can you get from the network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}?"
    elif num_roll == 20:
        subnetting_question = f"How many subnets and hosts per subnet can you get from the network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 21:
        subnetting_question = f"What is the last valid host on subnet {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}?"
    elif num_roll == 22:
        subnetting_question = f"What is the last valid host on subnet {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
    elif num_roll == 23:
        subnetting_question = f"You have the following subnetted network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}. You need to assign your router the first usable host address on the {placement}. subnet. What address would you use?"
    elif num_roll == 24:
        subnetting_question = f"You have the following subnetted network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. You need to assign your router the first usable host address on the {placement}. subnet. What address would you use?"
    # elif num_roll == 25:
    #     subnetting_question = f"How many subnets are available with the network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]}{cidr_block}"
    # elif num_roll == 26:
    #     subnetting_question = f"How many subnets are available with the network {network_address[0]}.{network_address[1]}.{network_address[2]}.{network_address[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"

    return subnetting_question


ip_address = new_host_address()
subnet_mask = get_variable_subnet()
cidr_block = get_cidr_block()
address_block = get_address_block()
interesting_octet = get_interesting_octet()
network_address = get_network_add()
broadcast_address = get_broadcast_address()
first_valid_host = get_first_host()
last_valid_host = get_last_host()
placement = get_placement()
question = generate_question()
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
