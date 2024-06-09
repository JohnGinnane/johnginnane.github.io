import re

# Games/
#     Colour: Max Number
#     Set/
#         Colour: Number

games = open("input.txt", "r").readlines()
#pattern = r"(\s+(?:[0-9]+\s*(?:green|blue|red))(?:,|))+(?:;|$|\s)"
game_pattern = r"Game ([0-9]+):"
set_pattern = r"((?:[0-9]+\s)\w+)+"
count_pattern = r"([0-9]+)\s*(\w+)"
index = 1

game_dict = {}
max_dict = {}
power_dict = {}

for game in games:
    #print("\n\n" + str(index) + " - " + game + "\n")
    index+=1
    game = game.strip()

    # Try to identify the game number
    gamenum = re.search(game_pattern, game)
    if gamenum:
        gamenum = int(gamenum.group(1))
        game_dict[gamenum] = {}
        max_dict[gamenum] = {}
    else:
        continue
    
    # I couldn't figure out how to
    # split the sets up using regex
    # so I'm going to use split()
    sets = game.split(";")
    
    set_index = 0
    for s in sets:
        set_index += 1
        game_dict[gamenum][set_index] = {}
        
        match = re.findall(set_pattern, s)
        for m in match:
            count = re.findall(count_pattern, m)
            if count:
                colour = count[0][1]
                colour_count = int(count[0][0])

                if colour in game_dict[gamenum][set_index]:
                    if colour_count > game_dict[gamenum][set_index][colour]:
                        game_dict[gamenum][set_index][colour] = colour_count
                else:
                    game_dict[gamenum][set_index][colour] = colour_count

                # Add colour to list of max values
                if not colour in max_dict[gamenum]:
                    max_dict[gamenum][colour] = colour_count
                else:
                    if colour_count > max_dict[gamenum][colour]:
                        max_dict[gamenum][colour] = colour_count

# Calculate powers of all sets for each game
for game in max_dict:
    game_power = 1
    
    for colour in max_dict[game]:
        game_power *= max_dict[game][colour]
        
    power_dict[game] = game_power
    
    #print("Game #" + str(game) + ": " + str(power_dict))

# Print the game dictionary
if 1 == 2:
    for game in game_dict:
        print("Game #" + str(game))
        
        for game_set in game_dict[game]:
            print("\tSet #" + game_set + "")
            
            for colour in game_dict[game][game_set]:
                print("\t\t" + colour + ": " + str(game_dict[game][game_set][colour]))




# Print max values per colour per game
if 1 == 2:
    for game in max_dict:
        print("Game #" + str(game))

        for colour in max_dict[game]:
            print("\t" + colour + ": " + str(max_dict[game][colour]))

# Part 1
if 1 == 1:
    max_colours = {
        "red": 12,
        "green": 13,
        "blue": 14
        }

    total = 0

    for game in max_dict:
        #print("Game #" + str(game))
        game_good = True
        
        for colour in max_colours:
            #print("\t" + colour + ": " + str(max_dict[game][colour]))
            
            if max_dict[game][colour] > max_colours[colour]:
                game_good = False
                break

        if game_good:
            total += game

    print("Total IDs: " + str(total))

# Part 2
if 1 == 1:
    total_power = 0

    for game in power_dict:
        total_power += power_dict[game]

    print("Total Power: " + str(total_power))
