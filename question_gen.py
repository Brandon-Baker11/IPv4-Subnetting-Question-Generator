import random
import os


def new_host_address():
    "Generates a random IP address host."
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
    "Generates the subnet mask for the IP address that is generated."
    excluded_mask = 255
    possible_masks = [item for item in masks if item != excluded_mask]
    
    if ip[0] == 10:

        add_zeroes = 2
        init_subnet = [255]
        octet = random.choice(possible_masks)
        init_subnet.append(octet)

        for _ in range(add_zeroes):
            init_subnet.append(0)

    elif ip[0] == 172:
        init_subnet = [255, 255]
        octet = random.choice(possible_masks)
        init_subnet.append(octet)
        init_subnet.append(0)

    elif ip[0] == 192:
        init_subnet = [255, 255, 255]
        octet = random.choice(possible_masks)
        init_subnet.append(octet)

    return init_subnet


def get_cidr_block(subnet_mask, masks):
    "Selects the appropriate CIDR notation depending on the subnet mask."
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
    "Returns the index value correlated with the interesting octet which is used to calculate the subnet ID/broadcast address."
    for octet in subnet_mask:
        if octet != 255:
            int_octet_index = subnet_mask.index(octet)
            break

    return int_octet_index


def get_address_block(subnet_mask):
    "Calculates the address block for the IP configuration that is generated."
    for octet in subnet_mask:
        if octet != 255:
            int_octet = octet
            break

    block = 256 - int_octet

    return block


def get_subnet_id(subnet_mask, ip, address_size, int_octet):
    "Calculates the subnet ID address for the IP configuration that is generated."
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
    "Calculates the parent network address for the IP configuration that is generated."
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
    "Calculates the broadcast address for the IP configuration that is generated."
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


def get_first_last_subnet_hosts(net_address, bcast_address, address_size):
    "Returns the valid host range for the subnet ID that is generated."
    first_host = []
    last_host = []
    index = 0

    for _ in net_address:
        first_host.append(net_address[index])
        last_host.append(bcast_address[index])
        index += 1

    if address_size >= 2:
        first_host[3] = first_host[3] + 1
        last_host[3] = last_host[3] - 1
        
    return first_host, last_host
    

def get_placement(subnet_mask):
    "Generates a placement variable based on the available subnets an address can have."
    place = ""
    end_range = 0
    start_point = 0

    for octet in subnet_mask:
        if octet == 255:
            continue
        if octet == 128:
            end_range = 2
            break
        if octet == 192:
            end_range = 4
            break
        else:
            end_range = 8
            break

    num_roll = random.randint(1, 8)

    if end_range == 2:
        if num_roll == 1:
            place = "first"
            start_point = 1
        else:
            place = "second"
            start_point = 2

    if end_range == 4:
        if num_roll == 1:
            place = "first"
            start_point = 1
        elif num_roll == 2:
            place = "second"
            start_point = 2
        elif num_roll == 3:
            place = "third"
            start_point = 3
        else:
            place = "fourth"
            start_point = 4

    if end_range == 8:
        if num_roll == 1:
            place = "first"
            start_point = 1
        elif num_roll == 2:
            place = "second"
            start_point = 2
        elif num_roll == 3:
            place = "third"
            start_point = 3
        elif num_roll == 4:
            place = "fourth"
            start_point = 4
        elif num_roll == 5:
            place = "fifth"
            start_point = 5
        elif num_roll == 6:
            place = "sixth"
            start_point = 6
        elif num_roll == 7:
            place = "seventh"
            start_point = 7
        else:
            place = "eighth"
            start_point = 8

    return place, start_point


def get_valid_parent_hosts(parent_id, subnet_mask, address_size, subnet_placement_int):
    "Returns the valid address range of the parent address that is generated."
    _first = []
    _last = []
    index = 0
    _start = subnet_placement_int - 1
    _end = subnet_placement_int

    for octet in parent_id:
        _first.append(octet)
        _last.append(octet)

    for octet in subnet_mask:
        if octet == 255:
            index += 1
        else:
            break
    if index == 1:
        _first[index] += _start * address_size
        _first[2] = 0
        _first[3] += 1
        _last[index] += _end * address_size - 1
        _last[2] = 255
        _last[3] = 254
    elif index == 2:
        _first[index] += _start * address_size
        _first[3] += 1
        _last[index] += _end * address_size - 1
        _last[3] = 254
    else:
        _first[index] += _start * address_size + 1
        _last[index] += _end * address_size - 1
    
    return _first, _last


def get_number_of_subnets(ip, subnet_mask, masks):
    "Returns the number of hosts that are within the IP address and subnet mask configuration."
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
    "Returns the number of hosts that are within the IP address and subnet mask configuration."
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
    "Displays the banner for the program."
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


def clear_screen():
    """Clears the console screen based on the operating system"""
    # Check if the OS is Windows (nt stands for New Technology)
    if os.name == 'nt':
        _ = os.system('cls')
    # Otherwise, assume it's a POSIX system (Linux, macOS, Unix, etc.)
    else:
        _ = os.system('clear')


def check_user_choice(menu):
    "Checks the validity of the input provided by the user."
    continue_practice = True
    is_valid_input = False
    menu_option = ""
    action = ""

    if menu == "answer":
        menu_option = "R"
        action = "to Reveal the Answer"
    elif menu == "next":
        menu_option = "N"
        action = "for the Next Question"
    elif menu == "start":
        menu_option = "Enter"
        action = "to Start Your Subnetting Practice"

    while not is_valid_input:
        MAX_LENGTH = 1
        try:
            choice = input(
                f"Press the [{menu_option}] Key {action}, or press [E] to Exit the Program.\n")
            choice = choice.upper()
            if menu == "start" and choice == "":
                is_valid_input = True
            elif choice == menu_option:
                is_valid_input = True
            elif choice == "E":
                continue_practice = False
                is_valid_input = True
                break
            elif choice.isalpha() is False:
                raise ValueError(
                    f"Invalid Input: Press the [{menu_option}] Key {action} or [E] to Exit the Program.")
            elif len(choice) > MAX_LENGTH:
                raise ValueError(
                    f"Error: Provided too many characters. Please limit input to {MAX_LENGTH} character.")
            else:
                raise ValueError(
                    f"Invalid Input: Press the [{menu_option}] Key {action} or [E] to Exit the Program.")
        except ValueError as err:
            clear_screen()
            print(banner)
            if menu != "start":
                print(q_n_a.get("question"))
            print(" ")
            print(err)
            print(" ")
    return continue_practice


def generate_qna(ip, cidr, subnet_mask, subnet_id, bcast_address, place, first_last_subnet, host_amount, subnet_amount, parent_id, first_last_parent):
    "Returns a random question using random.randint and applies the IP addressing details that were generated."

    num_roll = random.randint(1, 26)
    question = ""
    answer = ""

    if num_roll == 1:
        question = f"What valid host range is the IP address {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} a part of?"
        answer = f"{first_last_subnet[0][0]}.{first_last_subnet[0][1]}.{first_last_subnet[0][2]}.{first_last_subnet[0][3]} - {first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 2:
        question = f"What valid host range is the IP address {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} a part of?"
        answer = f"{first_last_subnet[0][0]}.{first_last_subnet[0][1]}.{first_last_subnet[0][2]}.{first_last_subnet[0][3]} - {first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 3:
        question = f"Which subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belong to?"
        answer = f"{subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}"
    elif num_roll == 4:
        question = f"Which subnet does host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belong to?"
        answer = f"{subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}"
    elif num_roll == 5:
        question = f"Your server needs to be assigned the last usable host address on the {place[0]} subnet of network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]}{cidr}. What address would you assign to the server?"
        answer = f"{first_last_parent[1][0]}.{first_last_parent[1][1]}.{first_last_parent[1][2]}.{first_last_parent[1][3]}"
    elif num_roll == 6:
        question = f"Your server needs to be assigned the last usable host address on the {place[0]} subnet of network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What address would you assign to the server?"
        answer = f"{first_last_parent[1][0]}.{first_last_parent[1][1]}.{first_last_parent[1][2]}.{first_last_parent[1][3]}"
    elif num_roll == 7:
        question = f"What is the first valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
        answer = f"{first_last_subnet[0][0]}.{first_last_subnet[0][1]}.{first_last_subnet[0][2]}.{first_last_subnet[0][3]}"
    elif num_roll == 8:
        question = f"What is the first valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belongs to?"
        answer = f"{first_last_subnet[0][0]}.{first_last_subnet[0][1]}.{first_last_subnet[0][2]}.{first_last_subnet[0][3]}"
    elif num_roll == 9:
        question = f"What is the broadcast address of the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} is a part of?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 10:
        question = f"What is the broadcast address of the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} is a part of?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 11:
        question = f"What is the last valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}{cidr} belongs to?"
        answer = f"{first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 12:
        question = f"What is the last valid host address on the subnet that host {ip[0]}.{ip[1]}.{ip[2]}.{ip[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]} belongs to?"
        answer = f"{first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 13:
        question = f"What is the broadcast address of network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 14:
        question = f"What is the broadcast address of network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{bcast_address[0]}.{bcast_address[1]}.{bcast_address[2]}.{bcast_address[3]}"
    elif num_roll == 15:
        question = f"You need to assign a server the last valid host address on the subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}. What IP address would you assign?"
        answer = f"{first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 16:
        question = f"You need to assign a server the last valid host address on the subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. What IP address would you assign?"
        answer = f"{first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 17:
        question = f"How many subnets and valid hosts per subnet can you get from the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{host_amount} hosts and {subnet_amount} subnets"
    elif num_roll == 18:
        question = f"How many subnets and valid hosts per subnet can you get from the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{host_amount} hosts and {subnet_amount} subnets"
    elif num_roll == 19:
        question = f"What is the last valid host on subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 20:
        question = f"What is the last valid host on subnet {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{first_last_subnet[1][0]}.{first_last_subnet[1][1]}.{first_last_subnet[1][2]}.{first_last_subnet[1][3]}"
    elif num_roll == 21:
        question = f"You have the following subnetted network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]}{cidr}. You need to assign your router the first usable host address on the {place[0]} subnet. What address would you use?"
        answer = f"{first_last_parent[0][0]}.{first_last_parent[0][1]}.{first_last_parent[0][2]}.{first_last_parent[0][3]}"
    elif num_roll == 22:
        question = f"You have the following subnetted network {parent_id[0]}.{parent_id[1]}.{parent_id[2]}.{parent_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}. You need to assign your router the first usable host address on the {place[0]} subnet. What address would you use?"
        answer = f"{first_last_parent[0][0]}.{first_last_parent[0][1]}.{first_last_parent[0][2]}.{first_last_parent[0][3]}"
    elif num_roll == 23:
        question = f"How many subnets are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}"
        answer = f"{subnet_amount} subnets"
    elif num_roll == 24:
        question = f"How many subnets are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{subnet_amount} subnets"
    elif num_roll == 25:
        question = f"How many valid hosts are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]}{cidr}?"
        answer = f"{host_amount} hosts"
    elif num_roll == 26:
        question = f"How many valid hosts are available with the network {subnet_id[0]}.{subnet_id[1]}.{subnet_id[2]}.{subnet_id[3]} {subnet_mask[0]}.{subnet_mask[1]}.{subnet_mask[2]}.{subnet_mask[3]}?"
        answer = f"{host_amount} hosts"
    return {"question": question, "answer": answer}


banner = display_banner()
clear_screen()
print(banner)
print(" ")
user_input = check_user_choice("start")

while user_input is True:
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
    first_last_valid_subnet_hosts = get_first_last_subnet_hosts(
         subnetted_network_id, broadcast_address, address_block)
    placement = get_placement(variable_length_subnet_mask)
    first_last_parent_hosts = get_valid_parent_hosts(
         parent_network_id, variable_length_subnet_mask, address_block, placement[1])
    num_of_subnets = get_number_of_subnets(
        ip_address, variable_length_subnet_mask, possible_variable_masks)
    num_of_hosts = get_number_of_hosts(
        ip_address, variable_length_subnet_mask, possible_variable_masks)
    q_n_a = generate_qna(
        ip_address, cidr_block, variable_length_subnet_mask, subnetted_network_id, broadcast_address, placement, first_last_valid_subnet_hosts, num_of_hosts, num_of_subnets, parent_network_id, first_last_parent_hosts)

    clear_screen()
    print(banner)
    print(q_n_a.get("question"))
    print(" ")

    user_input = check_user_choice("answer")

    if user_input is False:
        break

    clear_screen()
    print(banner)
    print(q_n_a.get("question"))
    print(" ")
    print("Answer:", q_n_a.get("answer", "\n"))
    print(" ")

    user_input = check_user_choice("next")

    if user_input is False:
        break
