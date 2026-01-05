# pylint: disable = line-too-long
# pylint: disable = missing-function-docstring
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


def get_variable_sub():
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


def get_network_add_v2():

    return


def get_network_add():
    """This funtion calculates a network address from the function new_host_add()"""

    ip_classes = ["a", "b", "c"]
    # divisible_by = []
    selected_class = random.choice(ip_classes)

    # Class A address
    if selected_class == "a":
        ip_octets = [10]
        for _ in range(3):
            ip_octets.append(0)
    # Class B address
    elif selected_class == "b":
        ip_octets = [172]
        ip_octets.append(random.randint(16, 31))
        for _ in range(2):
            ip_octets.append(0)
    # Class C address
    elif selected_class == "c":
        ip_octets = [192, 168]
        for _ in range(2):
            ip_octets.append(0)

    net_address = f"{ip_octets[0]}.{ip_octets[1]}.{ip_octets[2]}.{ip_octets[3]}"

    return net_address


num = [1, 2, 3, 4, 5, 6, 7]
ip_address = new_host_address()
subnet_mask = get_variable_sub()
cidr_block = get_cidr_block()
print(ip_address, subnet_mask, cidr_block)
# for item in num:
#     print(num.index(item))
# new_ip_class = get_variable_sub_v2()

# def subnetting_tool():
#     """ This function will generate an IP address and do the calculations to get the Subnet Mask, Network and Broadcast addresses,
#     and first and last hosts"""
#     ip_classes = ["a", "b", "c"]
#     masks = [128, 192, 224, 240, 248, 252, 254]
#     cidr_blocks_a = ["/9", "/10", "/11", "/12", "/13", "/14", "/15"]
#     cidr_blocks_b = ["/17", "/18", "/19", "/20", "/21", "/22", "/23"]
#     cidr_blocks_c = ["/25", "/26", "/27", "/28", "/29", "/30", "/31"]

#     return


# subnet_cidr = get_variable_sub()
# print(
#     f"The IP address and subnet is {new_host_add()}{subnet_cidr[1]} {subnet_cidr[0]}")
# print(get_network_add())


# Questions that only require a host IP and subnet or CIDR block
q_pool_1 = [
    "What valid host range is the IP address [ip address/CIDR] a part of?",
    "What is the first valid host address on the subnet that host [ip address subnet mask] belongs to?",
    "Which subnet does host [hostip/cidr] belong to? (random host)",
    "What is the broadcast address of the subnet that host [ipaddress/cidr] is a part of?",
    "What subnet does host [hostip/cidr] belong to?",
    "What is the last valid host address on the subnet that host [hostip/cidr] belongs to?"
]
q_pool_2 = [
    "Your server needs to be assigned the last usable host address on the 5th subnet of network [subnetip/CIDR]. What address would you assign to the server?",
    "You need to divide the [subnetadd] into [x amount] of subnets with [x amount] of hosts per subnet. What subnet mask should you use?",
    "What is the broadcast address of network [subnetadd/cidr]?",
    "You need to subnet the [subnetadd] network into [x amount] of different subnets. What subnet mask would you use?",
    "You need to assign a server the last valid host address on the subnet [subnetadd/cidr]. What IP address would you assign?",
    "How many subnets and hosts per subnet can you get from the network [subnetadd/cidr]?",
    "What is the last valid host on subnet [subnetadd/cidr]?",
    "You have been given the [subnetadd] network. You need to design a subnet mask that will give you [x amount] of subnets and up to [x amount] of hosts. What subnet mask should you use?",
    "You have the following subnetted network [subnetadd/cidr]. You need to assign your router the first usable host address on the third/fourth/fifth/etc. subnet. What address would you use?",
    "How many subnets are available with the network [subnet/ip]?"
    "Network [network_add] needs to be divided into [x amount] subnets, while keeping as many usable hosts in each subnet as possible. What mask should be used"

]
